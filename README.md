# Strategy Case Report Skill

**版本：2.5 ｜ 更新：2026-03-23**

AI 主導全程的策略型案例報告生產 skill。人類只在兩個停止點提供 input，其餘由 AI 自主推進，輸出可直接用於策略判斷與提案決策的高品質 insight。

---

## 這個 skill 做什麼

不是整理案例，不是泛用型簡報生成。

AI 自主執行從案例搜尋、策略拆解、模型分析，到批判修正、視覺決策、最終輸出的完整流程。遇到資訊缺口，AI 先提案再繼續，不等人告訴它下一步。

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

**單一模式：AI 自主執行。**

使用者不需要在開始前選擇模式。AI 依任務性質自主判斷執行深度。

**兩個停止點：**
1. **啟動確認**：AI 完成 Intake 後，輸出一句話任務確認（含輸出媒介），等 OK 才往前
2. **Shortlist 確認**：AI 輸出案例名單 + 每案決策相關性 + 視角組合說明，確認後全速執行至最終輸出，不再停止

停止點 2 確認後，Phase 4 → 5 → 5.5 → 6 → 6.5 → 7 全速自主執行，批判內化不外顯，視覺系統自主決定不等確認。

---

## 輸出路徑

| 路徑 | 說明 | 觸發關鍵字 |
|------|------|-----------|
| A1 | A4 印刷報告 PDF | 「報告」「文件」「閱讀版」「A4」 |
| A2 | 16:9 簡報 PDF | 「簡報」「deck」「slide」「投影」「提案用」 |
| B | HTML artifact（互動版） | 「HTML」「artifact」「互動版」 |
| D | 純文字稿（Markdown） | 「純文字」「文字稿」「不要視覺」 |

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
| What to steal | 萃取可被借用的策略方法（附使用條件） |

整份報告結構：封面、方法頁、案例總覽頁、3 案 × 7 頁、對照 Recap 頁、結論頁、來源附錄。

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
│   ├── critique-scorecard.md         # 策略長批判問題庫（AI 內化執行，不外顯）
│   ├── deepdive-protocol.md          # Phase 5.5 三軸深挖追問協議
│   ├── model-library.md              # 模型庫、決策樹、HTML 圖表實作指引
│   ├── output-a4.md                  # A4 印刷報告版型規格（路徑 A1）
│   ├── output-slide.md               # 16:9 Slide PDF 版型規格（路徑 A2）
│   ├── phases-4-7.md                 # Phase 4–7 完整執行規格
│   ├── plain-text-format.md          # 純文字分析稿格式模板（路徑 D）
│   ├── report-data-schema.md         # HTML artifact 資料結構定義（路徑 B）
│   ├── visual-ref.md                 # 視覺系統決策規格與搜圖規則（AI 自主執行）
│   └── writing-rules.md              # 寫作規則、各頁功能定義、論證型配圖執行規則
└── scripts/
    └── build_report.py               # HTML 報告建構腳本（Claude Code 環境專屬）
```

---

## 品質機制

**AI 自主批判（Phase 5.5 + Phase 6）**
Phase 5 完成後，AI 執行三軸深挖追問（根源 / 矛盾命名 / 可執行性），直接覆寫第一輪分析。Phase 6 切換策略長視角執行防守型批判，直接修正輸出。批判執行摘要寫入來源附錄，不輸出 Scorecard，不等人審查。

**視覺系統自主決定（Phase 6.5）**
AI 依輸出媒介 + 案例調性自主決定色彩系統、字體配對、版型節奏，不輸出 Visual Brief，不等確認。決策記錄寫入來源附錄。

**缺口提案機制**
AI 遇到資訊不足時，不問開放式問題，而是說明判斷依據、提出具體方案、問「這樣對嗎」。使用者沉默視為同意（低風險決策），高風險決策（影響整體方向）必須明確確認。

**成功標準**
案例選得準、問題切得準、Insight 足夠深、模型用得準而不重、內容能扛質疑、每案都能被轉成提案素材、輸出媒介與使用情境匹配、版型完整無結構性空白。每條標準在 SKILL.md 都有具體操作定義。

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
| v2.3 | 2026-03-20 | SKILL.md 重構為 Progressive Disclosure 架構（669→268 行）；Phase 4–7 extracted 至 references/phases-4-7.md；A4 版型 extracted 至 references/output-a4.md；lazy-load 讀取規則明確化；Description 精簡至 75 字；Hard Rules 去重（Rules 1–4 已在原則章節）；新增 Gotcha：Phase 5.5 追問形式化 |
| v2.4 | 2026-03-21 | 新增 Rule 9（版型完整性）與對應 Gotcha；成功標準補充「版型完整，無結構性空白」；output-slide.md v2.1（Steal card 寫作原則、DarkFull-Insight 行動指向要求、元素字數上限表）|
| v2.5 | 2026-03-23 | 修正 8 項文件衝突與不一致（visual-ref.md 移除等確認邏輯、critique-scorecard.md 移除 v1.x 殘留與深挖重複內容、phases-4-7.md 純文字稿路徑統一、output-slide.md 補 Rule 9 自查 Checklist、phases-4-7.md Phase 5 What to steal 補字數上限）；report_schema.json 搬至 references/report-data-schema.md（Markdown 格式）；SKILL.md 讀取規則表補 Phase 7 路徑 B 條目；README 全面同步至 v2.5 |
