# Strategy Case Report Skill

**版本：2.6 ｜ 更新：2026-03-23**

AI 主導全程的策略型案例報告生產 skill。人類只在兩個停止點提供 input，其餘由 AI 自主推進，輸出可直接用於策略判斷與提案決策的高品質 insight。

---

## 這個 skill 做什麼

不是整理案例，不是泛用型簡報生成。

AI 自主執行從案例搜尋、扎根搜尋、策略拆解、模型分析，到批判修正、視覺決策、最終輸出的完整流程。遇到資訊缺口，AI 先提案再繼續，不等人告訴它下一步。深度分析的目標不是答完所有問題，而是把「能確認、能估算、無法判斷」切清楚。

**典型用途：**
- 市場趨勢月報
- 品牌案例觀察報告
- 策略型案例深拆報告
- 提案前置策略文件
- 決策前置研究

---

## 安裝方式

### Claude.ai（建議）
1. 下載 `strategy-case-report-v2.zip`
2. 前往 Claude.ai → Settings → Customize → Skills
3. 上傳 ZIP（必須包含資料夾本身在根目錄）
4. 安裝完成後，在對話中提到「案例報告」「策略 deck」「品牌案例分析」「幫我研究」等關鍵字即會自動觸發

### Claude Code
將資料夾放入專案的 `.claude/skills/` 目錄：
```
your-project/
└── .claude/
    └── skills/
        └── strategy-case-report/
            ├── SKILL.md
            ├── references/
            └── scripts/
```

---

## 執行模式

**單一模式：AI 自主執行。兩段 context 架構。**

v2.6 採用分段執行設計：分析 context（Phase 1–6）與輸出 context（Phase 6.5–7）分離，各自乾淨，避免長 context 造成的注意力衰減。

**兩個停止點：**
1. **啟動確認**：AI 完成 Intake 後，輸出一句話任務確認（含輸出媒介），等 OK 才往前
2. **Shortlist 確認**：AI 輸出案例名單 + 每案決策相關性 + 視角組合說明，確認後全速執行至截點

> **注意**：「全速執行」不覆蓋高風險決策清單。Phase 3.5 扎根搜尋若觸發替換案例條件（壓力層 + 張力層同時 unknown），AI 會停止並提案，等確認後繼續。

**截點（人類判斷）：**
Phase 6 批判完成後，AI 輸出截點 JSON（`report_data.json`）。使用者確認內容後，開啟新對話啟用 **report-renderer skill**，貼入 JSON 並指定輸出格式，啟動渲染。

**純文字稿（路徑 D）例外**：Phase 6 後直接輸出純文字稿，不輸出截點 JSON，不轉 report-renderer。

---

## 輸出路徑

strategy-case-report 負責分析段（Phase 1–6），輸出截點 JSON 後由 **report-renderer skill** 負責渲染段（Phase 6.5–7）。路徑 D 例外，由本 skill 直接輸出。

| 路徑 | 說明 | 觸發關鍵字 | 執行位置 |
|------|------|-----------|---------|
| A1 | A4 印刷報告 PDF | 「報告」「文件」「閱讀版」「A4」 | report-renderer |
| A2 | 16:9 簡報 PDF | 「簡報」「deck」「slide」「投影」「提案用」 | report-renderer |
| B | HTML artifact（互動版） | 「HTML」「artifact」「互動版」 | report-renderer |
| D | 純文字稿（Markdown） | 「純文字」「文字稿」「不要視覺」 | strategy-case-report 直接輸出 |

輸出媒介在 Phase 1 Intake 時必須明確確認，「PDF」不等於 A4，AI 會主動釐清。

---

## 報告結構

每個案例預設 7 頁：

| 頁面 | 功能 |
|------|------|
| Case in one line | 一句話定義案例價值 |
| The real problem | 定義品牌面對的真實市場問題 |
| The tension | 拆解 tension / insight，不停在表面觀察 |
| The strategic reframe | 說明品牌怎麼重做說法 |
| The system | 用 IMC / Journey 呈現執行系統 |
| Why it lands | 區分已被證明的事實與判讀 |
| What to steal | 萃取可被借用的策略方法（附條件區間） |

整份報告結構：封面、方法頁、案例總覽頁、3 案 × 7 頁、對照 Recap 頁、結論頁（含知識邊界聲明）、來源附錄（含待補資料區塊）。

---

## 分析框架

內建 12 個策略模型，按需配置，每案最多使用 3 個：

**核心模型庫（8 個）**
SWOT → TOWS、STP、JTBD、Brand Ladder、Brand Essence Pyramid、Golden Circle、Consumer Journey、CEPs

**條件式模型庫（4 個）**
4P、Binet & Field、COM-B、Kapferer Brand Identity Prism

所有模型以 HTML/CSS 製作圖表，不用圖片替代。

---

## 檔案結構

```
strategy-case-report/
├── SKILL.md                          # 主流程（角色定位、硬規則、Phase 1–3、Gotchas）
├── references/
│   ├── case-selection.md             # 案例篩選規則與 shortlist 評估標準
│   ├── critique-scorecard.md         # 策略長批判問題庫（含可知/不可知批判層）
│   ├── deepdive-protocol.md          # Phase 5.5 三軸深挖追問協議
│   ├── model-library.md              # 模型庫、決策樹、HTML 圖表實作指引
│   ├── phases-4-7.md                 # Phase 3.5–6 完整執行規格（含截點定義）
│   ├── plain-text-format.md          # 路徑 D 純文字稿輸出格式（Phase 6 確認後讀取）
│   ├── report-data-schema.md         # 截點 JSON 資料結構定義（三欄結構）⚠️ v2.6 欄位權威來源
│   ├── root-search.md                # Phase 3.5 扎根搜尋規格
│   └── writing-rules.md              # 寫作規則、各頁功能定義、論證型配圖規則
└── scripts/
    ├── build_report.py               # HTML 報告建構腳本（路徑 B，v2.6 對齊三欄 schema）
    └── report_schema.json            # JSON 結構參考範例（⚠️ 舊版示範，以 report-data-schema.md 為準）
```

視覺輸出相關規格（output-a4.md、output-slide.md、visual-ref.md）已移至 **report-renderer skill**，由該 skill 負責渲染。

---

## 品質機制

**扎根搜尋（Phase 3.5）**
Shortlist 確認後，AI 對每個入選案例執行三層扎根搜尋（壓力層 / 張力層 / 邊界層），每層先搜直接資料，找不到才改找代理變數。兩層都找不到資料時，AI 主動提案替換案例。扎根結果填入截點 JSON 的 `root_evidence` 區塊。

**三欄輸出格式（Phase 5）**
每個分析單元輸出三欄：`confirmed`（直接資料支撐）、`estimated`（代理推論，附假設條件）、`unknown`（無法判斷，說明需要什麼資料）。深度分析的價值不是答完所有問題，而是把可知與不可知切清楚。

**AI 自主批判（Phase 5.5 + Phase 6）**
Phase 5.5 追問目標是「把 estimated 層的假設說清楚，把 unknown 層的問題拆成可回答的子問題」。Phase 6 新增「可知與不可知是否切清楚」批判維度，防止把 estimated 寫成 confirmed 的幻覺。

**兩段 context 截點（strategy-case-report → report-renderer）**
Phase 6 結束後輸出截點 JSON，使用者確認後在 report-renderer skill 開啟新對話渲染。兩段各自 context 乾淨：分析 context 只跑搜尋和推論，輸出 context 只跑版型和渲染，互不干擾。

**成功標準**
案例選得準、問題切得準、Insight 足夠深、模型用得準而不重、可知與不可知切清楚、內容能扛質疑、每案都能被轉成提案素材、輸出媒介與使用情境匹配、版型完整無結構性空白。

---

## 適用環境

| 環境 | 支援狀況 |
|------|---------|
| Claude.ai（網頁 / App） | ✅ 完整支援 |
| Claude Code | ✅ 完整支援（含路徑 B build script）|
| Claude Desktop / Cowork | ✅ 完整支援 |

HTML artifact 輸出（路徑 B）需要 Claude.ai 或支援 artifact 渲染的環境。純文字稿（路徑 D）在所有環境均可使用。

---

## License

MIT

---

## 版本變更記錄

| 版本 | 日期 | 主要變更 |
|------|------|---------|
| v1.6 | — | 基礎版本 |
| v2.0 | 2026-03-20 | Phase 5.5 深挖層、Phase 6 防守型批判、Phase 6.5 Visual Brief、Autonomous Mode、Hard Rule 4、Phase 6/6.5 沉默執行 |
| v2.1 | 2026-03-20 | 輸出媒介判斷邏輯、Phase 7 A1/A2 兩條路徑、output-slide.md、Rule 5/6 |
| v2.2 | 2026-03-20 | Phase 2 視角組合判斷、Phase 3 視角角色欄位、Phase 4 Blueprint 規格、Phase 5 最低標準、writing-rules 內嵌、成功標準交叉引用 |
| v2.3 | 2026-03-20 | SKILL.md 重構為 Progressive Disclosure 架構；Phase 4–7 extracted；lazy-load 讀取規則 |
| v2.4 | 2026-03-21 | Rule 9（版型完整性）；output-slide.md v2.1 |
| v2.5 | 2026-03-23 | 修正 8 項文件衝突；report-data-schema.md 建立；README 全面同步 |
| v2.6 | 2026-03-23 | **架構重設**：新增 Phase 3.5 扎根搜尋（root-search.md）；Phase 5 三欄輸出格式（confirmed / estimated / unknown）；Phase 6 結束後輸出截點 JSON，分析與輸出拆為兩段 context；deepdive-protocol.md 追問目標重新定義；critique-scorecard.md 新增可知與不可知批判層；report-data-schema.md 全面改寫為三欄結構 + root_evidence |
| v2.6.1 | 2026-03-23 | **文件契約修正**：build_report.py 對齊 v2.6 三欄 schema（confirmed/estimated/unknown + root_evidence + scenarios[]）；report_schema.json 同步 v2.6 結構並加版本優先級聲明；SKILL.md 補路徑 D 讀取時機（plain-text-format.md）及全速執行 override 說明；phases-4-7.md 補 Phase 3.5 替換案例觸發條件的 override 聲明；report-data-schema.md 加優先級警示（以本文件為準，不得參考舊版 report_schema.json）；輸出路徑表新增「執行位置」欄說明分工 |
