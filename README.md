# Strategy Case Report Skill

**版本：1.6 ｜ 更新：2026-03-20**

一份用於 Claude 的策略型案例報告生產 skill，輸出可供策略判斷與提案借用的 strategy learning asset。

---

## 這個 skill 做什麼

不是整理案例，不是泛用型簡報生成。

它建立一套可複製的策略報告生產流程：從案例搜尋、策略拆解、模型分析，到策略長視角的高壓批判，最終輸出有設計感的 HTML artifact deck 或純文字分析稿。

**典型用途：**
- 市場趨勢月報
- 品牌案例觀察報告
- 策略型案例深拆報告
- 提案前置策略文件
- 內部策略學習 deck

---

## 安裝方式

### Claude.ai（建議）
1. 下載 `strategy-case-report.skill`（或直接 clone 此 repo 後壓縮資料夾為 ZIP）
2. 前往 Claude.ai → Settings → Customize → Skills
3. 上傳 `.skill` 檔（ZIP 必須包含資料夾本身在根目錄）
4. 安裝完成後，在對話中提到「案例報告」「策略 deck」「品牌案例分析」等關鍵字即會自動觸發

### Claude Code
將資料夾放入專案的 `.claude/skills/` 目錄：
```
your-project/
└── .claude/
    └── skills/
        └── strategy-case-report/
            ├── SKILL.md
            └── references/
```

---

## 執行模式

### Full Mode（完整版）
適合月報、重要提案前置文件、對外使用的策略 deck。

- 每案 7 頁完整分析
- 強制策略長批判輪次
- 輸出 HTML artifact deck
- 預計 12–18 輪對話

### Sprint Mode（壓縮版）
適合內部快速學習 deck、個人工作加速。

- 每案 4–5 頁重點分析
- 精簡批判（3 個核心問題）
- 輸出 HTML artifact deck 或純文字分析稿
- 預計 4–10 輪對話（依輸出形式）

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
├── SKILL.md                          # 主流程（角色定位、硬規則、Phase 1–7）
└── references/
    ├── case-selection.md             # 案例篩選規則與 shortlist 評估標準
    ├── critique-scorecard.md         # 策略長批判問題庫與 Scorecard 格式
    ├── model-library.md              # 模型庫、決策樹、HTML 圖表實作指引
    ├── plain-text-format.md          # 純文字分析稿格式模板
    ├── visual-ref.md                 # Visual Brief 執行流程與視覺系統決策
    └── writing-rules.md              # 寫作規則、各頁功能定義、論證型配圖執行規則
```

---

## 品質機制

**Approval Gate**：每個關鍵節點（Plan 批准、Shortlist 確認、藍圖確認、批判確認、Visual Brief 確認）都需要使用者明確同意才能繼續，AI 不自動進入下一步。

**策略長批判（Full Mode 強制）**：第一輪分析完成後，切換到策略長視角，逐案高壓挑戰。輸出 Critique Scorecard 給使用者確認，有 ❌ 必須修正後才能進入輸出。

**成功標準（每條都有具體定義）**：案例選得準、問題切得準、Insight 足夠深、模型用得準而不重、內容能扛質疑、每案都能被轉成提案素材。

---

## 適用環境

| 環境 | 支援狀況 |
|------|---------|
| Claude.ai（網頁 / App） | ✅ 完整支援 |
| Claude Code | ✅ 完整支援 |
| Claude Desktop / Cowork | ✅ 完整支援 |

HTML artifact 輸出需要 Claude.ai 或支援 artifact 渲染的環境。純文字稿輸出在所有環境均可使用。

---

## License

MIT
