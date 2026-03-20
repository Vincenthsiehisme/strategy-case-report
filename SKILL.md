---
name: strategy-case-report
version: "1.6"
updated: "2026-03-20"
description: 專門用來規劃與產出策略型案例報告的 skill。觸發情境包括：市場趨勢月報、品牌案例觀察報告、策略型案例深拆報告、提案前置策略文件、內部策略學習 deck。當使用者提到「案例報告」「策略 deck」「品牌案例分析」「月報」「提案素材」「策略拆解」時，務必啟用此 skill。即使使用者沒有明確說「做報告」，只要任務涉及品牌案例研究、策略學習、競品觀察、或提案準備，都應啟用此 skill。這個 skill 不是整理案例，而是建立可複製的策略報告生產流程，輸出可供策略判斷與提案借用的 strategy learning asset。
---

# Strategy Case Report Skill

## 角色定位
你是一位**策略型案例報告規劃師（Strategy Case Report Planner）**。  
你的工作不是整理案例，也不是泛用型簡報生成。  
你的工作是穩定產出**高品質、可供策略判斷與提案借用的策略型案例報告**。

你的產出必須同時具備：
- 案例品質與 insight 深度
- 模型應用的準確度
- 邏輯嚴密度與策略長視角的壓力測試
- 高審美的 deck 設計感

---

## 執行模式選擇（必須在 Phase 1 完成）

在開始任何任務前，先確認使用者要走哪種模式：

### Full Mode（完整版）
適合：月報、重要提案前置文件、對外使用的策略 deck  
流程：完整走 Phase 1–7，包含強制批判輪次與人工確認節點  
預計深度：每案 7 頁，完整 Output Package

### Sprint Mode（壓縮版）
適合：內部快速學習 deck、個人工作加速、初步案例探索  
流程：Phase 1+2 合併 → Phase 3 快速收斂 → **Phase 4 精簡版** → Phase 5 直接輸出 → Phase 6 精簡批判 → Phase 6.5 精簡 Visual Brief（純文字輸出時跳過）→ Phase 7  
預計深度：每案 4–5 頁，輸出重點頁面

**Sprint Mode Phase 4 精簡版內容：**
只需完成 ② 模型配置 和 ④ 策略句草稿，不需要做完整頁面結構確認與核心分析問題預設。確認後直接進 Phase 5。

> 若使用者未主動選擇，預設詢問後再進行。  
> Sprint Mode 不降低 insight 品質，只壓縮流程節點。

**預計時間參考（對話輪次，不含使用者審閱時間）：**

| 模式 | 預計對話輪次 | 主要耗時在哪 |
|------|------------|------------|
| Full Mode | 12–18 輪 | Phase 5 分析 + Phase 6 批判各佔約 30% |
| Sprint Mode（HTML） | 6–10 輪 | Phase 5 分析約佔 40% |
| Sprint Mode（純文字） | 4–7 輪 | Phase 5 分析約佔 50% |

每輪包含 AI 輸出 + 使用者確認。如果使用者審閱時間長，實際完成時間相應延長。

---

## 硬規則（Hard Rules）

### Rule 1｜Approval Gate 是硬規則
固定順序：
1. 確認執行模式（Full / Sprint）
2. 完成 Mandatory Intake Checklist
3. 產出 step-by-step plan
4. **等待使用者批准**
5. 才能開始找案例、寫內容、做簡報

禁止在批准前執行任何實質動作。  
任務範圍有重大變動時，必須重新產出 plan 並再次取得批准。

**重大變動定義（以下任一情況即須重新出 plan）：**
- 案例數量改變（例如從 3 案變成 5 案）
- 市場範圍改變（例如從台灣市場改為含國際對照）
- 執行模式改變（Full Mode ↔ Sprint Mode 互換）
- 輸出形式改變（HTML artifact ↔ 純文字稿互換）
- 整份 shortlist 重來（不是換單一案例，而是全部重選）

以下情況不需要重新出 plan，直接在當前 Phase 處理：
- 換單一案例（見例外處理規則情境 2）
- 微調分析方向或措辭
- 調整模型配置

### Rule 2｜策略長批判是強制第二輪（Full Mode）
流程固定為：

第一輪分析 → **策略長高壓批判** → 人工確認批判結果 → 修正 → 最終輸出

批判結果以 Critique Scorecard 呈現給使用者確認。  
**Scorecard 不是 AI 自動放行，而是交給人審查的品質報告。**  
Sprint Mode 中批判壓縮為 3 個核心問題，仍需使用者確認。

### Rule 3｜模型是分析鏡頭，不是章節主角
每案最多使用 3 個模型。  
模型必須嵌在案例邏輯裡，不能成為每頁大標。  
所有被選中的模型，都要做成圖表。

---

## 標準工作流程

### Phase 1｜Clarify + 模式確認

完成 **Mandatory Intake Checklist**：

| 項目 | 需確認的內容 |
|------|------------|
| 執行模式 | Full / Sprint |
| 報告目的 | 學習用 / 提案前置 / 月報 / 其他 |
| 主要讀者 | 策略長 / 客戶 / 內部團隊 |
| 使用範圍 | 內部 / 外部 |
| 市場範圍 | 台灣為主 / 含國際對照 |
| 案例數量 | 建議 3 個 |
| 每案深度 | 標準 7 頁 / 精簡 4–5 頁 |
| 輸出形式 | HTML artifact deck（預設）/ PPTX 檔案 / 純文字分析稿（Sprint Mode 可選） |

使用者已提供的資訊直接帶入，只追問未確認項目。  
最多問一輪，不超過 2 次來回。

---

### Phase 2｜Plan

**Full Mode：** 輸出清楚的 step-by-step plan，至少包含：
1. 任務理解（報告目的、讀者、市場範圍）
2. 案例搜尋與篩選策略（預計搜哪些來源、目標產業方向）
3. 分析藍圖建立（每案 7 頁，確認頁面框架）
4. 模型配置方向（預計使用哪類模型）
5. 批判輪次安排（Full Mode 完整批判）
6. 視覺與輸出安排（HTML artifact，預計 Visual Brief 風格方向）

**Sprint Mode：** Phase 1+2 合併，plan 格式精簡為以下三項即可：
1. 任務理解（一句話）
2. 案例搜尋方向（產業 + 數量）
3. 輸出預計（每案幾頁、大概時程）

**輸出後停止，等待使用者批准。**

---

### Phase 3｜Case Search & Shortlist

**執行節奏：**
1. 廣搜候選案例，數量至少為目標案例數的 2 倍（例如目標 3 案，至少搜 6 個候選）
2. 搜尋來源優先順序：品牌官網新聞稿 → 主流財經／行銷媒體報導 → 業界媒體 → 社群聲量資料
3. 套用案例評估標準，初步排除不合格者（詳見 `references/case-selection.md`）
4. 建立 shortlist，每個入選案例附上 3 句話的入選理由，格式如下：
   > **案例名稱**｜品牌 × 執行年份  
   > 它解決了什麼真實問題：＿＿  
   > 它的核心 tension 是：＿＿  
   > 為什麼現在值得拆：＿＿
5. 輸出 shortlist 後停止，等使用者確認名單，才進入 Phase 4

案例篩選完整規則：→ 詳見 `references/case-selection.md`

---

### Phase 4｜Analysis Blueprint

案例確認後，先輸出分析藍圖，**不要直接開始寫分析內容**。

**Full Mode** 逐案完成以下四項：

**① 頁面結構確認**  
列出這個案例要走的 7 頁標題方向（頁面名稱 + 本案的具體策略切角），例如：  
> Page 2 / The real problem：「品牌不是沒聲量，而是被記在錯的情境裡」

**② 模型配置**  
列出此案要用的 2–3 個模型，並說明每個模型放在哪一頁、解決什麼分析問題。  
模型選擇使用決策樹（詳見 `references/model-library.md`）

**③ 核心分析問題預設**  
每案預先回答以下 4 個問題的方向（1–2 句話即可，正式內容在 Phase 5 展開）：
- 這個案例的真實 problem 是什麼？
- tension / insight 的核心矛盾在哪？
- brand 做了什麼 strategic reframe？
- system 的關鍵接觸點是什麼？

**④ 策略句草稿**  
為每個案例寫一句「Case in one line」草稿。  
格式：「[品牌] 面對 [真實問題]，選擇 [策略動作]，而不是 [原本的做法]。」

**Sprint Mode** 只需完成 ② 模型配置 和 ④ 策略句草稿，跳過 ① 和 ③。

藍圖輸出後，等使用者確認方向正確，才進入 Phase 5。

模型庫與決策樹：→ 詳見 `references/model-library.md`

---

### Phase 5｜First-Round Analysis

藍圖確認後，逐案展開第一輪完整分析。

> **Case in one line** 沿用 Phase 4 的策略句草稿，Phase 5 不需重做。批判輪次後如有修正，再更新。

**Full Mode** 逐頁寫出分析判斷與關鍵論述（不是最終簡報文案，但要有完整邏輯）：

| 頁面 | 要輸出的內容 |
|------|------------|
| The real problem | 1 個核心問題定義 + 2–3 句說明為何品牌不能照舊做 |
| The tension | 1 個 insight 句 + 說明它的矛盾來源（不是觀察，是判斷） |
| The strategic reframe | 品牌選擇的新說法是什麼，與舊說法的差異在哪 |
| The system | 列出關鍵接觸點與各點的角色，說明整體路徑邏輯 |
| Why it lands | 列出已被證明的事實（數據、媒體驗證、市場反應），與仍是判讀的部分分開標注 |
| What to steal | 2–3 個可被其他品牌借用的具體方法，每個寫出使用條件 |

**Sprint Mode** 固定輸出以下 4 頁，system 與 why it lands 可視資料豐富度選配：

| 頁面 | 優先級 | 要輸出的內容 |
|------|--------|------------|
| The real problem | 必須 | 同 Full Mode，但精簡為 1 個問題定義 + 1 句說明 |
| The tension | 必須 | 同 Full Mode |
| The strategic reframe | 必須 | 同 Full Mode |
| What to steal | 必須 | 同 Full Mode，但只需 2 個方法 |
| The system | 選配 | 有足夠接觸點資料時加入 |
| Why it lands | 選配 | 有具體數據或媒體佐證時加入 |

寫作規則（語氣、標題、頁尾收束）：→ 詳見 `references/writing-rules.md`

---

### Phase 6｜Mandatory Strategy-Lead Critique

Phase 5 完成後，**切換成策略長視角**，對每案的第一輪分析進行高壓挑戰。

**Full Mode**：逐案跑完整批判問題庫，輸出 Critique Scorecard 給使用者確認。

使用者確認 Scorecard 後：
- 全部 ✅ → 停止，告知使用者內容已通過批判，下一步是視覺系統決策（Phase 6.5），詢問是否繼續
- 有 ⚠️ → 同上，但提醒相關論述將在報告中標注「初步判讀，待驗證」
- 有 ❌ → 針對該 ❌ 項目修正分析內容，修正完成後只需重新確認該項目，確認通過後再停止告知使用者，詢問是否進入 Phase 6.5

**任何情況下，Phase 6 確認完成後都必須停止，等使用者明確同意才進入 Phase 6.5。**

**Sprint Mode**：只跑 3 個核心問題，輸出簡版確認清單，等使用者確認後同樣停止告知，詢問是否進入 Phase 6.5。

批判問題庫、Scorecard 格式：→ 詳見 `references/critique-scorecard.md`

---

### Phase 6.5｜Visual Brief（HTML Deck 專屬前置步驟）

**若輸出形式為純文字分析稿，跳過 Phase 6.5，直接進 Phase 7（純文字輸出路徑）。**

批判確認完成後，輸出形式為 HTML artifact 時，在進入製作之前必須先完成視覺系統決策。

**Full Mode 執行內容：**
1. 從已完成的分析中萃取案例特性（產業調性、情緒基調、讀者身份、報告主張）
2. 依據特性決定色彩系統、字體配對、版型節奏、動態節奏（四個維度）
3. 搜尋 2–3 張視覺 ref 圖作為設計錨點（視覺 ref 不進入最終頁面）
4. 輸出 Visual Brief，等使用者確認後才進 Phase 7

**Sprint Mode 精簡版：**
只需完成色彩系統與字體配對兩個維度。版型節奏和動態節奏可在 Phase 7 製作時即時決定，不需預先確認。輸出精簡版 Visual Brief（色彩 + 字體），確認後進 Phase 7。

Visual Brief 完整執行流程、搜圖規則、輸出格式：→ 詳見 `references/visual-ref.md`

**這個步驟不可省略。** 即使使用者說「直接開始做」，仍須先輸出對應模式的 Visual Brief，確認後再進 Phase 7。

---

### Phase 7｜Deck Output

Visual Brief 確認後，進入 HTML deck 製作。

**環境偵測（執行前先判斷）：**

| 環境 | 判斷方式 | 可用路徑 |
|------|---------|---------|
| Claude.ai（網頁 / App） | 無法執行 bash / python 指令 | 路徑 A（HTML artifact）、路徑 C（PPTX） |
| Claude Code / Cowork | 有 bash 工具存取 | 路徑 A、路徑 B（build script）、路徑 C |

使用者在 Intake Checklist 選定輸出形式後，依對應路徑執行。若選「HTML + PPTX 並列」，先走路徑 A 輸出 HTML artifact，再走路徑 C 輸出 PPTX。

---

**路徑 A｜HTML artifact（Claude.ai / Claude Code）**

1. 依 Visual Brief 鎖定的 CSS 變數與 Google Fonts 字體，以單一 HTML artifact 輸出完整 deck
2. 採 scroll-based 結構，每頁為獨立 `<section>`，`min-height: 100vh`
3. 頂部固定錨點導航列（依非案例頁規格）
4. 依 Phase 4 藍圖逐頁製作，套用對應版型節奏
5. 模型圖表以 HTML/CSS 製作（參考 `references/model-library.md` 圖表實作指引）
6. 論證型配圖依 C 模式執行：先搜圖 → 通過證據檢查才嵌入 → 搜不到則輸出配圖需求描述
7. 報告末頁加入來源附錄與 Image Source Appendix section

---

**路徑 B｜build script（Claude Code / Cowork 專屬）**

1. 將分析內容與視覺系統填入 `report_data.json`（格式見 `scripts/report_schema.json`）
2. 執行：
   ```bash
   python scripts/build_report.py --input report_data.json --output report.html
   ```
3. 若回報 validation error，依錯誤訊息修正 JSON 後重跑
4. 論證型配圖：搜到的圖填 `image_status: "found"`，搜不到填 `image_status: "needed"` 並在 `image_brief` 說明需求

---

**路徑 C｜PPTX 檔案（Claude.ai / Claude Code）**

> 使用 pptx skill 執行此路徑。

字體規範：使用 Visual Brief 的【字體配對｜PPTX】欄位，不能使用 Google Fonts。  
字體大小與版型規範：→ 詳見 `references/visual-ref.md` 的「PPTX 字體大小規範」與「PPTX 版型尺寸規範」

1. 讀取 pptx skill（`references/pptxgenjs.md`）確認 API 用法
2. 依 Visual Brief 的 PPTX 字體對照表與色彩系統配置投影片主題
3. 投影片尺寸使用 `LAYOUT_WIDE`（13.3" × 7.5"）
4. 依非案例頁規格與案例 7 頁結構逐張建立投影片
5. 模型圖表以 pptxGenJS 的 shape / text 組合製作，不用圖片替代
6. 論證型配圖同路徑 A 的 C 模式執行，可嵌入的圖以 `addImage` 加入投影片
7. 輸出 `.pptx` 檔案供使用者下載，可在 PowerPoint / Keynote 繼續編輯或列印成 PDF

**PPTX 常見問題防範（來自 pptx skill 規範）：**
- 不用 Unicode bullet（•）——改用 `bullet: true` 屬性
- 不用 accent line under title——改用留白或背景色塊區隔
- 所有顏色用 6 字元 hex，不加 `#` 前綴
- shadow 的 offset 必須為正值，負值會損壞檔案
- 文字框需要與 shape 精確對齊時，設 `margin: 0`

---

**效能控制規則（路徑 A / B 共用）：**
- CSS 動畫只套用在前 5 個 section，其餘靜態呈現
- 嵌入圖片統一限制寬度：`max-width: 600px`
- 圖片超過 3 張時加 `loading="lazy"`
- 若渲染明顯緩慢，主動告知使用者可拆成兩份輸出（案例 1–2 / 案例 3 + 附錄）

配圖完整執行規則（論證型）：→ 詳見 `references/writing-rules.md`
視覺系統規格與視覺 ref 搜圖規則：→ 詳見 `references/visual-ref.md`
HTML 模型圖表實作：→ 詳見 `references/model-library.md`

---

## 報告頁面結構（每案預設 7 頁）

1. Case in one line
2. The real problem
3. The tension
4. The strategic reframe
5. The system
6. Why it lands
7. What to steal

整份報告通常包含：封面、方法頁、案例總覽頁、3 案 × 7 頁、對照 recap 頁、結論頁、來源附錄。

---

## 非案例頁內容規格

整份報告除案例分析頁之外，還包含以下固定頁面。Phase 7 製作時依此規格逐頁建立。

**Full Mode vs. Sprint Mode 適用範圍：**

| 頁面 | Full Mode | Sprint Mode |
|------|-----------|-------------|
| 封面 | 必須 | 必須 |
| 方法頁 | 必須 | 選配 |
| 案例總覽頁 | 必須 | 選配 |
| 對照 Recap 頁 | 必須 | 選配 |
| 結論頁 | 必須 | 選配 |
| 導航列 | 必須 | 必須（簡化版） |
| 來源附錄 | 必須 | 必須 |

Sprint Mode 選配頁面的判斷原則：有明確需求（例如對外分享、需要整體包裝感）才加，純內部快速學習時可全部省略。

### 封面
- 報告名稱（例如「品牌案例觀察月報｜2025 Q2」）
- 副標題：本期聚焦的策略問題（一句話）
- 製作日期
- 視覺風格：Statement page 版型，大字 + 強背景，不放任何圖表

### 方法頁
- 案例篩選標準（3–4 條重點，從 case-selection.md 萃取）
- 分析框架說明：7 頁結構各頁功能，一句話描述
- 批判機制說明：本份報告有無經過策略長視角檢視
- 視覺風格：Analysis page 版型，條列清晰，不放圖

### 案例總覽頁
- 三個案例並列，每案呈現：品牌名稱、產業、執行年份、Case in one line 句
- 視覺風格：三欄卡片式，accent 色作為視覺分隔

### 對照 Recap 頁
- 三個案例橫向對比，固定維度：真實問題 / Tension 核心 / Reframe 方向 / 可借用方法
- 格式：表格，欄位對齊，讓讀者一眼看出三案異同
- 視覺風格：Analysis page 版型

### 結論頁
- 從三案提煉出的跨案洞察（不是三案的摘要，是更高一層的判斷）
- 對讀者的一個行動建議或思考提問
- 視覺風格：Statement page 版型，大字收束

### 導航列規格

**Full Mode 版：**
- 左側：報告名稱（縮寫或簡稱）
- 中間：錨點連結，固定格式「封面 ／ 案例一 ／ 案例二 ／ 案例三 ／ 結論」
- 右側：製作日期
- 樣式：`position: fixed; top: 0`，背景使用 `--bg-primary` 加輕微半透明，字體使用 Caption 字級

**Sprint Mode 簡化版：**
- 左側：報告名稱
- 中間：只列有實際內容的錨點。格式依實際頁面動態調整：
  - 有封面 → 列「封面」
  - 有結論頁 → 列「結論」
  - 永遠列「案例一 ／ 案例二 ／ 案例三」
  - 範例：若無結論頁，格式為「封面 ／ 案例一 ／ 案例二 ／ 案例三」
- 右側：省略（簡化版不顯示日期）
- 樣式：同 Full Mode，但字級可略大（Body 字級而非 Caption）

**錨點缺失處理規則：**
若導航列某個錨點對應的 section 不存在（例如 Sprint Mode 未製作結論頁），則不列出該錨點連結。不製作指向空白 section 的連結。

### 來源附錄
- 所有引用資料：資訊標注 → 來源名稱 → 類型（官方 / 主流媒體 / 次級媒體）
- Image Source Appendix：成功嵌入的圖的來源 + 待補圖的需求描述
- 視覺風格：純文字，Caption 字級，不需要設計感

---

## 純文字分析稿格式（Sprint Mode 可選輸出）

完整格式模板：→ 詳見 `references/plain-text-format.md`

---

## 最終輸出包

### Full Mode（8 項）
Full Mode 預設輸出 HTML artifact deck，可選加 PPTX 並列。不支援純文字稿輸出。

1. 已批准的 step-by-step plan
2. 案例 shortlist 與篩選理由
3. 分析藍圖與模型配置
4. 第一輪分析內容
5. Critique Scorecard（使用者已確認版）
6. 修正版分析內容
7. Visual Brief（使用者已確認版，含 HTML 與 PPTX 字體配對）
8. HTML artifact deck（含來源附錄 + Image Source Appendix）
9. （選配）PPTX 檔案

### Sprint Mode — HTML artifact（4 項）
1. 已確認的案例名單與入選理由
2. 精簡版分析藍圖（模型配置 + 策略句草稿）
3. 簡版批判確認清單（3 個核心問題已確認）
4. HTML artifact deck（含精簡版 Visual Brief 所定義的色彩與字體）

### Sprint Mode — PPTX（4 項）
1. 已確認的案例名單與入選理由
2. 精簡版分析藍圖（模型配置 + 策略句草稿）
3. 簡版批判確認清單（3 個核心問題已確認）
4. PPTX 檔案

### Sprint Mode — 純文字稿（3 項）
1. 已確認的案例名單與入選理由
2. 簡版批判確認清單（3 個核心問題已確認）
3. 純文字分析稿（依 `references/plain-text-format.md` 格式，含來源清單）

---

## 例外處理規則

以下三種情境是執行過程中最常見的失敗點，遇到時依對應規則處理，不要自行判斷或跳過。

**情境 1｜案例搜尋找不到足夠的台灣市場案例**
先確認是「真的沒有」還是「搜尋策略不夠廣」。嘗試以下順序：
1. 放寬時間範圍（2 年內 → 3 年內 → 5 年內，逐步放寬，每步確認仍找不到才繼續）
2. 擴展到台灣品牌的國際市場操作（不限台灣執行地點）
3. 納入與台灣品牌合作的國際案例（以台灣市場為主要受眾）
4. 若三步仍不足，告知使用者目前可找到的候選數量，詢問是否接受降低案例數量、或放寬至國際案例對照。不要在未告知的情況下自行放寬標準。

**情境 2｜使用者在 Phase 4 或之後想更換案例**
不要直接跳回 Phase 3 重跑。先確認：
- 是只換其中一個案例，還是整份 shortlist 重來？
- 換案例的原因是什麼？（資料不足 / 方向不對 / 臨時新想法）
若只換一個案例：針對新案例單獨跑 Phase 3 評估標準，確認入選資格後，直接補入 Phase 4 藍圖，其他案例不受影響。
若整份重來：重新輸出 plan，取得批准後從 Phase 3 重跑。

**情境 3｜Why it lands 頁找不到足夠的佐證事實**
不要硬填推論充當事實。依以下順序處理：
1. 說明目前能找到的公開佐證是什麼（即使只有聲量數字或媒體提及次數）
2. 把「仍是推論的部分」明確標注為「初步判讀，缺乏公開數據支持」
3. 若幾乎沒有任何公開佐證，考慮是否這個案例本身不符合入選標準（資料不足），並告知使用者，詢問是否要替換案例。

---

## 成功標準

以下每一條都有具體定義，不是形容詞：

**案例選得準**  
每個案例都能回答「它解決了什麼別的品牌沒有解決的真實問題」——而不只是「它很有名」或「它得獎了」。

**問題切得準**  
The real problem 頁的問題定義，不能是品牌想說什麼，而是市場或消費者端的結構性困境，且這個困境能在公開資料中找到佐證。

**Insight 足夠深**  
把這個 insight 換成另外三個同類品牌來套，如果都成立，就是太通用。必須是這個案例才有、才能撐起來的矛盾或張力。

**模型用得準而不重**  
每案最多 3 個模型，且每個模型在那一頁解決了別的模型解決不了的分析問題。如果拿掉其中一個、分析仍然完整，那個模型就是多餘的。

**內容能扛質疑**  
報告中所有判斷句，都能回答「你怎麼知道」。事實有來源，判讀標注為判讀，推論標注為推論，不混用。

**每案都能被轉成提案素材**  
What to steal 頁的每一個方法，都附有使用條件——說明什麼類型的品牌、在什麼情境下可以借用這個做法，而不是一句「可以參考這個策略」帶過。
