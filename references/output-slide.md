# Output Slide Spec · 16:9 Slide PDF
version: "1.1"
updated: "2026-03-20"
paired-with: "strategy-case-report SKILL v2.2"

---

## 文件定位

本文件是 `strategy-case-report` SKILL v2.2 的配套規格文件。

**文件層級說明：**
- SKILL v2.2「Slide 版型規格」章節 → **摘要層**，提供執行中的快速參照
- 本文件（output-slide.md）→ **完整規格層**，提供所有細節、範例、錯誤修正

當兩份文件說法有衝突時，**以本文件為準**。

**觸發條件：**  
Phase 1 Intake 確認輸出形式為「簡報 PDF（16:9 Slide）」時，Phase 6.5 與 Phase 7 路徑 A2 必須依本文件執行。

---

## 版本變更記錄

| 版本 | 日期 | 主要變更 |
|------|------|---------|
| v1.0 | 2026-03-20 | 初始版本，配合 SKILL v2.1 |
| v1.1 | 2026-03-20 | 對齊 SKILL v2.2：統一字體規格表格欄位、釐清版型庫定義（Dark Full）、新增文件定位與版本說明、整合 Gotchas 為唯一來源、新增版型 HTML 範本骨架 |

---

## 1. 頁面規格

```css
@page {
  size: 338mm 190mm;   /* 16:9，等比於 1920×1080 */
  margin: 0;           /* 零 page margin，內距全部在 .slide div 內控制 */
}
```

每個投影片單元：

```css
.slide {
  width: 338mm;
  height: 190mm;
  position: relative;
  overflow: hidden;          /* 硬規則：內容絕對不能溢出 */
  page-break-after: always;
  display: flex;
  flex-direction: column;
}
```

**`overflow: hidden` 是不可妥協的硬規則。**  
如果內容塞不進去，解法是拆成兩頁，不是縮字或移除 `overflow: hidden`。

**.slide 內距規則：**  
所有內距在 `.slide` 的子容器內控制。一般內容頁的 slide-inner padding 為 `7mm 12mm 6mm`。封面與 Section Divider 依設計需要調整，通常 `12–14mm`。

---

## 2. 字體規格

Slide 的讀者距離螢幕或投影畫面較遠，閱讀時間極短。字體規格與 A4 印刷版完全不同，**不可混用**。

| 層級 | 用途 | 字體大小 | 字重 | 備註 |
|------|------|---------|------|------|
| Display | 封面主標題、Section Divider 主標 | 26–34px | 800 | 可跨行，最多 3 行；行距 1.15 |
| Title | 每頁標題（`sh-title`） | 16–20px | 800 | 單行為佳，最多 2 行 |
| Subtitle | Insight box / Quote box 核心主張句 | 10–12px | 700 | 最多 3 行；這裡放主張，不放摘要 |
| Body | Card / steal card 內文 | 8.5–9.5px | 400–500 | **最小可用字體**；每 block ≤ 6 行 |
| Label | Eyebrow、tag、小標籤 | 7–8px | 600–700 | 全大寫 + `letter-spacing: 1.5–3px` |
| Source | 來源標注、初步判讀標注 | 6.5–7px | 400 | `font-style: italic`，色彩減淡至 #B0BEC5 |
| Metric | 關鍵數字 | 18–26px | 800 | 必須與 Label 層級搭配，形成視覺錨點 |

**字體最小值：6.5px。** 低於此閾值在投影時不可讀，不允許使用。

**Body 文字每個 card 或 block 內不超過 6 行。** 超過 6 行代表這個 card 的資訊量需要拆成兩個 card 或兩頁。

**字體系統：**  
使用 system font stack，不依賴外部字體（WeasyPrint 不支援 Google Fonts）：
```css
font-family: "Helvetica Neue", Arial, "PingFang TC", "Microsoft JhengHei", sans-serif;
```

---

## 3. 版面設計語言

### 3.1 印刷版 vs. Slide 根本差異

| 維度 | A4 印刷報告 | 16:9 Slide |
|------|------------|-----------|
| 閱讀方式 | 線性、逐段讀 | 掃視、主張先行 |
| 每頁資訊量 | 高密度 | 單一核心主張 |
| 段落文字 | 允許 5–8 行連續段落 | **禁止**，改用 card / bullet / metric |
| 色塊比例 | 點綴性 | 結構性，整頁背景色是常態 |
| 留白 | 功能性（呼吸感） | 設計語言的一部分（不填滿是對的） |
| 視覺錨點 | 選配 | **必須**：大數字、粗標題、色條、色塊 |
| 頁面高度 | 297mm（A4 含邊距） | 190mm，零 margin |
| overflow | `visible`（允許內容流動） | `hidden`（硬規則） |

### 3.2 每頁資訊密度原則

每頁只允許 **一個核心主張**，配 2–4 個支撐元素。

**支撐元素種類：**
- **Metric strip**：大數字 + 短說明，通常 3–4 個並排
- **Card**：有標題的資訊方塊，內文 ≤ 6 行
- **Steal card**：方法卡，有標題 + 說明 + 條件，左側金色邊框
- **Flow**：流程步驟圖，通常 4–6 個步驟橫向排列
- **Quote box**：核心主張句，深色背景，字重 700
- **Reframe pair**：舊說法 vs. 新說法並排，用於 Strategic reframe 頁

**每頁禁止出現的格式：**
- 連續段落文字超過 3 行未換 card
- 多層巢狀 bullet point
- 超過 5 個 card 在同一頁
- 表格超過 6 列（Recap 表格頁例外）

### 3.3 版型庫

每頁必須選用以下版型之一。不允許自行發明未定義的版型。

#### Cover（封面）
- 背景：深色（主色，通常深藍 / 深灰）
- 結構：左右雙欄。左欄（約 60%）：eyebrow tag + 主標題 + 說明文 + 底部 meta。右欄（約 40%）：案例摘要列表。
- 特徵：主標題 ≥ 26px，右欄背景略淺於左欄以製造層次

#### Section Divider（案例分隔頁）
- 背景：深色（主色）
- 結構：全版深色，大型數字（透明度 6–8%）作底部裝飾，品牌名稱 + 主標題 + 說明文 + 分析視角 tag。
- 用途：每個案例的**第一頁**，製造視覺轉折，讓讀者感受到「換案例了」
- 特徵：無頂部色條；主標題 ≥ 26px；分析視角 tag 用強調色實心背景

#### Content（標準內容頁）
- 背景：白色
- 結構：頂部 4px 色條（案例識別色）→ slide-inner（含 slide-header + 主體內容）
- slide-header：左側案例標籤（eyebrow）+ 頁面標題（Title 層級）；右側年份 + 視角標籤
- 主體內容：flex 佈局，依頁面內容選用支撐元素組合
- **頂部色條是必須的**，每個案例固定一種識別色，全程不變

#### Dark Full（深色全版頁）
- 背景：深色（主色）
- 用途：**Cross-Case Recap 頁、結論的 Core Insight 頁**。製造「整份報告的視覺高潮」，讓讀者感受到節奏轉折。
- 特徵：表格或主張句在深色背景上呈現，文字用白色或高亮度色；重點用強調色標注
- **與 Section Divider 的差異**：Section Divider 是案例的「起點轉折」，Dark Full 是全報告的「收尾轉折」。兩者都是深色背景，但 Section Divider 有大型數字底紋，Dark Full 通常沒有。

#### Appendix（來源附錄）
- 背景：淺灰（#F4F7FB）
- 結構：雙欄文字佈局，字體較小但仍需 ≥ 7.5px
- 用途：來源列表 + 批判執行摘要 + 視覺決策記錄

---

## 4. 色彩使用規則

色彩系統在 Phase 6.5 由 AI 依案例調性決定。本規格定義使用規則，不限定特定色票。

### 4.1 色彩角色定義

| 色彩角色 | 用途 | 選色原則 |
|---------|------|---------|
| 主色（Primary） | Cover / Section Divider / Dark Full 背景、深色元素 | 深色系，傳達信任感與策略嚴肅性。通常為深藍、深灰、深綠 |
| 強調色（Accent） | 頂部色條、重點文字、tag、steal card 左邊框 | 暖色或高飽和色，傳達行動感。通常為橙、紅、黃 |
| 輔助色（Secondary） | 部分 card 邊框、metric 數字 | 中性或冷色，與主色形成對比 |
| 金色 / 提示色 | Steal card 邊框、重要標注 | 選配，不是每份報告都需要 |

### 4.2 案例識別色系統

**每個案例分配一種識別色**，用於：
- 頂部色條（Content 頁，4px）
- Section Divider 的分析視角 tag 背景
- Shortlist 與 Recap 頁中對應案例的標記

三個案例的識別色必須明顯可區分，不可用色系相近的顏色（例如：深藍 + 中藍 + 淺藍 = 難以區分）。

### 4.3 對比度規則

白色背景頁（Content / Appendix）：
- 文字與背景的對比比率必須 ≥ 4.5:1
- 禁止在白色背景上使用低飽和度淺色文字

深色背景頁（Cover / Section Divider / Dark Full）：
- 主要文字用白色（#FFFFFF 或接近白）
- 輔助文字用降低透明度的白（rgba(255,255,255,0.55–0.70)）
- 強調文字用強調色

### 4.4 顏色編碼規則

所有顏色必須使用**硬編碼 hex**，不使用 CSS variable。  
原因：WeasyPrint 不支援 CSS variable（`var(--color-xxx)`），使用後顏色會全部失效。

```css
/* 正確 */
color: #0B2244;
background: #E8522A;

/* 錯誤 */
color: var(--primary);
background: var(--accent);
```

---

## 5. Slide 頁數規劃

16:9 Slide 的資訊密度低於 A4 報告，相同內容需要更多頁。

### 5.1 每案分析頁數

| 分析單元 | A4 報告 | Slide（16:9） | 合頁條件 |
|---------|--------|--------------|---------|
| Case in one line | 1 頁 | 1 頁 | Metrics 同頁 |
| Real problem | 1 頁 | 1 頁 | — |
| Tension | 1 頁 | 可與 Reframe 合頁 | 兩個單元合計內容量 ≤ 4 個 card |
| Strategic reframe | 1 頁 | 可與 Tension 合頁 | 同上 |
| System | 1 頁 | 1 頁 | Flow + 說明 |
| Why it lands | 1 頁 | 1 頁 | Metrics + 事實 + 判讀 |
| What to steal | 1 頁 | 1 頁 | 3 個 steal card |

每案分析頁數：**7–9 頁**（依合頁情況）

### 5.2 非案例頁頁數

| 頁面 | 頁數 |
|------|------|
| 封面（Cover） | 1 |
| 框架說明 | 1 |
| 案例總覽 | 1 |
| Section Divider（每案） | 1 × 案例數 |
| Cross-Case Recap | 1（Dark Full） |
| 結論 Phase 框架 | 1 |
| Core Insight | 1（Dark Full） |
| 來源附錄 | 1–2 |

**3 案報告預估總頁數：26–32 頁**

---

## 6. 寫作規則（Slide 專用）

### 6.1 標題規則

**`sh-title`（頁面功能標籤）**：名詞句，是導覽用的，不是主張。

```
正確：「核心矛盾」「策略重框」「可借用的方法」
```

**Quote box / Insight box 的 `q-text`**：必須是完整主張句，不是摘要。

```
錯誤（描述）：
「Trip.com 導入了 AI Trip Planner，讓旅客可以用三個問題完成行程規劃。」

正確（主張）：
「三個問題取代三百個篩選器——Trip.com 押注的是，旅遊平台的護城河不在庫存量，
而在把旅客意圖轉化為行動的速度。」
```

### 6.2 Section Divider 標題

Section Divider 的主標題可以是名詞句（品牌名稱 + 核心動作），但必須讓讀者一眼看出「這個案例的分析視角是什麼」。

```
正確：
「Trip.com × AI Trip Planner」（品牌 + 核心動作）
「Disney × MagicBand 旅客資料飛輪」（品牌 + 核心概念）

不夠好：
「Trip.com」（只有品牌名，看不出分析視角）
```

### 6.3 Steal card 標題

必須以動詞開頭，說明「做什麼」。

```
錯誤（名詞）：「意圖捕捉前台入口」
正確（動詞）：「把「意圖捕捉」做成前台入口，取代搜尋框」
```

### 6.4 禁止的寫作模式

- 「因為 AI 的崛起」「在數位化浪潮下」——背景描述，不是結構性力量
- 把品牌的自述當作已驗證事實（必須標注「品牌自述，未經獨立驗證」）
- 把「合理推測」直接寫成已驗證結論
- 在 Slide 上出現超過 3 行未換 card 的連續文字

---

## 7. WeasyPrint 轉換規格

### 7.1 轉換代碼

```python
from weasyprint import HTML, CSS

css = CSS(string='''
@page {
  size: 338mm 190mm;
  margin: 0;
}
''')

HTML(filename='/home/claude/report_slides.html').write_pdf(
    '/mnt/user-data/outputs/report_slides.pdf',
    stylesheets=[css]
)

print('PDF generated successfully')
```

### 7.2 轉換前檢查清單

執行轉換前，逐項確認：

**頁面結構：**
- [ ] 所有投影片用 `<div class="slide">` 包裹
- [ ] 每個 `.slide` 有 `overflow: hidden`
- [ ] 每個 `.slide` 有 `page-break-after: always`
- [ ] 無 `position: fixed` 元素
- [ ] 無 `min-height: 100vh`
- [ ] 無 `height: 297mm`（A4 高度，不應出現在 Slide 中）

**字體與顏色：**
- [ ] 所有顏色使用硬編碼 hex，無 `var(--xxx)`
- [ ] 所有字體使用 system font stack，無 Google Fonts 或 `@font-face`
- [ ] 最小字體 ≥ 6.5px

**版型完整性：**
- [ ] 封面頁（Cover）存在
- [ ] 每個案例有 Section Divider
- [ ] 每個 Content 頁有頂部 4px 色條
- [ ] Cross-Case Recap 頁使用 Dark Full 版型
- [ ] Core Insight 頁使用 Dark Full 版型

**禁止項目：**
- [ ] 無 CSS animation 或 transition（WeasyPrint 不支援）
- [ ] 無 JavaScript（WeasyPrint 不執行 JS）
- [ ] 無外部圖片 URL（使用 base64 或 SVG inline）

---

## 8. 版型 HTML 骨架範本

以下為每種版型的最小結構範本，供 Phase 7 執行時參照。顏色值請依 Phase 6.5 決定的色彩系統替換。

### Cover 骨架

```html
<div class="slide" style="background:#0B2244; flex-direction:row;">
  <!-- 左欄：主標題區（60%） -->
  <div style="width:60%; padding:14mm 12mm 10mm 14mm; display:flex; flex-direction:column; justify-content:space-between;">
    <div style="font-size:7px; letter-spacing:3px; text-transform:uppercase; color:#C9A84C; font-weight:700;">
      Strategy Case Report · 2026
    </div>
    <div>
      <div style="font-size:9px; color:#8BAFD4; margin-bottom:3mm;">報告副標題</div>
      <div style="width:20mm; height:3px; background:#E8522A; margin:3mm 0;"></div>
      <div style="font-size:26px; font-weight:800; color:#fff; line-height:1.15;">
        報告主標題<br><span style="color:#E8522A;">重點詞</span>
      </div>
      <div style="font-size:9px; color:#8BAFD4; line-height:1.7; margin-top:4mm;">
        報告說明文，最多 3 行。
      </div>
    </div>
    <div style="font-size:7px; color:#3A567A; border-top:1px solid rgba(255,255,255,0.08); padding-top:3mm; display:flex; justify-content:space-between;">
      <span>決策情境說明</span>
      <span>月份 年份</span>
    </div>
  </div>
  <!-- 右欄：案例摘要區（40%） -->
  <div style="width:40%; background:#0D2A52; padding:10mm; border-left:1px solid rgba(255,255,255,0.08);">
    <div style="font-size:7.5px; color:#C9A84C; letter-spacing:2px; text-transform:uppercase; margin-bottom:4mm;">三個案例</div>
    <!-- 案例項目 × 3 -->
    <div style="display:flex; gap:2.5mm; align-items:flex-start; margin-bottom:4mm;">
      <div style="font-size:18px; font-weight:800; color:rgba(255,255,255,0.08); min-width:8mm;">01</div>
      <div>
        <div style="font-size:8.5px; font-weight:700; color:#fff;">品牌名稱</div>
        <div style="font-size:7px; color:#8BAFD4;">分析視角 · 年份</div>
      </div>
    </div>
  </div>
</div>
```

### Section Divider 骨架

```html
<div class="slide" style="background:#0B2244; flex-direction:column; justify-content:center; padding:14mm 16mm;">
  <div style="font-size:60px; font-weight:800; color:rgba(255,255,255,0.06); line-height:1; margin-bottom:-4mm;">01</div>
  <div style="font-size:7px; letter-spacing:3px; color:#C9A84C; text-transform:uppercase; font-weight:700; margin-bottom:2mm;">Case 01 · 分析視角</div>
  <div style="font-size:28px; font-weight:800; color:#fff; line-height:1.15; margin-bottom:3mm;">
    品牌名稱<br><span style="color:#E8522A;">× 核心動作</span>
  </div>
  <div style="font-size:9.5px; color:#8BAFD4; max-width:160mm; line-height:1.7;">
    一句話說明這個案例解決了什麼問題，以及分析視角是什麼。
  </div>
  <div style="display:inline-block; background:#E8522A; color:white; font-size:7.5px; font-weight:700; padding:1.5mm 4mm; border-radius:1px; letter-spacing:1px; text-transform:uppercase; margin-top:4mm;">
    分析視角標籤 · 年份
  </div>
</div>
```

### Content 骨架

```html
<div class="slide">
  <!-- 頂部色條（案例識別色，4px） -->
  <div style="height:4px; width:100%; background:#3D7EC7; flex-shrink:0;"></div>
  <!-- 內容區 -->
  <div style="flex:1; padding:7mm 12mm 6mm; display:flex; flex-direction:column;">
    <!-- Slide Header -->
    <div style="display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:4mm; flex-shrink:0;">
      <div>
        <div style="font-size:7px; color:#3D7EC7; font-weight:700; letter-spacing:2px; text-transform:uppercase;">Case 01 · 品牌名稱</div>
        <div style="font-size:16px; font-weight:800; color:#0B2244; line-height:1.15; margin-top:0.5mm;">頁面標題</div>
      </div>
      <div style="text-align:right;">
        <div style="font-size:14px; font-weight:800; color:#E8EEF6;">2023–25</div>
        <div style="font-size:7px; color:#94A3B8;">分析視角</div>
      </div>
    </div>
    <!-- 主體內容（依頁面需求組合支撐元素） -->
    <!-- Quote box、Metric strip、Card、Steal card、Flow 等 -->
  </div>
</div>
```

### Dark Full 骨架

```html
<div class="slide" style="background:#0B2244; flex-direction:column;">
  <div style="height:4px; width:100%; background:#C9A84C; flex-shrink:0;"></div>
  <div style="flex:1; padding:7mm 12mm 6mm; display:flex; flex-direction:column;">
    <!-- Slide Header -->
    <div style="margin-bottom:4mm; flex-shrink:0;">
      <div style="font-size:7px; color:#C9A84C; font-weight:700; letter-spacing:2px; text-transform:uppercase;">Cross-Case Recap / Core Insight</div>
      <div style="font-size:16px; font-weight:800; color:#fff; line-height:1.15; margin-top:0.5mm;">頁面標題</div>
    </div>
    <!-- 主體內容：深色背景上的表格或主張句 -->
  </div>
</div>
```

### Appendix 骨架

```html
<div class="slide" style="background:#F4F7FB;">
  <div style="height:4px; width:100%; background:linear-gradient(90deg,#0B2244,#3D7EC7,#E8522A); flex-shrink:0;"></div>
  <div style="flex:1; padding:7mm 12mm 6mm; display:flex; flex-direction:column;">
    <div style="font-size:7px; color:#E8522A; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:1mm;">Source Appendix</div>
    <div style="font-size:16px; font-weight:800; color:#0B2244; margin-bottom:4mm;">來源附錄</div>
    <!-- 雙欄內容 -->
    <div style="display:flex; gap:6mm; flex:1;">
      <div style="flex:1;"><!-- 左欄 --></div>
      <div style="flex:1;"><!-- 右欄 --></div>
    </div>
  </div>
</div>
```

---

## 9. 常見錯誤與修正（唯一來源）

本節是 SKILL v2.2 Gotchas 中「Slide 版型」相關條目的完整版。SKILL 中的 Gotchas 為摘要，以本節為準。

**錯誤 1｜A4 的字體大小套用到 Slide**  
A4 的 body 文字 8–10px 在印刷品上可讀，但在 Slide 上太小。Slide 的 body 最小 8.5px，重要內文應在 9.5–10.5px。  
→ **修正**：對照本文件第 2 節字體規格表，逐層確認字體大小。

**錯誤 2｜連續段落文字**  
一個 card 裡放了 8 行連續文字，讀者看不完。  
→ **修正**：拆成兩個 card，或把次要資訊降為 source note（6.5px）。

**錯誤 3｜每頁 card 數量過多**  
5 個 card + 1 個 metric strip + 1 個 flow 全部在同一頁，結果每個 card 只有 2–3 行，什麼都說不清楚。  
→ **修正**：每頁最多 4 個支撐元素，超過就拆頁。

**錯誤 4｜Section Divider 用白色背景**  
Section Divider 的功能是「視覺轉折 + 案例預告」，必須用深色背景才能讓讀者感受到節奏切換。  
→ **修正**：Section Divider 永遠使用深色（主色）背景，沒有例外。

**錯誤 5｜忘記頂部色條**  
Content 頁缺少頂部 4px 色條，讀者無法快速判斷在看哪個案例。  
→ **修正**：每個 Content 頁的頂部第一個元素必須是 `height:4px` 的色條，顏色與該案例識別色一致。

**錯誤 6｜使用 CSS variable**  
`var(--primary)` 在 WeasyPrint 中不被支援，導致顏色全部失效（通常變成黑色或透明）。  
→ **修正**：所有顏色改為硬編碼 hex，轉換前執行第 7.2 節檢查清單。

**錯誤 7｜Dark Full 與 Section Divider 混用**  
兩者都是深色背景，但用途不同：Section Divider 是案例起點，Dark Full 是全報告的收尾轉折。若把 Recap 頁做成 Section Divider 風格（有大型數字底紋），會讓讀者誤以為是新案例開始。  
→ **修正**：Section Divider 有大型數字底紋 + 分析視角 tag；Dark Full 通常沒有數字底紋，內容是表格或主張句。

**錯誤 8｜`overflow: hidden` 被移除**  
當內容過多時，試圖移除 `overflow: hidden` 讓內容溢出。這會導致內容跨頁，破壞投影片邊界。  
→ **修正**：`overflow: hidden` 不可移除。內容過多的解法只有一個：拆成兩頁。

**錯誤 9｜整份報告沒有深色背景頁**  
所有頁面都是白色背景，讀者在瀏覽時沒有任何節奏感，視覺疲勞。  
→ **修正**：封面（Cover）、每案的 Section Divider、Recap（Dark Full）、Core Insight（Dark Full）必須是深色背景頁。白色背景頁和深色背景頁交替出現，製造節奏。

**錯誤 10｜Quote box 放的是摘要而非主張**  
Quote box 放了「這個案例說明了數位轉型的重要性」這種無意義的摘要句。  
→ **修正**：Quote box 的文字必須是一個完整的策略主張，可以引發爭議或讓人思考。參照第 6.1 節寫作規則。
