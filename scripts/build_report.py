#!/usr/bin/env python3
"""
build_report.py — Strategy Case Report HTML Deck Builder
Version: 2.6 | 2026-03-23

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
定位與使用時機
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

路徑 B（HTML artifact）有兩條執行路徑，視環境選擇：

  路徑 B-1｜report-renderer skill（建議）
    適用：Claude.ai、Claude Desktop、Cowork 等支援 skill 的環境
    流程：Phase 6 截點輸出 report_data.json
          → 開新對話啟用 report-renderer skill
          → 貼入 JSON，說明「渲染成 HTML artifact」
          → report-renderer skill 執行渲染

  路徑 B-2｜build_report.py（Claude Code 環境 / report-renderer 不可用時）
    適用：Claude Code 本地環境，或 report-renderer skill 尚未安裝時的 fallback
    流程：Phase 6 截點輸出 report_data.json
          → 在 Claude Code 環境呼叫本 script
          → 直接產出 report.html

兩條路徑讀取相同的 report_data.json，輸出相同的 HTML 結構。
report-renderer skill 可用時優先走 B-1，build_report.py 是備用路徑，不是廢棄路徑。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
v2.6 變更
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  - 對齊 report-data-schema.md v2.6 三欄結構（confirmed / estimated / unknown）
  - 新增 root_evidence 渲染（壓力層 / 張力層 / 邊界層 status badge）
  - why_it_lands 改從 confirmed/estimated/unknown 三欄讀取，移除舊 verified_facts / preliminary_reads
  - what_to_steal 改從 scenarios[] 結構讀取，移除舊 condition 字串
  - real_problem / tension / strategic_reframe / system 全部支援三欄輸出
  - unknown 欄位不進正文，寫入來源附錄「待補資料」區塊
  - insight_confidence badge：estimated 時加「初步判讀」標注
  - validate() 新增舊 schema 欄位偵測（body / verified_facts / condition），有舊欄位直接報錯

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
使用方式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

由 Claude Code 呼叫：
    python scripts/build_report.py --input report_data.json --output report.html

直接執行（本機）：
    python scripts/build_report.py --input report_data.json --output report.html [--open]

Dependencies: Python 3.8+，無需第三方套件
Schema:       references/report-data-schema.md v2.6（以此為唯一準則，不參考 report_schema.json）
"""

import argparse
import json
import sys
from pathlib import Path


# ─────────────────────────────────────────
# 1. CLI
# ─────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="Build strategy case report HTML deck from JSON data")
    p.add_argument("--input",  required=True, help="Path to report_data.json")
    p.add_argument("--output", required=True, help="Output HTML file path")
    p.add_argument("--open",   action="store_true", help="Open in browser after build")
    return p.parse_args()


# ─────────────────────────────────────────
# 2. Validation (v2.6)
# ─────────────────────────────────────────

REQUIRED_PAGES_FULL   = {"real_problem", "tension", "strategic_reframe", "system",
                          "why_it_lands", "what_to_steal"}
REQUIRED_PAGES_SPRINT = {"real_problem", "tension", "strategic_reframe", "what_to_steal"}

def validate(data: dict) -> list[str]:
    """Return list of validation errors. Empty = pass."""
    errors = []

    # meta
    for field in ("title", "date", "mode"):
        if not data.get("meta", {}).get(field):
            errors.append(f"meta.{field} is required")

    mode = data.get("meta", {}).get("mode", "full")
    if mode not in ("full", "sprint"):
        errors.append(f"meta.mode must be 'full' or 'sprint', got '{mode}'")

    # visual
    vis = data.get("visual", {})
    for c in ("bg_primary", "bg_secondary", "text_primary", "text_secondary", "accent"):
        if not vis.get("colors", {}).get(c):
            errors.append(f"visual.colors.{c} is required")
    for f in ("display", "body"):
        if not vis.get("fonts", {}).get(f):
            errors.append(f"visual.fonts.{f} is required")

    # cases
    cases = data.get("cases", [])
    if not cases:
        errors.append("At least one case is required")

    required_pages = REQUIRED_PAGES_FULL if mode == "full" else REQUIRED_PAGES_SPRINT
    for i, case in enumerate(cases):
        prefix = f"cases[{i}]"
        for field in ("brand", "industry", "year", "case_in_one_line"):
            if not case.get(field):
                errors.append(f"{prefix}.{field} is required")
        # root_evidence required in v2.6
        if "root_evidence" not in case:
            errors.append(f"{prefix}.root_evidence is required (v2.6)")
        # pages
        pages = case.get("pages", {})
        for page in required_pages:
            if page not in pages:
                errors.append(f"{prefix}.pages.{page} is missing (required for {mode} mode)")
        # detect old schema fields
        for page_name, page_data in pages.items():
            if isinstance(page_data, dict):
                if "body" in page_data:
                    errors.append(
                        f"{prefix}.pages.{page_name}: found old-schema field 'body'. "
                        "v2.6 uses confirmed/estimated/unknown. See report-data-schema.md."
                    )
                if "verified_facts" in page_data:
                    errors.append(
                        f"{prefix}.pages.{page_name}: found old-schema field 'verified_facts'. "
                        "v2.6 uses confirmed[].claim. See report-data-schema.md."
                    )
                if "methods" in page_data:
                    for j, m in enumerate(page_data.get("methods", [])):
                        if "condition" in m and "scenarios" not in m:
                            errors.append(
                                f"{prefix}.pages.{page_name}.methods[{j}]: "
                                "found old-schema field 'condition'. "
                                "v2.6 uses scenarios[]. See report-data-schema.md."
                            )

    return errors


# ─────────────────────────────────────────
# 3. Helpers
# ─────────────────────────────────────────

def google_fonts_link(display: str, body: str) -> str:
    families = "+".join(
        f"{f.replace(' ', '+')}:wght@400;600;700"
        for f in dict.fromkeys([display, body])
    )
    return f'<link href="https://fonts.googleapis.com/css2?family={families}&display=swap" rel="stylesheet">'


def css_variables(colors: dict, fonts: dict) -> str:
    return f"""
  --bg-primary:    {colors['bg_primary']};
  --bg-secondary:  {colors['bg_secondary']};
  --text-primary:  {colors['text_primary']};
  --text-secondary:{colors['text_secondary']};
  --accent:        {colors['accent']};
  --font-display:  '{fonts['display']}', serif;
  --font-body:     '{fonts['body']}', sans-serif;"""


def pending_badge(label: str = "初步判讀") -> str:
    return f'<span class="badge-pending">{label}</span>'


def unknown_badge() -> str:
    return '<span class="badge-unknown">待補資料</span>'


def status_badge(status: str) -> str:
    """Render a root_evidence layer status badge."""
    labels = {"rooted": "已扎根", "estimated": "代理推論", "unknown": "缺乏佐證"}
    css_classes = {"rooted": "badge-rooted", "estimated": "badge-estimated", "unknown": "badge-unknown-layer"}
    label = labels.get(status, status)
    css = css_classes.get(status, "badge-pending")
    return f'<span class="{css}">{label}</span>'


def render_confirmed_list(items: list, show_source: bool = True) -> str:
    """Render confirmed[] items as <li> elements."""
    if not items:
        return ""
    lis = ""
    for item in items:
        claim = item.get("claim") or item.get("fact", "")
        source = item.get("source_ref", "")
        source_html = f' <span class="source-ref">（{source}）</span>' if source and show_source else ""
        lis += f"<li>{claim}{source_html}</li>"
    return lis


def render_estimated_list(items: list) -> str:
    """Render estimated[] items with proxy annotation."""
    if not items:
        return ""
    lis = ""
    for item in items:
        claim = item.get("claim", "")
        proxy = item.get("proxy", "")
        assumption = item.get("assumption", "")
        proxy_html = ""
        if proxy or assumption:
            detail_parts = []
            if proxy:
                detail_parts.append(f"代理：{proxy}")
            if assumption:
                detail_parts.append(f"前提：{assumption}")
            proxy_html = f' <span class="proxy-note">（{" ／ ".join(detail_parts)}）</span>'
        lis += f"<li>{pending_badge()} {claim}{proxy_html}</li>"
    return lis


def render_unknown_appendix_items(page_name: str, items: list) -> str:
    """Render unknown[] items for the pending-data appendix section."""
    if not items:
        return ""
    rows = ""
    for item in items:
        question = item.get("question", "")
        needed = item.get("needed", "")
        impact = item.get("impact", "")
        rows += f"""
      <tr>
        <td class="pending-page">{page_name}</td>
        <td>{question}</td>
        <td class="pending-needed">{needed}</td>
        <td class="pending-impact">{impact}</td>
      </tr>"""
    return rows


# ─────────────────────────────────────────
# 4. Nav + Cover + Method + Overview
# ─────────────────────────────────────────

def nav_html(meta: dict, cases: list, conclusion: dict | None) -> str:
    links = ['<a href="#cover">封面</a>']
    for i, case in enumerate(cases, 1):
        label = case.get("brand", f"案例{i}")
        links.append(f'<a href="#case-{i}">{label}</a>')
    if conclusion and conclusion.get("cross_case_insight"):
        links.append('<a href="#conclusion">結論</a>')

    title = meta.get("title", "")
    short_title = title.split("｜")[0] if "｜" in title else title[:10]
    nav_links = " <span>／</span> ".join(links)
    return f"""
<nav id="top-nav">
  <span class="nav-title">{short_title}</span>
  <div class="nav-links">{nav_links}</div>
</nav>"""


def section_cover(meta: dict) -> str:
    subtitle = meta.get("subtitle", "")
    date = meta.get("date", "")
    return f"""
<section id="cover" class="page page-statement">
  <div class="cover-content">
    <p class="cover-date">{date}</p>
    <h1 class="display">{meta['title']}</h1>
    {"<p class='cover-subtitle'>" + subtitle + "</p>" if subtitle else ""}
  </div>
</section>"""


def section_method(mode: str) -> str:
    mode_label = "Full Mode（完整分析）" if mode == "full" else "Sprint Mode（精簡分析）"
    critique = "✅ 已通過策略長視角批判（Full Mode）" if mode == "full" else "✅ 已通過 3 個核心批判問題"
    return f"""
<section id="method" class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">About This Report</p>
    <h2 class="heading">案例篩選與分析方法</h2>
    <div class="method-grid">
      <div class="method-col">
        <h3>篩選標準</h3>
        <ul>
          <li>近期台灣市場為主，有足夠公開資料</li>
          <li>有真實問題與 tension 可拆解</li>
          <li>IMC 規模足以撐起 system 分析</li>
          <li>非教科書案例，有新鮮判讀空間</li>
        </ul>
      </div>
      <div class="method-col">
        <h3>分析框架（每案）</h3>
        <ol>
          <li>Case in one line — 案例核心定義</li>
          <li>The real problem — 真實市場問題</li>
          <li>The tension — Insight 與矛盾</li>
          <li>The strategic reframe — 策略重框</li>
          <li>The system — IMC 執行系統</li>
          <li>Why it lands — 佐證與事實</li>
          <li>What to steal — 可借用方法</li>
        </ol>
      </div>
      <div class="method-col">
        <h3>品質機制</h3>
        <p>執行模式：{mode_label}</p>
        <p>{critique}</p>
        <p class="method-note">三欄輸出：confirmed（直接佐證）/ estimated（代理推論）/ unknown（待補資料）</p>
      </div>
    </div>
  </div>
</section>"""


def section_overview(cases: list) -> str:
    cards = ""
    for i, case in enumerate(cases, 1):
        # show root_evidence summary per case
        re = case.get("root_evidence", {})
        pressure_status = re.get("pressure", {}).get("status", "unknown")
        tension_status  = re.get("tension",  {}).get("status", "unknown")
        boundary_status = re.get("boundary", {}).get("status", "unknown")
        cards += f"""
      <div class="overview-card">
        <p class="eyebrow">{case.get('industry','')} · {case.get('year','')}</p>
        <h3>{case.get('brand','')}</h3>
        <p class="case-one-liner">{case.get('case_in_one_line','')}</p>
        <div class="root-badges">
          <span class="root-label">扎根</span>
          壓力 {status_badge(pressure_status)}
          張力 {status_badge(tension_status)}
          邊界 {status_badge(boundary_status)}
        </div>
      </div>"""
    return f"""
<section id="overview" class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Case Overview</p>
    <h2 class="heading">本期三個案例</h2>
    <div class="overview-grid">{cards}
    </div>
  </div>
</section>"""


# ─────────────────────────────────────────
# 5. Individual Case Pages (v2.6 three-column)
# ─────────────────────────────────────────

def section_case_intro(case: dict, idx: int) -> str:
    return f"""
<section id="case-{idx}" class="page page-statement">
  <div class="case-intro-content">
    <p class="eyebrow">Case {idx} · {case.get('industry','')} · {case.get('year','')}</p>
    <h2 class="display">{case.get('brand','')}</h2>
    <p class="case-one-liner-large">{case.get('case_in_one_line','')}</p>
  </div>
</section>"""


def page_real_problem(page: dict, case_idx: int) -> str:
    confirmed_items = render_confirmed_list(page.get("confirmed", []))
    estimated_items = render_estimated_list(page.get("estimated", []))
    has_unknown     = bool(page.get("unknown"))

    content_html = ""
    if confirmed_items:
        content_html += f'<ul class="evidence-list confirmed-list">{confirmed_items}</ul>'
    if estimated_items:
        content_html += f'<ul class="evidence-list estimated-list">{estimated_items}</ul>'
    if has_unknown:
        content_html += f'<p class="unknown-notice">{unknown_badge()} 部分問題根源尚缺佐證，詳見來源附錄「待補資料」。</p>'

    return f"""
<section class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The Real Problem</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    {content_html}
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_tension(page: dict, case_idx: int) -> str:
    insight = page.get("insight", "")
    confidence = page.get("insight_confidence", "rooted")
    confidence_badge = pending_badge("初步判讀") if confidence == "estimated" else ""

    confirmed_items = render_confirmed_list(page.get("confirmed", []))
    estimated_items = render_estimated_list(page.get("estimated", []))
    has_unknown     = bool(page.get("unknown"))

    evidence_html = ""
    if confirmed_items or estimated_items:
        evidence_html += '<div class="tension-evidence">'
        if confirmed_items:
            evidence_html += f'<ul class="evidence-list confirmed-list">{confirmed_items}</ul>'
        if estimated_items:
            evidence_html += f'<ul class="evidence-list estimated-list">{estimated_items}</ul>'
        evidence_html += '</div>'
    if has_unknown:
        evidence_html += f'<p class="unknown-notice">{unknown_badge()} 部分矛盾根源尚缺佐證，詳見來源附錄「待補資料」。</p>'

    return f"""
<section class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The Tension</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    <p class="insight-sentence">{insight} {confidence_badge}</p>
    {evidence_html}
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_reframe(page: dict, case_idx: int) -> str:
    confirmed_items = render_confirmed_list(page.get("confirmed", []))
    estimated_items = render_estimated_list(page.get("estimated", []))
    has_unknown     = bool(page.get("unknown"))

    evidence_html = ""
    if confirmed_items or estimated_items:
        evidence_html += '<div class="reframe-evidence">'
        if confirmed_items:
            evidence_html += f'<ul class="evidence-list confirmed-list">{confirmed_items}</ul>'
        if estimated_items:
            evidence_html += f'<ul class="evidence-list estimated-list">{estimated_items}</ul>'
        evidence_html += '</div>'
    if has_unknown:
        evidence_html += f'<p class="unknown-notice">{unknown_badge()} 詳見來源附錄「待補資料」。</p>'

    return f"""
<section class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The Strategic Reframe</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    <div class="reframe-grid">
      <div class="reframe-col old">
        <p class="reframe-label">舊框架</p>
        <p>{page.get('old_frame','')}</p>
      </div>
      <div class="reframe-arrow">→</div>
      <div class="reframe-col new">
        <p class="reframe-label">新框架</p>
        <p>{page.get('new_frame','')}</p>
      </div>
    </div>
    <p class="body-text rationale">{page.get('rationale','')}</p>
    {evidence_html}
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_system(page: dict, case_idx: int) -> str:
    touchpoints = page.get("touchpoints", [])
    tp_html = ""
    for tp in touchpoints:
        status_icon = "🖼" if tp.get("image_status") == "found" else "📋"
        tp_html += f"""
      <div class="touchpoint-card">
        <p class="tp-icon">{status_icon}</p>
        <p class="tp-name">{tp.get('name','')}</p>
        <p class="tp-role">{tp.get('role','')}</p>
      </div>"""

    image_brief_html = ""
    if page.get("image_brief"):
        image_brief_html = f'<div class="image-brief-note">📋 配圖待補：{page["image_brief"]}</div>'

    confirmed_items = render_confirmed_list(page.get("confirmed", []))
    estimated_items = render_estimated_list(page.get("estimated", []))
    has_unknown     = bool(page.get("unknown"))
    evidence_html = ""
    if confirmed_items:
        evidence_html += f'<ul class="evidence-list confirmed-list">{confirmed_items}</ul>'
    if estimated_items:
        evidence_html += f'<ul class="evidence-list estimated-list">{estimated_items}</ul>'
    if has_unknown:
        evidence_html += f'<p class="unknown-notice">{unknown_badge()} 詳見來源附錄「待補資料」。</p>'

    return f"""
<section class="page page-system">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The System</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    <div class="touchpoints-row">{tp_html}
    </div>
    {image_brief_html}
    {evidence_html}
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_why_it_lands(page: dict, case_idx: int) -> str:
    """
    v2.6: reads confirmed/estimated/unknown instead of verified_facts/preliminary_reads.
    confirmed → 已驗證（直接從 root_evidence 填入）
    estimated → 初步判讀（附代理變數說明）
    unknown   → 不進正文，只在 appendix 顯示
    """
    confirmed = page.get("confirmed", [])
    estimated = page.get("estimated", [])
    has_unknown = bool(page.get("unknown"))

    verified_html = ""
    if confirmed:
        def _src(item):
            sr = item.get("source_ref", "")
            return f'<span class="source-ref">（{sr}）</span>' if sr else ""
        items = "".join(
            f'<li>{item.get("claim","")}{_src(item)}</li>'
            for item in confirmed
        )
        verified_html = f"""
    <div class="evidence-col verified">
      <p class="evidence-label">已驗證事實</p>
      <ul>{items}</ul>
    </div>"""

    prelim_html = ""
    if estimated:
        items = ""
        for item in estimated:
            proxy_parts = []
            if item.get("proxy"):
                proxy_parts.append(f'代理：{item["proxy"]}')
            if item.get("assumption"):
                proxy_parts.append(f'前提：{item["assumption"]}')
            proxy_note = f' <span class="proxy-note">（{" ／ ".join(proxy_parts)}）</span>' if proxy_parts else ""
            items += f"<li>{item.get('claim','')}{proxy_note}</li>"
        prelim_html = f"""
    <div class="evidence-col prelim">
      <p class="evidence-label">初步判讀（代理推論）</p>
      <ul>{items}</ul>
    </div>"""

    unknown_notice = ""
    if has_unknown:
        unknown_notice = f'<p class="unknown-notice">{unknown_badge()} 部分成效缺乏直接佐證，詳見來源附錄「待補資料」。</p>'

    return f"""
<section class="page page-proof">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · Why It Lands</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    <div class="evidence-grid">
      {verified_html}
      {prelim_html}
    </div>
    {unknown_notice}
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_what_to_steal(page: dict, case_idx: int) -> str:
    """
    v2.6: reads methods[].scenarios[] instead of methods[].condition string.
    Each scenario: condition + (first_step | outcome) + confidence.
    boundary_status from root_evidence.boundary.status.
    """
    methods_html = ""
    for j, m in enumerate(page.get("methods", []), 1):
        title = m.get("title", "")
        boundary = m.get("boundary_status", "unknown")
        boundary_html = f'<span class="boundary-status">{status_badge(boundary)} 邊界</span>'

        scenarios_html = ""
        for sc in m.get("scenarios", []):
            condition = sc.get("condition", "")
            first_step = sc.get("first_step", "")
            outcome    = sc.get("outcome", "")
            confidence = sc.get("confidence", "estimated")
            conf_badge = pending_badge("初步判讀") if confidence == "estimated" else ""

            result_text = first_step if first_step else outcome
            result_class = "scenario-outcome" if (outcome and not first_step) else "scenario-step"
            scenarios_html += f"""
        <div class="scenario-row">
          <span class="scenario-condition">{condition}</span>
          <span class="{result_class}">{result_text} {conf_badge}</span>
        </div>"""

        methods_html += f"""
      <div class="steal-card">
        <p class="steal-num">0{j}</p>
        <p class="steal-method">{title}</p>
        {boundary_html}
        <div class="scenarios-block">{scenarios_html}
        </div>
      </div>"""

    confirmed_items = render_confirmed_list(page.get("confirmed", []))
    estimated_items = render_estimated_list(page.get("estimated", []))
    has_unknown     = bool(page.get("unknown"))
    evidence_html = ""
    if confirmed_items:
        evidence_html += f'<ul class="evidence-list confirmed-list">{confirmed_items}</ul>'
    if estimated_items:
        evidence_html += f'<ul class="evidence-list estimated-list">{estimated_items}</ul>'
    if has_unknown:
        evidence_html += f'<p class="unknown-notice">{unknown_badge()} 詳見來源附錄「待補資料」。</p>'

    return f"""
<section class="page page-takeaway">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · What To Steal</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    <div class="steal-grid">{methods_html}
    </div>
    {evidence_html}
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


# ─────────────────────────────────────────
# 6. Recap + Conclusion + Sources
# ─────────────────────────────────────────

def section_recap(cases: list) -> str:
    headers = "<th></th>" + "".join(f"<th>{c.get('brand','')}</th>" for c in cases)

    def get_confirmed_first(page_data: dict) -> str:
        items = page_data.get("confirmed", [])
        if items:
            return items[0].get("claim", "—")
        items = page_data.get("estimated", [])
        if items:
            return items[0].get("claim", "—") + " *"
        return "—"

    dims = [
        ("真實問題", lambda c: get_confirmed_first(c.get("pages", {}).get("real_problem", {}))),
        ("Tension 核心", lambda c: c.get("pages", {}).get("tension", {}).get("insight", "—")),
        ("Reframe 方向", lambda c: c.get("pages", {}).get("strategic_reframe", {}).get("new_frame", "—")),
        ("可借用方法", lambda c: (
            (c.get("pages", {}).get("what_to_steal", {}).get("methods") or [{}])[0].get("title", "—")
        )),
    ]
    rows = ""
    for label, getter in dims:
        cells = "".join(f"<td>{getter(c)}</td>" for c in cases)
        rows += f"<tr><th>{label}</th>{cells}</tr>"

    return f"""
<section id="recap" class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Cross-Case Comparison</p>
    <h2 class="heading">三案對照</h2>
    <div class="recap-table-wrap">
      <table class="recap-table">
        <thead><tr>{headers}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="recap-note">* 標記條目為代理推論（estimated），尚待直接資料驗證。</p>
  </div>
</section>"""


def section_conclusion(conclusion: dict) -> str:
    if not conclusion or not conclusion.get("cross_case_insight"):
        return ""
    key_unknowns = conclusion.get("key_unknowns", [])
    unknowns_html = ""
    if key_unknowns:
        items = "".join(f"<li>{u}</li>" for u in key_unknowns)
        unknowns_html = f"""
    <div class="key-unknowns">
      <p class="unknowns-label">知識邊界——補齊後最影響判斷的待查資訊</p>
      <ul>{items}</ul>
    </div>"""
    return f"""
<section id="conclusion" class="page page-statement">
  <div class="conclusion-content">
    <p class="eyebrow">Conclusion</p>
    <p class="display conclusion-insight">{conclusion['cross_case_insight']}</p>
    <p class="conclusion-prompt">{conclusion.get('action_prompt','')}</p>
    {unknowns_html}
  </div>
</section>"""


def section_sources(cases: list) -> str:
    """
    v2.6: Sources appendix includes two sections:
      1. Regular source list
      2. Pending data (unknown[]) from all pages
    Also separates proxy sources.
    """
    # ── Regular sources ──
    source_rows = ""
    for case in cases:
        for s in case.get("sources", []):
            type_label = {
                "official": "官方",
                "major_media": "主流媒體",
                "secondary_media": "次級媒體",
                "proxy": "代理變數來源"
            }.get(s.get("type", ""), s.get("type", ""))
            src = s.get("source", "")
            src_display = f'<a href="{src}" target="_blank">{src}</a>' if src.startswith("http") else src
            is_proxy = s.get("type") == "proxy"
            row_class = ' class="proxy-source-row"' if is_proxy else ""
            source_rows += f"""
      <tr{row_class}>
        <td>{case.get('brand','')}</td>
        <td>{s.get('label','')}</td>
        <td>{src_display}</td>
        <td>{type_label}</td>
      </tr>"""

    # ── Pending data (unknown[]) ──
    page_label_map = {
        "real_problem": "The Real Problem",
        "tension": "The Tension",
        "strategic_reframe": "The Strategic Reframe",
        "system": "The System",
        "why_it_lands": "Why It Lands",
        "what_to_steal": "What To Steal",
    }
    pending_rows = ""
    for case in cases:
        brand = case.get("brand", "")
        pages = case.get("pages", {})
        for page_key, page_data in pages.items():
            unknowns = page_data.get("unknown", []) if isinstance(page_data, dict) else []
            if unknowns:
                page_label = page_label_map.get(page_key, page_key)
                pending_rows += render_unknown_appendix_items(
                    f"{brand} · {page_label}", unknowns
                )
        # root_evidence unknown layers
        re = case.get("root_evidence", {})
        for layer_key, layer_label in [("pressure","壓力層"), ("tension","張力層"), ("boundary","邊界層")]:
            layer = re.get(layer_key, {})
            if layer.get("status") == "unknown":
                pending_rows += f"""
      <tr>
        <td class="pending-page">{brand} · 扎根 {layer_label}</td>
        <td>此層缺乏直接資料及代理變數</td>
        <td class="pending-needed">需要直接資料或有效代理變數</td>
        <td class="pending-impact">影響 Real Problem / Tension 分析深度</td>
      </tr>"""

    pending_section = ""
    if pending_rows:
        pending_section = f"""
    <h3 class="appendix-sub-heading">待補資料（unknown 層）</h3>
    <p class="appendix-note">以下資訊在分析過程中無法取得，補齊後可能改變對應頁面的判斷。</p>
    <table class="sources-table pending-table">
      <thead><tr><th>頁面</th><th>待釐清問題</th><th>需要的資料</th><th>補齊後的影響</th></tr></thead>
      <tbody>{pending_rows}</tbody>
    </table>"""

    return f"""
<section id="sources" class="page page-sources">
  <div class="page-inner">
    <p class="eyebrow">Appendix</p>
    <h2 class="heading">來源附錄</h2>
    <table class="sources-table">
      <thead><tr><th>案例</th><th>標注</th><th>來源</th><th>類型</th></tr></thead>
      <tbody>{source_rows}</tbody>
    </table>
    {pending_section}
  </div>
</section>"""


# ─────────────────────────────────────────
# 7. CSS
# ─────────────────────────────────────────

BASE_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {__CSS_VARS__ }

html { scroll-behavior: smooth; }

body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.7;
}

/* ── Nav ── */
#top-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.75rem 2.5rem;
  background: color-mix(in srgb, var(--bg-primary) 92%, transparent);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid color-mix(in srgb, var(--text-secondary) 20%, transparent);
  font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--text-secondary);
}
.nav-title { font-family: var(--font-display); font-weight: 700; color: var(--text-primary); }
.nav-links { display: flex; gap: 0.25rem; align-items: center; flex-wrap: wrap; }
.nav-links a {
  color: var(--text-secondary); text-decoration: none; padding: 0.25rem 0.5rem;
  border-radius: 2px; transition: color 0.2s;
}
.nav-links a:hover { color: var(--accent); }
.nav-links span { color: var(--text-secondary); opacity: 0.4; }

/* ── Pages ── */
.page {
  min-height: 100vh; padding: 7rem 6vw 4rem;
  display: flex; flex-direction: column; justify-content: center;
}
.page-inner { max-width: 900px; width: 100%; }

/* ── Typography ── */
.display {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 5rem);
  font-weight: 700; letter-spacing: -0.02em;
  line-height: 1.1;
}
.heading {
  font-family: var(--font-body);
  font-size: clamp(1rem, 2vw, 1.4rem);
  font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--text-secondary);
  margin-bottom: 1.5rem;
}
.eyebrow {
  font-size: 0.7rem; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--accent);
  margin-bottom: 0.75rem; opacity: 0.9;
}
.body-text { font-size: 1rem; line-height: 1.8; color: var(--text-primary); max-width: 660px; }
.page-footer {
  margin-top: 2.5rem; padding-top: 1.25rem;
  border-top: 1px solid color-mix(in srgb, var(--accent) 30%, transparent);
  font-size: 0.85rem; color: var(--accent); font-style: italic;
}
.insight-sentence {
  font-family: var(--font-display);
  font-size: clamp(1.2rem, 2.5vw, 1.8rem);
  font-weight: 600; color: var(--text-primary);
  margin-bottom: 1.25rem; max-width: 700px;
}

/* ── Badges ── */
.badge-pending {
  display: inline-block; font-size: 0.68rem; padding: 0.15rem 0.5rem;
  background: color-mix(in srgb, #f0a500 15%, transparent);
  color: #f0a500; border: 1px solid #f0a500;
  border-radius: 2px; letter-spacing: 0.04em;
  vertical-align: middle;
}
.badge-unknown {
  display: inline-block; font-size: 0.68rem; padding: 0.15rem 0.5rem;
  background: color-mix(in srgb, var(--text-secondary) 15%, transparent);
  color: var(--text-secondary); border: 1px solid var(--text-secondary);
  border-radius: 2px; letter-spacing: 0.04em;
  vertical-align: middle;
}
.badge-rooted {
  display: inline-block; font-size: 0.65rem; padding: 0.1rem 0.45rem;
  background: color-mix(in srgb, #4caf7d 18%, transparent);
  color: #4caf7d; border: 1px solid #4caf7d;
  border-radius: 2px;
}
.badge-estimated {
  display: inline-block; font-size: 0.65rem; padding: 0.1rem 0.45rem;
  background: color-mix(in srgb, #f0a500 15%, transparent);
  color: #f0a500; border: 1px solid #f0a500;
  border-radius: 2px;
}
.badge-unknown-layer {
  display: inline-block; font-size: 0.65rem; padding: 0.1rem 0.45rem;
  background: color-mix(in srgb, var(--text-secondary) 12%, transparent);
  color: var(--text-secondary); border: 1px solid var(--text-secondary);
  border-radius: 2px;
}

/* ── Evidence lists ── */
.evidence-list { padding-left: 1.1rem; margin: 0.75rem 0; }
.evidence-list li { font-size: 0.9rem; margin-bottom: 0.5rem; line-height: 1.6; }
.confirmed-list li { color: var(--text-primary); }
.estimated-list li { color: var(--text-secondary); font-style: italic; }
.source-ref { font-size: 0.75rem; opacity: 0.6; }
.proxy-note { font-size: 0.75rem; opacity: 0.65; }
.unknown-notice {
  margin-top: 0.75rem; padding: 0.5rem 0.8rem;
  background: color-mix(in srgb, var(--text-secondary) 8%, transparent);
  border-left: 2px solid var(--text-secondary);
  font-size: 0.82rem; color: var(--text-secondary);
}

/* ── Root evidence badges in overview ── */
.root-badges {
  display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;
  margin-top: 0.75rem; font-size: 0.72rem; color: var(--text-secondary);
}
.root-label { letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.5; }

/* ── Statement pages ── */
.page-statement { background: var(--bg-primary); }
.cover-content, .case-intro-content, .conclusion-content { max-width: 800px; }
.cover-date { font-size: 0.75rem; color: var(--text-secondary); letter-spacing: 0.1em; margin-bottom: 1.5rem; }
.cover-subtitle { margin-top: 1.5rem; font-size: 1.1rem; color: var(--text-secondary); max-width: 600px; }
.case-one-liner-large { margin-top: 1.5rem; font-size: clamp(1rem, 2vw, 1.3rem); color: var(--text-secondary); max-width: 640px; line-height: 1.6; }
.conclusion-insight { margin-top: 1rem; }
.conclusion-prompt { margin-top: 2rem; font-size: 1.1rem; color: var(--text-secondary); }
.key-unknowns { margin-top: 2rem; padding: 1.25rem 1.5rem; background: var(--bg-secondary); border-left: 3px solid var(--accent); }
.unknowns-label { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.75rem; }
.key-unknowns ul { padding-left: 1.1rem; }
.key-unknowns li { font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 0.35rem; }

/* ── Method ── */
.method-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 2rem; margin-top: 1.5rem; }
.method-col h3 { font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.75rem; }
.method-col ul, .method-col ol { padding-left: 1.2rem; }
.method-col li { font-size: 0.9rem; margin-bottom: 0.4rem; color: var(--text-secondary); }
.method-col p { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.4rem; }
.method-note { font-size: 0.78rem; opacity: 0.65; font-style: italic; }

/* ── Overview ── */
.overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
.overview-card { background: var(--bg-secondary); padding: 1.5rem; border-left: 3px solid var(--accent); }
.overview-card h3 { font-family: var(--font-display); font-size: 1.4rem; margin: 0.5rem 0; }
.case-one-liner { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; }

/* ── Reframe ── */
.reframe-grid { display: flex; align-items: flex-start; gap: 1.5rem; margin: 1.5rem 0; flex-wrap: wrap; }
.reframe-col { flex: 1; min-width: 200px; padding: 1.25rem; background: var(--bg-secondary); }
.reframe-col.new { border-top: 3px solid var(--accent); }
.reframe-col.old { opacity: 0.6; }
.reframe-label { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.5rem; }
.reframe-arrow { font-size: 2rem; color: var(--accent); align-self: center; }
.rationale { margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-secondary); font-style: italic; }
.reframe-evidence { margin-top: 1rem; }

/* ── System ── */
.page-system { background: color-mix(in srgb, var(--bg-secondary) 60%, var(--bg-primary)); }
.touchpoints-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1.5rem; }
.touchpoint-card { background: var(--bg-primary); padding: 1rem 1.25rem; border-bottom: 2px solid var(--accent); min-width: 150px; flex: 1; }
.tp-icon { font-size: 1.2rem; margin-bottom: 0.4rem; }
.tp-name { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.25rem; }
.tp-role { font-size: 0.8rem; color: var(--text-secondary); }
.image-brief-note { margin-top: 1rem; padding: 0.75rem 1rem; background: color-mix(in srgb, var(--accent) 10%, transparent); border-left: 2px solid var(--accent); font-size: 0.82rem; color: var(--text-secondary); }

/* ── Proof (Why it lands) ── */
.page-proof { background: var(--bg-primary); }
.evidence-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1.5rem; }
.evidence-col { }
.evidence-label { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.75rem; }
.evidence-col ul { padding-left: 1.1rem; }
.evidence-col li { font-size: 0.9rem; margin-bottom: 0.5rem; line-height: 1.6; }
.evidence-col.prelim li { color: var(--text-secondary); font-style: italic; }

/* ── Takeaway (What to steal, scenarios) ── */
.page-takeaway { background: var(--bg-primary); }
.steal-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; margin-top: 1.5rem; }
.steal-card { background: var(--bg-secondary); padding: 1.5rem; border-top: 2px solid var(--accent); }
.steal-num { font-family: var(--font-display); font-size: 2rem; color: var(--accent); opacity: 0.4; margin-bottom: 0.5rem; }
.steal-method { font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }
.boundary-status { font-size: 0.72rem; display: block; margin-bottom: 0.75rem; }
.scenarios-block { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem; }
.scenario-row { display: flex; flex-direction: column; gap: 0.15rem; padding: 0.5rem 0.75rem; background: color-mix(in srgb, var(--bg-primary) 60%, transparent); border-left: 2px solid color-mix(in srgb, var(--accent) 40%, transparent); }
.scenario-condition { font-size: 0.78rem; color: var(--text-secondary); }
.scenario-step { font-size: 0.85rem; color: var(--text-primary); }
.scenario-outcome { font-size: 0.85rem; color: var(--text-secondary); font-style: italic; }

/* ── Recap ── */
.recap-table-wrap { overflow-x: auto; margin-top: 1.5rem; }
.recap-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.recap-table th, .recap-table td { padding: 0.75rem 1rem; text-align: left; vertical-align: top; border-bottom: 1px solid color-mix(in srgb, var(--text-secondary) 20%, transparent); }
.recap-table thead th { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); }
.recap-table tbody th { color: var(--text-secondary); font-weight: 400; white-space: nowrap; }
.recap-note { margin-top: 0.75rem; font-size: 0.75rem; color: var(--text-secondary); font-style: italic; }

/* ── Sources / Appendix ── */
.page-sources { background: var(--bg-secondary); }
.appendix-sub-heading { margin-top: 2rem; margin-bottom: 0.5rem; font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); }
.appendix-note { font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.75rem; }
.sources-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-top: 1.25rem; }
.sources-table th, .sources-table td { padding: 0.5rem 0.75rem; text-align: left; border-bottom: 1px solid color-mix(in srgb, var(--text-secondary) 15%, transparent); vertical-align: top; }
.sources-table th { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); }
.sources-table a { color: var(--text-secondary); }
.proxy-source-row td { color: var(--text-secondary); font-style: italic; }
.pending-table .pending-page { font-weight: 600; white-space: nowrap; }
.pending-table .pending-needed { font-size: 0.8rem; color: var(--text-secondary); }
.pending-table .pending-impact { font-size: 0.8rem; color: var(--accent); }

/* ── Animation (first 5 sections only) ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.page:nth-child(-n+6) .display   { animation: fadeUp 0.6s ease both; }
.page:nth-child(-n+6) .heading   { animation: fadeUp 0.6s 0.1s ease both; }
.page:nth-child(-n+6) .body-text { animation: fadeUp 0.6s 0.2s ease both; }
.page:nth-child(-n+6) .eyebrow   { animation: fadeUp 0.4s ease both; }
"""


# ─────────────────────────────────────────
# 8. Assemble HTML
# ─────────────────────────────────────────

def build_html(data: dict) -> str:
    meta       = data["meta"]
    visual     = data["visual"]
    cases      = data["cases"]
    conclusion = data.get("conclusion")
    mode       = meta.get("mode", "full")

    css_vars  = css_variables(visual["colors"], visual["fonts"])
    full_css  = BASE_CSS.replace("__CSS_VARS__", css_vars)
    gf_link   = google_fonts_link(visual["fonts"]["display"], visual["fonts"]["body"])

    body_parts = []
    body_parts.append(nav_html(meta, cases, conclusion))
    body_parts.append(section_cover(meta))

    if mode == "full":
        body_parts.append(section_method(mode))
        body_parts.append(section_overview(cases))

    for i, case in enumerate(cases, 1):
        pages = case.get("pages", {})
        body_parts.append(section_case_intro(case, i))
        if "real_problem"      in pages: body_parts.append(page_real_problem(pages["real_problem"], i))
        if "tension"           in pages: body_parts.append(page_tension(pages["tension"], i))
        if "strategic_reframe" in pages: body_parts.append(page_reframe(pages["strategic_reframe"], i))
        if "system"            in pages: body_parts.append(page_system(pages["system"], i))
        if "why_it_lands"      in pages: body_parts.append(page_why_it_lands(pages["why_it_lands"], i))
        if "what_to_steal"     in pages: body_parts.append(page_what_to_steal(pages["what_to_steal"], i))

    if mode == "full":
        body_parts.append(section_recap(cases))

    if conclusion and conclusion.get("cross_case_insight"):
        body_parts.append(section_conclusion(conclusion))

    body_parts.append(section_sources(cases))

    body_html = "\n".join(body_parts)
    title = meta.get("title", "Strategy Case Report")

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  {gf_link}
  <style>{full_css}</style>
</head>
<body>
{body_html}
</body>
</html>"""


# ─────────────────────────────────────────
# 9. Main
# ─────────────────────────────────────────

def main():
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)

    errors = validate(data)
    if errors:
        print("❌ Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"   · {e}", file=sys.stderr)
        sys.exit(1)

    html = build_html(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report built: {output_path}")
    print(f"   Cases: {len(data['cases'])}")
    print(f"   Mode:  {data['meta']['mode']}")
    print(f"   Size:  {output_path.stat().st_size // 1024} KB")
    print(f"   Schema: v2.6 (confirmed/estimated/unknown)")

    if args.open:
        import webbrowser
        webbrowser.open(output_path.resolve().as_uri())


if __name__ == "__main__":
    main()
