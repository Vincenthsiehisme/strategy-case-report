# Phase 3.5–7 執行規格

> 此檔案在進入 Phase 3.5 前讀取（Phase 3 Shortlist 確認後觸發讀取）。  
> v2.6 新增 Phase 3.5（扎根搜尋）；Phase 4 Blueprint 新增已知/可估/待查分布標注；Phase 5 改為三欄輸出格式；Phase 6 新增「可知與不可知是否切清楚」批判維度；Phase 6 結束後輸出截點 JSON。

---

## Phase 3.5｜扎根搜尋（AI 自主執行）

> **讀取完整規格**：執行前讀取 `references/root-search.md`，內含三層問題架構、兩階段搜尋策略、替換案例判斷標準、來源記錄格式。

**觸發時機**：Phase 3 Shortlist 確認後立即執行，只對確定入選的案例執行。

**執行宣告**（AI 輸出後開始執行，不等確認）：
> 「Shortlist 確認，開始扎根搜尋。預計執行 [N] 步驟：[案例 1] 三層 × [案例 2] 三層 × [案例 3] 三層，共 9 層搜尋，每層最多兩個階段。」

**三層問題**（每層依序執行直接資料搜尋 → 代理變數搜尋）：
- **壓力層**：為什麼這個品牌在這個時間點不能不做這件事？
- **張力層**：這個矛盾在產業裡存在多久？為什麼沒人解決？
- **邊界層**：這個方法在什麼條件下不成立？

**替換案例觸發條件**：壓力層 + 張力層同時為 `unknown` → AI 主動提案替換，說明原因，等確認（高風險決策）。

**Phase 3.5 輸出**：扎根摘要（AI 內部使用，不外顯），帶入 Phase 4 Blueprint。格式見 `root-search.md`。

完成後直接進 Phase 4。

---

## Phase 4｜Analysis Blueprint（AI 自主執行）

> **分析模型參考**：選用模型時，讀取 `references/model-library.md`。

逐案完成內部規劃，不輸出給使用者確認。

**每案 Blueprint 包含四個部分：**

**① 頁面結構規劃**
依輸出媒介列出每案的頁面清單（標題 + 本案具體策略切角）：

```
頁面 1｜Case in one line
  → 本案切角：[品牌]如何用[具體動作]解決[具體問題]

頁面 2｜The real problem
  → 本案切角：[哪個結構性力量]讓[品牌]在[時間點]無法再照舊做
  → 已知/可估/待查：[壓力層 status] / [張力層 status] / [邊界層 status]

頁面 3｜The tension
  → 本案切角：[哪個習以為常的假設]在這個案例中被推翻了
  → insight 信心層級：[rooted / estimated]

頁面 4｜The strategic reframe
  → 本案切角：[舊說法]被[新說法]取代，差異在[具體的選擇]

頁面 5｜The system
  → 本案切角：[哪些接觸點]被串連，整體路徑邏輯是[什麼]

頁面 6｜Why it lands
  → 本案切角：[哪些 confirmed]支撐，[哪些 estimated]標注，[哪些 unknown]移附錄

頁面 7｜What to steal
  → 本案切角：[哪 2–3 個方法]，各自的 scenarios 結構是[什麼]
```

**② 分析模型配置**（同前版本，每案最多 3 個）

**③ 核心分析問題**（同前版本）

**④ 策略句草稿**
「[品牌] 面對 [真實問題]，選擇 [策略動作]，而不是 [原本的做法]。」

**⑤ 已知/可估/待查分布標注（v2.6 新增）**
對照 Phase 3.5 扎根摘要，標注每案三層的狀態：

```
壓力層：[rooted / estimated / unknown]
張力層：[rooted / estimated / unknown]
邊界層：[rooted / estimated / unknown]

整體評估：
- 高信心部分（可直接作為 confirmed 輸出）：___
- 需代理推論部分（estimated，需附 proxy + assumption）：___
- 分析盲區（unknown，移至來源附錄「待補資料」）：___
```

完成後直接進 Phase 5。

---

## Phase 5｜First-Round Analysis（AI 自主執行）

> **寫作規則**：執行前確認已讀取 `references/writing-rules.md`。

逐案展開完整分析，固定 6 個分析單元。**v2.6 核心變更：每個分析單元輸出三欄結構，不強求填滿，強求切清楚。**

### 三欄輸出格式

每個分析單元都用以下三欄組織內容：

| 欄位 | 定義 | 來源要求 |
|------|------|---------|
| `confirmed` | 有直接資料支撐的判斷 | 每條必須附 source_ref |
| `estimated` | 代理變數推論，有邏輯但無直接佐證 | 每條必須附 proxy + assumption |
| `unknown` | 目前無法判斷 | 每條必須說明 needed + impact |

**原則：`unknown` 不是缺陷，是分析結果的一部分。** 把無法判斷的部分切清楚，比用語言深度填充它更有價值。

### 各單元最低標準

| 分析單元 | 三欄最低要求 |
|---------|------------|
| The real problem | confirmed 或 estimated 至少各有 1 條；若壓力層 unknown，必須在 unknown 欄說明「需要什麼資料才能確認問題根源」 |
| The tension | insight 句必須標注 `insight_confidence`（rooted 或 estimated）；換入 2–3 個同類品牌名後不成立；說明矛盾存在多久 |
| The strategic reframe | 舊框架 vs. 新框架必須是實質不同的框架；新框架說清楚品牌主動放棄了什麼 |
| The system | 接觸點 ≥ 3；說明接觸點之間的邏輯關係（路徑，不是清單） |
| Why it lands | confirmed 直接從 root_evidence 對應層填入，不重新生成；estimated 附代理變數說明；unknown 不進正文 |
| What to steal | 每個方法用 scenarios 結構輸出（條件 → 結果），不輸出單點使用條件；boundary_status 來自 root_evidence.boundary.status；**Slide 版字數上限**：中欄 ≤ 70 字，右欄 ≤ 55 字 |

**寫作規則（不變）：**

- 判斷優先於描述：「Trip.com 押注的是⋯⋯」比「Trip.com 做了⋯⋯」更好
- 命名矛盾：說清楚這個矛盾存在多久、為什麼市場接受了它
- 說清楚邊界：每個 insight 說清楚在什麼條件下成立、在什麼條件下不成立

**禁止的寫作模式：**
- 把 estimated 寫成 confirmed（最常見的幻覺來源）
- 「因為 AI 的崛起」「在數位化浪潮下」——背景描述，不是結構性力量
- 把品牌的自述當作已驗證事實

完成後直接進 Phase 5.5。

---

## Phase 5.5｜深挖層（AI 自主執行，不外顯）

> **讀取完整規格**：執行前讀取 `references/deepdive-protocol.md`。

**v2.6 目標重新定義**：Phase 5.5 的追問目標不是「挖更深」，而是「把 estimated 層的假設說清楚，把 unknown 層的問題拆成可回答的子問題」。

**三軸執行重點：**
- **軸 1｜根源追問**：對照 root_evidence.pressure，確認 real problem 的 estimated 判斷有邏輯支撐；把 unknown 拆成「可驗證的部分 / 可估算的部分 / 暫時無法判斷的部分」
- **軸 2｜矛盾命名測試**：替換測試（真正換入品牌名）+ 反駁測試（找到邊界條件）；確認 insight_confidence 標注正確
- **軸 3｜可執行性測試**：確認每個 steal 的 scenarios 結構完整，每個 scenario 有可說出的 first_step 或明確的 outcome

**⚠️ 執行警示**：若三軸執行後什麼都沒有修改，這本身是警示訊號。特別是軸 2 替換測試，AI 應真正換入品牌名驗證，不是宣稱執行了。

完成後進 Phase 6。

---

## Phase 6｜防守型批判與修正（AI 自主執行，不外顯）

> **讀取完整批判問題庫**：執行前讀取 `references/critique-scorecard.md`。

**v2.6 新增批判維度**：在原有批判問題庫之外，新增「可知與不可知是否切清楚」的批判層。

**執行模式規則（不變）：**
- 預設 Full Mode；Sprint Mode 僅在使用者明示時使用；不得自行降級

**執行邏輯（批判內化，不外顯）：**
- 發現問題 → 直接修正
- 無法修正（資料不足）→ 標注「初步判讀，缺乏公開數據支持」
- 批判執行摘要寫入截點 JSON 的來源附錄區塊
- 批判完成後不停止、不輸出 Scorecard

> **純文字稿路徑例外**：輸出形式為純文字稿時，跳過 Phase 6.5 和截點，直接進 Phase 7 路徑 D。

**Phase 6 完成後：輸出截點 JSON（`report_data.json`）**

AI 將填完的 JSON 輸出給使用者，並說明：

> 「第一段分析完成。`report_data.json` 如下。
>
> 請確認 JSON 內容後，開啟新對話並啟用 **report-renderer skill**，貼入 JSON，說明輸出格式（例如：「渲染成 16:9 Slide PDF」），即可啟動第二段渲染。
>
> [完整 JSON 內容]」

使用者確認 JSON 內容後，手動開啟新對話，使用 report-renderer skill 渲染輸出。

---

## Phase 6.5 + Phase 7｜視覺決策與輸出（report-renderer skill）

Phase 6.5（視覺決策）和 Phase 7（渲染輸出）已移至 **report-renderer skill** 執行。

strategy-case-report 的職責在 Phase 6 截點輸出 JSON 後結束。後續渲染流程、版型規格、輸出映射規則，全部由 report-renderer skill 處理。

**report-renderer skill 的執行規格見其 SKILL.md 和 references/render-mapping.md。**
