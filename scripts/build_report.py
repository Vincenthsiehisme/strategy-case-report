#!/usr/bin/env python3
"""
build_report.py — Strategy Case Report HTML Deck Builder
Version: 1.0 | 2026-03-20

用途：
    讀取 report_data.json（由 Claude Phase 6.5 後填入），
    組裝成完整的 HTML artifact deck。

使用方式（由 Claude 呼叫）：
    python scripts/build_report.py --input report_data.json --output report.html

直接執行：
    python scripts/build_report.py --input report_data.json --output report.html [--open]

Dependencies: Python 3.8+，無需第三方套件
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
# 2. Validation
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
        pages = case.get("pages", {})
        for page in required_pages:
            if page not in pages:
                errors.append(f"{prefix}.pages.{page} is missing (required for {mode} mode)")

    return errors


# ─────────────────────────────────────────
# 3. HTML Fragments
# ─────────────────────────────────────────

def google_fonts_link(display: str, body: str) -> str:
    families = "+".join(
        f"{f.replace(' ', '+')}:wght@400;600;700"
        for f in dict.fromkeys([display, body])   # deduplicate, preserve order
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


def nav_html(meta: dict, cases: list, conclusion: dict | None) -> str:
    links = []
    links.append('<a href="#cover">封面</a>')
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


def pending_badge() -> str:
    return '<span class="badge-pending">初步判讀，待驗證</span>'


# ── Cover ──

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


# ── Method page ──

def section_method(mode: str) -> str:
    mode_label = "Full Mode（完整分析）" if mode == "full" else "Sprint Mode（精簡分析）"
    critique = "✅ 已通過策略長視角批判" if mode == "full" else "✅ 已通過 3 個核心批判問題"
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
      </div>
    </div>
  </div>
</section>"""


# ── Case Overview ──

def section_overview(cases: list) -> str:
    cards = ""
    for i, case in enumerate(cases, 1):
        cards += f"""
      <div class="overview-card">
        <p class="eyebrow">{case.get('industry','')} · {case.get('year','')}</p>
        <h3>{case.get('brand','')}</h3>
        <p class="case-one-liner">{case.get('case_in_one_line','')}</p>
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


# ── Individual Case Pages ──

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
    badge = pending_badge() if page.get("pending_verification") else ""
    return f"""
<section class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The Real Problem</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    {badge}
    <p class="body-text">{page.get('body','')}</p>
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_tension(page: dict, case_idx: int) -> str:
    badge = pending_badge() if page.get("pending_verification") else ""
    return f"""
<section class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The Tension</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    {badge}
    <p class="insight-sentence">{page.get('insight','')}</p>
    <p class="body-text">{page.get('body','')}</p>
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_reframe(page: dict, case_idx: int) -> str:
    badge = pending_badge() if page.get("pending_verification") else ""
    return f"""
<section class="page page-analysis">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The Strategic Reframe</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    {badge}
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
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_system(page: dict, case_idx: int) -> str:
    badge = pending_badge() if page.get("pending_verification") else ""
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

    return f"""
<section class="page page-system">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · The System</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    {badge}
    <div class="touchpoints-row">{tp_html}
    </div>
    {image_brief_html}
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_why_it_lands(page: dict, case_idx: int) -> str:
    badge = pending_badge() if page.get("pending_verification") else ""
    verified = "".join(f"<li>{f}</li>" for f in page.get("verified_facts", []))
    prelim   = "".join(f"<li>{f}</li>" for f in page.get("preliminary_reads", []))
    prelim_section = f"""
    <div class="evidence-col prelim">
      <p class="evidence-label">初步判讀（待驗證）</p>
      <ul>{prelim}</ul>
    </div>""" if prelim else ""

    return f"""
<section class="page page-proof">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · Why It Lands</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    {badge}
    <div class="evidence-grid">
      <div class="evidence-col verified">
        <p class="evidence-label">已驗證</p>
        <ul>{verified}</ul>
      </div>
      {prelim_section}
    </div>
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


def page_what_to_steal(page: dict, case_idx: int) -> str:
    badge = pending_badge() if page.get("pending_verification") else ""
    methods_html = ""
    for j, m in enumerate(page.get("methods", []), 1):
        methods_html += f"""
      <div class="steal-card">
        <p class="steal-num">0{j}</p>
        <p class="steal-method">{m.get('method','')}</p>
        <p class="steal-condition">適用：{m.get('condition','')}</p>
      </div>"""
    return f"""
<section class="page page-takeaway">
  <div class="page-inner">
    <p class="eyebrow">Case {case_idx} · What To Steal</p>
    <h2 class="heading">{page.get('headline','')}</h2>
    {badge}
    <div class="steal-grid">{methods_html}
    </div>
    <p class="page-footer">{page.get('footer','')}</p>
  </div>
</section>"""


# ── Recap ──

def section_recap(cases: list) -> str:
    headers = "<th></th>" + "".join(f"<th>{c.get('brand','')}</th>" for c in cases)
    dims = [
        ("真實問題", lambda c: c.get("pages", {}).get("real_problem", {}).get("headline", "—")),
        ("Tension 核心", lambda c: c.get("pages", {}).get("tension", {}).get("insight", "—")),
        ("Reframe 方向", lambda c: c.get("pages", {}).get("strategic_reframe", {}).get("new_frame", "—")),
        ("可借用方法", lambda c: (c.get("pages", {}).get("what_to_steal", {}).get("methods") or [{}])[0].get("method", "—")),
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
  </div>
</section>"""


# ── Conclusion ──

def section_conclusion(conclusion: dict) -> str:
    if not conclusion or not conclusion.get("cross_case_insight"):
        return ""
    return f"""
<section id="conclusion" class="page page-statement">
  <div class="conclusion-content">
    <p class="eyebrow">Conclusion</p>
    <p class="display conclusion-insight">{conclusion['cross_case_insight']}</p>
    <p class="conclusion-prompt">{conclusion.get('action_prompt','')}</p>
  </div>
</section>"""


# ── Sources ──

def section_sources(cases: list) -> str:
    rows = ""
    for case in cases:
        for s in case.get("sources", []):
            type_label = {"official": "官方", "major_media": "主流媒體",
                          "secondary_media": "次級媒體"}.get(s.get("type",""), s.get("type",""))
            src = s.get("source", "")
            src_display = f'<a href="{src}" target="_blank">{src}</a>' if src.startswith("http") else src
            rows += f"""
      <tr>
        <td>{case.get('brand','')}</td>
        <td>{s.get('label','')}</td>
        <td>{src_display}</td>
        <td>{type_label}</td>
      </tr>"""
    return f"""
<section id="sources" class="page page-sources">
  <div class="page-inner">
    <p class="eyebrow">Appendix</p>
    <h2 class="heading">來源附錄</h2>
    <table class="sources-table">
      <thead><tr><th>案例</th><th>標注</th><th>來源</th><th>類型</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>"""


# ─────────────────────────────────────────
# 4. CSS
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
  display: inline-block; font-size: 0.7rem; padding: 0.2rem 0.6rem;
  background: color-mix(in srgb, var(--accent) 15%, transparent);
  color: var(--accent); border: 1px solid var(--accent);
  border-radius: 2px; letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

/* ── Statement pages ── */
.page-statement { background: var(--bg-primary); }
.cover-content, .case-intro-content, .conclusion-content {
  max-width: 800px;
}
.cover-date { font-size: 0.75rem; color: var(--text-secondary); letter-spacing: 0.1em; margin-bottom: 1.5rem; }
.cover-subtitle { margin-top: 1.5rem; font-size: 1.1rem; color: var(--text-secondary); max-width: 600px; }
.case-one-liner-large { margin-top: 1.5rem; font-size: clamp(1rem, 2vw, 1.3rem); color: var(--text-secondary); max-width: 640px; line-height: 1.6; }
.conclusion-insight { margin-top: 1rem; }
.conclusion-prompt { margin-top: 2rem; font-size: 1.1rem; color: var(--text-secondary); }

/* ── Method ── */
.method-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 2rem; margin-top: 1.5rem; }
.method-col h3 { font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.75rem; }
.method-col ul, .method-col ol { padding-left: 1.2rem; }
.method-col li { font-size: 0.9rem; margin-bottom: 0.4rem; color: var(--text-secondary); }
.method-col p { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.4rem; }

/* ── Overview ── */
.overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
.overview-card {
  background: var(--bg-secondary); padding: 1.5rem;
  border-left: 3px solid var(--accent);
}
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

/* ── System ── */
.page-system { background: color-mix(in srgb, var(--bg-secondary) 60%, var(--bg-primary)); }
.touchpoints-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1.5rem; }
.touchpoint-card {
  background: var(--bg-primary); padding: 1rem 1.25rem;
  border-bottom: 2px solid var(--accent); min-width: 150px; flex: 1;
}
.tp-icon { font-size: 1.2rem; margin-bottom: 0.4rem; }
.tp-name { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.25rem; }
.tp-role { font-size: 0.8rem; color: var(--text-secondary); }
.image-brief-note {
  margin-top: 1rem; padding: 0.75rem 1rem;
  background: color-mix(in srgb, var(--accent) 10%, transparent);
  border-left: 2px solid var(--accent);
  font-size: 0.82rem; color: var(--text-secondary);
}

/* ── Proof ── */
.page-proof { background: var(--bg-primary); }
.evidence-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1.5rem; }
.evidence-col { }
.evidence-label { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.75rem; }
.evidence-col ul { padding-left: 1.1rem; }
.evidence-col li { font-size: 0.9rem; margin-bottom: 0.5rem; line-height: 1.6; }
.evidence-col.prelim li { color: var(--text-secondary); font-style: italic; }

/* ── Takeaway ── */
.page-takeaway { background: var(--bg-primary); }
.steal-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-top: 1.5rem; }
.steal-card {
  background: var(--bg-secondary); padding: 1.5rem;
  border-top: 2px solid var(--accent);
}
.steal-num { font-family: var(--font-display); font-size: 2rem; color: var(--accent); opacity: 0.4; margin-bottom: 0.5rem; }
.steal-method { font-size: 1rem; font-weight: 600; margin-bottom: 0.75rem; }
.steal-condition { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6; }

/* ── Recap ── */
.recap-table-wrap { overflow-x: auto; margin-top: 1.5rem; }
.recap-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.recap-table th, .recap-table td { padding: 0.75rem 1rem; text-align: left; vertical-align: top; border-bottom: 1px solid color-mix(in srgb, var(--text-secondary) 20%, transparent); }
.recap-table thead th { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); }
.recap-table tbody th { color: var(--text-secondary); font-weight: 400; white-space: nowrap; }

/* ── Sources ── */
.page-sources { background: var(--bg-secondary); }
.sources-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-top: 1.25rem; }
.sources-table th, .sources-table td { padding: 0.5rem 0.75rem; text-align: left; border-bottom: 1px solid color-mix(in srgb, var(--text-secondary) 15%, transparent); }
.sources-table th { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); }
.sources-table a { color: var(--text-secondary); }

/* ── Animation (first 5 sections only) ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.page:nth-child(-n+6) .display    { animation: fadeUp 0.6s ease both; }
.page:nth-child(-n+6) .heading    { animation: fadeUp 0.6s 0.1s ease both; }
.page:nth-child(-n+6) .body-text  { animation: fadeUp 0.6s 0.2s ease both; }
.page:nth-child(-n+6) .eyebrow    { animation: fadeUp 0.4s ease both; }
"""


# ─────────────────────────────────────────
# 5. Assemble HTML
# ─────────────────────────────────────────

def build_html(data: dict) -> str:
    meta      = data["meta"]
    visual    = data["visual"]
    cases     = data["cases"]
    conclusion = data.get("conclusion")
    mode      = meta.get("mode", "full")

    css_vars  = css_variables(visual["colors"], visual["fonts"])
    full_css  = BASE_CSS.replace("__CSS_VARS__", css_vars)
    gf_link   = google_fonts_link(visual["fonts"]["display"], visual["fonts"]["body"])

    # Build body sections
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
# 6. Main
# ─────────────────────────────────────────

def main():
    args = parse_args()

    # Load
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

    # Validate
    errors = validate(data)
    if errors:
        print("❌ Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"   · {e}", file=sys.stderr)
        sys.exit(1)

    # Build
    html = build_html(data)

    # Write
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report built: {output_path}")
    print(f"   Cases: {len(data['cases'])}")
    print(f"   Mode:  {data['meta']['mode']}")
    print(f"   Size:  {output_path.stat().st_size // 1024} KB")

    if args.open:
        import webbrowser
        webbrowser.open(output_path.resolve().as_uri())


if __name__ == "__main__":
    main()
