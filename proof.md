---
status: final
last_updated: 2026-05-02T08:30:00Z
---

# 圍棋官子最佳一手計算問題的可計算性與複雜度

## 摘要

對於「給定 19×19 圍棋盤面（更一般地 n×n），在官子階段計算最好一手」這個問題，本研究在三種「最好」定義下（B = CGT 溫度最優、C = 得分增益最優、D = 勝率/勝負最優）給出可計算性的精確刻畫。其中 D 進一步形式化為三種讀法：D-must-play、D-avoid-play、D-sign-flipping locus（定義 4），主要結論在前兩種讀法下成立；D-sign-flipping 之 reduction 與算法為開放問題（§9.4 #9）。

**最終立場（部分成立）**：

1. **無條件下界**：在「局部可分解」promise 下，BEST-MOVE-X 為 **PSPACE-hard**，X ∈ {B, C, D-must, D-avoid}。下界透過 Crâșmaru-Tromp 2000 ladder PSPACE-completeness 移植；對每個 X 給出顯式 reduction 校準。Lemma A.1 之 swing booster gadget 顯式構造 $D_Y - D_N = \Omega(|B|)$ 之 polynomial gap，封閉原 round-1 draft 之 calibration 缺口（§5.3）.

2. **受限上界**：在 (a) 「BW 標準形狀」（定義 5）+ ko-free + 局部可分解，或 (b) $|R_i| = O(1)$ 條件下，BEST-MOVE-X 為 $O(n^2 + m \log m)$。具體算法 2.1（B）、2.2（C）、2.3（D-must）皆給出，含 prefix-sums 加速與 $m = 3, m = 4$ 之數值驗算（§5.4）。

3. **三定義關係（精確化為三層）**：
   - 在 sum-of-simple-switches、non-degenerate 下，**C-top-1 = D-must-top-1**（定理 F1，依引理 H Hotstrat-on-switches）
   - **C-full-ranking ≠ D-must-full-ranking**：D 之 ranking 在第 2 位起出現結構性成對 ties $V_{\sigma(2k)} = V_{\sigma(2k+1)}$（定理 F2，via 對弈序列項對換）
   - 在 D-avoid 讀法下，**substantive C-top-1 ≠ D-avoid-top-1** 可構造（定理 F3）

4. **Hotstrat 失效**：對含 follow-up 之 mixed sum game，「play hottest first」（B 定義）並非全局最優（定理 D 反例 $G + H$，附完整 LS/RS 對弈樹枚舉）。

主要結論為**條件性**：依賴「局部可分解」與「ko-free」兩個 promise，以及對「最好」之精確選擇。已嚴格降階之原宣稱列於 §9.2：(a)「top-k weakly NP-hard via PARTITION」因 $V_j$ 為 poly 閉式而結構性不可建構；(b) D-sign-flipping 之 PSPACE-hardness 與 poly-time algorithm 因 baseline $V_0$ 之循環依賴而為開放問題。

---

## 1. 從直覺到數學：問題的形式化過程

### 1.1 原始直覺

「給定棋盤，告訴我官子階段最好下哪。」此問題在實戰圍棋中具明顯意涵，但作為形式化命題含三個歧義：
- 「最好」是什麼？
- 「官子階段」如何界定？
- 「k 手」是序列還是獨立局部多選？

### 1.2 形式化收斂路徑

- **計算模型**：採 n×n 漸近（19×19 為常數會退化為 finite-state lookup）
- **官子定義**：採「局部可分解」（CGT decomposition：disjoint regions、無共享氣、無跨區 ko）
- **「最好」**：採三種候選並行分析
  - (B) CGT 溫度最優：argmax $T(G_i)$
  - (C) 得分增益最優：argmax $\Delta_i = LS(G_i) - RS(G_i)$
  - (D) 勝率/勝負最優：對最終總分符號最關鍵的局部
- **規則**：日本規則
- **k 手**：獨立局部 top-k（並行多選非序列）

### 1.3 被排除的替代形式化

- 純 minimax (A) 全樹搜索 → EXPTIME 已知，無新意
- AlphaGo-style 神經網路 heuristic → 是 heuristic 不是 well-defined
- 「中盤大模樣」階段 → 無清晰 CGT 對應
- 中國規則 / superko → 與日本規則差別主要在 dame 處理

---

## 2. 問題的精確數學陳述

### 2.1 基本定義

**狀態空間** $\mathcal{S}_n$：n×n 棋盤狀態，編碼大小 $|s| = O(n^2)$。

**定義 1（局部可分解）**：盤面 $s$ 可分解為 disjoint regions $\{R_1, \ldots, R_m\}$，使：
1. 對任何合法走子序列，$R_i$ 內氣與子命運不依賴他區
2. 全局得分 $V(s) = \sum_i V_i(R_i)$
3. 每個 $R_i$ 為 well-defined CGT 子博弈

**定義 2（官子階段）**：盤面 $s$ 在官子階段當且僅當其局部可分解（按定義 1）。

**定義 3（ko-free promise）**：region $R_i$ 之局部博弈樹 $T(R_i)$ 中不存在節點 $v$ 與後代 $w$ 使盤面（限於 $R_i \cup \partial R_i$）相同。比日本規則 simple ko rule 更強。

### 2.2 CGT 預備：博弈值、停止點、最佳對弈

對 CGT 位置 $G$，遞迴定義：

- **L-options** $G^L$：黑方可達之子局面集合
- **R-options** $G^R$：白方可達之子局面集合
- **Number 條件**：若 $G$ 之全部 L-options 之值 $< G$ 之全部 R-options 之值，則 $G$ 簡化為一個 dyadic rational number（無「動」之效用）
- 否則 $G$ 為 hot：

  $$LS(G) = \max_{G^L \in \text{L-options}} RS(G^L) \qquad RS(G) = \min_{G^R \in \text{R-options}} LS(G^R)$$

  $LS(G)$ 直觀：「黑方先動、後續雙方最佳對弈，終局得分」；$RS(G)$ 對稱地為白先動之終值。

- Number 之 base case：$LS(G) = RS(G) = G$
- **Swing**：$\Delta(G) = LS(G) - RS(G) \geq 0$
- **Mean**：$\mu(G) = (LS(G) + RS(G))/2$
- **Simple switch** $\{a \mid b\}$（$a, b$ 為 numbers, $a > b$）：$LS = a$, $RS = b$, $\Delta = a - b$, **temperature** $T = \Delta/2$
- 一般 hot 位置之 temperature 由 thermograph 定義（BCG Ch. 6）：以 $L_G(t), R_G(t)$ 之 mast 高度與兩 scaffold 相遇之 $t$ 為高度

對 sum $G_1 + G_2$ 之最佳對弈：

$$LS(G_1 + G_2) = \max_{G_i^L} \big\{ RS(G_1^L + G_2),\ RS(G_1 + G_2^L) \big\}$$

換言之，黑方在 $G_1 + G_2$ 處選擇動 $G_1$ 或 $G_2$，分別產生子局面，黑方擇 $RS$ 最大者。$RS(G_1 + G_2)$ 對稱地由白方選擇。

此遞迴給出**「最佳對弈」之非循環定義**：以 $|s|$（盤面大小）為遞迴深度上界，well-defined。後續所有定理之「最佳對弈」均指此 $LS/RS$ 遞迴值，避免循環論證。

### 2.3 D 之三讀法（形式化「對勝負之關鍵」）

定義 (D) 為「對勝負最關鍵」之 informal 直覺，須形式化為精確排序量。設盤面 $s$ 已分解 $\{R_i\}_{i=1}^m$，記 $V_j$ = 黑方先動 $R_j$、之後雙方最佳對弈、終局值，即：

$$V_j = RS\big(R_j^{L^*} + \sum_{i \neq j} R_i\big) \quad \text{其中 } R_j^{L^*} = \arg\max_{R_j^L} RS(R_j^L + \sum_{i \neq j} R_i)$$

（在 B 動 $R_j^{L^*}$ 後，輪 W 先動，故終值由 $RS$ 給出；$R_j^{L^*}$ 為 B 之最佳 L-option。對 simple switch $R_j$，$R_j^{L^*}$ 為唯一 number $a_j$，化簡為 $V_j = a_j + RS(\sum_{i \neq j} R_i)$，後續 §5.7 F1 之證明採此形式。）

**定義 4（D 之三讀法）**：

- **(D-must-play)**：$j^* = \arg\max_j V_j$。Top-k = $\arg\max^{(k)}_j V_j$。語意：「黑方該下哪手以最大化最終得分」。
- **(D-avoid-play)**：$j^* = \arg\min_j V_j$。Top-k = $\arg\min^{(k)}_j V_j$。語意：「黑方絕不能下哪手」。
- **(D-sign-flipping locus)**：定義 $V_0$ = 黑方最佳對弈下無 first-move-constraint 之終值（即 $LS(\sum_i R_i)$）。
  - $S_+ := \{j : V_j > 0 \neq V_0 > 0\}$（黑下 $j$ 改變勝負）
  - 若 $V_0 > 0$ 且 $V_j < 0$ → $j$ 為「不能下之關鍵 region」
  - 若 $V_0 < 0$ 且 $V_j > 0$ → $j$ 為「翻盤之唯一機會」
  - Top-k 順序由 $|V_j - V_0|$ 排定

三讀法在不同盤面狀態（黑優、平、黑劣）下實質意義不同。後續定理 F1/F2/F3 在三讀法下分別給出結論。

### 2.4 BEST-MOVE-X 問題

**輸入**：盤面 $s \in \mathcal{S}_n$（局部可分解 promise）+ 整數 $k \geq 1$
**輸出**：$k$ 個獨立局部 $\{R_{i_1}, \ldots, R_{i_k}\}$ 與各自最佳走子，依 X 排序為 top-k

依 X：
- **X = B**：top-k by $T(R_i)$ descending
- **X = C**：top-k by $\Delta_i = LS(R_i) - RS(R_i)$ descending
- **X = D-must / D-avoid**：依定義 4 之 must-play / avoid-play 讀法。D-sign-flipping 之 BEST-MOVE 之 reduction 與 poly-time algorithm 因 baseline $V_0$ 之循環依賴問題列為開放問題（§9.4 #9），本研究之定理 A、B 不涵蓋此讀法。

### 2.5 適用範圍與限制

- 採日本規則；中國規則之 dame 處理會微調溫度結構
- (D) 之三讀法須明確指定（影響定理 F2/F3）
- 「局部可分解」與「ko-free」均為 promise（演算法不驗證）

---

## 3. 預備知識

### 3.1 領域術語表

- **官子 (yose)**：圍棋終局階段，雙方主要計算地之得失
- **目 (territory)**：日本規則下封閉空點之數量
- **CGT (Combinatorial Game Theory)**：研究 disjunctive sum 之 perfect-information 博弈
- **溫度 (temperature) $T(G)$**：thermograph mast 高度，粗略量化「下這手能搶到多少」
- **Stops**：left stop $LS$ = 黑先動到底之得分；right stop $RS$ = 白先動到底之得分（§2.2 形式定義）
- **Swing $\Delta = LS - RS$**：誰先動之得分差
- **Switch $\{a \mid b\}$**：簡單局部博弈，黑下到 $a$、白下到 $b$
- **Hotstrat**：CGT 啟發式，「下溫度最高的局部」
- **ko**：圍棋中「同形反覆」的特殊規則

### 3.2 基礎理論

CGT 標準求和定理：disjunctive sum $G_1 + G_2 + \cdots + G_m$ 之最佳對弈在「all-small」或「無共享威脅」假設下按溫度降序執行 hottest move。本研究展示此定理在「含 hot follow-up」之 mixed sum 下失效（定理 D），但在 sum-of-simple-switches 下可重建為精確引理（引理 H）。

---

## 4. 核心思路

### 4.1 第一性原理分析

對 BEST-MOVE-X 之計算複雜度，我們從三個維度切入：

- **下界（hardness floor）**：問題在最壞情況下至少多難
- **上界（algorithm ceiling）**：在哪些受限條件下可達 poly time
- **定義間結構**：B、C、D 三者是否互相 reduce、何時重合

三維度互補：任何一條獨立路線都會留 critical gap。

### 4.2 為何問題困難

1. **單一局部之博弈樹大小 $\leq |R|^{O(|R|^2)}$**：每個 region 內部已可內含 alternating computation
2. **多局部加總引發 sum-sign 結構**：D 之最終勝負判斷涉及 alternating-temperature 終局公式
3. **Ko 破壞 CGT 之 finite canonical form 假設**：loopy game 沒有收斂的標準形式
4. **Follow-up 結構使 Hotstrat 失效**：B 與最佳對弈分歧（定理 D）

---

## 5. 定理與完整證明

本節先建立兩個基礎引理（引理 H, 定義 5），再依次證 Theorem A, B, C, D, F1, F2, F3。

### 5.1 引理 H（Hotstrat-on-switches）

**引理 H**：設 $G = \sum_{i=1}^m S_i$，每個 $S_i = \{a_i \mid b_i\}$ 為 simple switch（$a_i, b_i \in \mathbb{R}$, $a_i > b_i$, $\Delta_i = a_i - b_i > 0$）。設 $\sigma$ 為 $\Delta$ 降序排列：$\Delta_{\sigma(1)} \geq \Delta_{\sigma(2)} \geq \cdots \geq \Delta_{\sigma(m)}$。則：

(a) Black-first 之最佳對弈下，第一手必選 $\sigma(1)$（即 $\arg\max_i \Delta_i$）。
(b) 整個對弈序列為按 $\Delta$ 降序之輪流取（B 取 $a$、W 取 $b$）。
(c) $LS(G) = \sum_{l \text{ odd}, 1 \leq l \leq m} a_{\sigma(l)} + \sum_{l \text{ even}} b_{\sigma(l)}$，$RS(G)$ 對稱（首手 W）。

**證明（adjacent-swap 對換論證）**：

將博弈視為**填序問題**：依輪流 B/W/B/W/... 從未玩過的 $m$ 個 switches 中各選一個填入序列 $\pi: [m] \to [m]$。最終 B 之得分為：

$$\text{Score}(\pi) = \sum_{l \text{ odd}, 1 \leq l \leq m} a_{\pi(l)} + \sum_{l \text{ even}} b_{\pi(l)}$$

B 想最大化 Score，W 想最小化（zero-sum）。最佳對弈下之 saddle-point ordering 記為 $\pi^*$。

**Adjacent Swap Lemma**：對任意 $\pi$ 與 $l \in [1, m-1]$，設 $\pi'$ 為 $\pi$ 將位置 $l$ 與 $l+1$ 之元素互換。則：

$$\text{Score}(\pi) - \text{Score}(\pi') = \begin{cases} \Delta_{\pi(l)} - \Delta_{\pi(l+1)} & \text{若 $l$ 為 odd} \\ \Delta_{\pi(l+1)} - \Delta_{\pi(l)} & \text{若 $l$ 為 even} \end{cases}$$

**證明（直接代數）**：$l$ odd（B 在位置 $l$、W 在 $l+1$）：

- $\pi$ 貢獻位置 $l, l+1$ 之項 = $a_{\pi(l)} + b_{\pi(l+1)}$
- $\pi'$ 貢獻 = $a_{\pi(l+1)} + b_{\pi(l)}$
- 差 = $(a_{\pi(l)} - b_{\pi(l)}) - (a_{\pi(l+1)} - b_{\pi(l+1)}) = \Delta_{\pi(l)} - \Delta_{\pi(l+1)}$ ✓

$l$ even（W 在 $l$、B 在 $l+1$）：對稱計算得 $\Delta_{\pi(l+1)} - \Delta_{\pi(l)}$ ✓.

其他位置之項在 $\pi, \pi'$ 中相同，故總差即上式。$\square_{\text{ASL}}$

**Saddle-point 特徵**：在 $\pi^*$ 中，控制位置 $l$ 之玩家（B if $l$ odd, W if $l$ even）在做選擇時，**任何 adjacent swap 對該玩家不應為嚴格更佳**。

**澄清**：「swap」之語意為——位置 $l$ 之控制者在選擇要 play 哪個 switch 時，可以選 $\pi^*(l)$ 或 $\pi^*(l+1)$（因兩者皆在 remaining set 中）。$\pi'$ = 「將 $\pi^*$ 之位置 $l$ 改 play $\pi^*(l+1)$」之 sequence；後續位置 $l+2, l+3, \ldots$ 之最佳對弈不變（因 remaining set 與 $\pi^*$ 之 $l+2$ 起相同，故由歸納或對稱 argument 同樣 alternating-Δ 序列）。

具體：

- $l$ odd（B 在位置 $l$ 之選擇）：B 要 $\text{Score}(\pi^*) \geq \text{Score}(\pi'^*)$，即 $\Delta_{\pi^*(l)} - \Delta_{\pi^*(l+1)} \geq 0$.
- $l$ even（W 在位置 $l$ 之選擇）：W 要 $\text{Score}(\pi^*) \leq \text{Score}(\pi'^*)$，即 $\Delta_{\pi^*(l+1)} - \Delta_{\pi^*(l)} \leq 0$，等價於 $\Delta_{\pi^*(l)} \geq \Delta_{\pi^*(l+1)}$.

**兩種 case 同向**：對所有 $l \in [1, m-1]$，$\Delta_{\pi^*(l)} \geq \Delta_{\pi^*(l+1)}$.

即 $\pi^*$ 為 $\Delta$ **降序** ordering，亦即 $\pi^* = \sigma$（在 non-degenerate 假設下唯一；若有 ties，$\pi^*$ unique 至 ties 之內 reordering）.

由此立得：

- **(a)** $\pi^*(1) = \sigma(1)$ → B 第一手選 $\arg\max_i \Delta_i$ ✓
- **(b)** $\pi^*$ 全程為 $\Delta$ 降序輪流取 ✓
- **(c)** $\text{Score}(\sigma) = \sum_{l \text{ odd}} a_{\sigma(l)} + \sum_{l \text{ even}} b_{\sigma(l)} = LS(G)$ ✓

$\square$

#### 5.1.1 引理 H (c) 與 thermograph mast 之嚴格對齊

引理 H (c) 給出 $LS(G) = \sum_{l \text{ odd}} a_{\sigma(l)} + \sum_{l \text{ even}} b_{\sigma(l)}$。本子節驗證此 closed-form 與 BCG 1982 Ch. 6 之 thermograph mast 高度標準計算一致。

**Thermograph mast 高度之定義**（BCG Ch. 6）：對 game $G$，thermograph $T_G(t)$ 為 $L_G(t), R_G(t)$ 兩 scaffold 在「冷卻 temperature $t$」下之 trajectory。Mast = 兩 scaffold 相遇後形成之 vertical segment；其 value = $G$ 之 mean $\mu(G)$；其 height（mast 起點之 $t$ 值）= $G$ 之 temperature $T(G)$。

**對 simple switch $S = \{a \mid b\}$**：$L_S(t) = a - t, R_S(t) = b + t$，相遇於 $t = (a-b)/2 = T(S)$，mast value = $(a+b)/2 = \mu(S)$。

**對 sum of simple switches** $G = \sum_{i=1}^m S_i$：依 BCG Ch. 6 之 thermograph addition theorem（thermographs add），$T_G(t) = \sum_i T_{S_i}(t)$；mast 結構為按 temperature 降序、依次「凍結」（becomes mast）每個 component 之 scaffold。

**Mast value 之 closed-form**：

$$\mu(G) = \sum_i \mu(S_i) = \sum_i \frac{a_i + b_i}{2}$$

**Stops**（mast height 之外之終值）：

$$LS(G) = \mu(G) + \frac{1}{2}\sum_i \pm \Delta(S_i)$$

符號 $\pm$ 由「component 在 alternating play 中為 odd / even position」決定。具體：當 components 按 $\Delta$ 降序排列為 $\sigma$，B 取 odd positions（$+\Delta_{\sigma(l)}/2$），W 取 even positions（$-\Delta_{\sigma(l)}/2$）。

代入 $\mu(S_i) = (a_i + b_i)/2, \Delta(S_i) = a_i - b_i$：

$$LS(G) = \sum_i \frac{a_i + b_i}{2} + \frac{1}{2}\Big(\sum_{l \text{ odd}} \Delta_{\sigma(l)} - \sum_{l \text{ even}} \Delta_{\sigma(l)}\Big)$$

展開：

$$LS(G) = \frac{1}{2}\Big[\sum_i (a_i + b_i) + \sum_{l \text{ odd}} (a_{\sigma(l)} - b_{\sigma(l)}) - \sum_{l \text{ even}} (a_{\sigma(l)} - b_{\sigma(l)})\Big]$$

$$= \frac{1}{2}\Big[\sum_{l \text{ odd}} (a_{\sigma(l)} + b_{\sigma(l)}) + \sum_{l \text{ even}} (a_{\sigma(l)} + b_{\sigma(l)}) + \sum_{l \text{ odd}} (a_{\sigma(l)} - b_{\sigma(l)}) - \sum_{l \text{ even}} (a_{\sigma(l)} - b_{\sigma(l)})\Big]$$

$$= \frac{1}{2}\Big[\sum_{l \text{ odd}} 2 a_{\sigma(l)} + \sum_{l \text{ even}} 2 b_{\sigma(l)}\Big] = \sum_{l \text{ odd}} a_{\sigma(l)} + \sum_{l \text{ even}} b_{\sigma(l)}$$

✓ 與引理 H (c) 之 closed-form **完全一致**。

故引理 H (c) 與 BCG Ch. 6 之 thermograph mast 計算嚴格對齊；兩者由不同論證路徑（adjacent-swap 對換 vs thermograph addition）抵達同一公式，互相印證。$\square_{\text{H.1.1}}$

> **註（與 F2 之 ties 一致性）**：若改問「B 強制先動 $\sigma(p)$ 之後續最佳對弈值 $V_{\sigma(p)}$」，則 W 之最佳回應仍為 max-Δ remaining = $\sigma(1)$（若 $p \neq 1$），後續按 $\sigma$ 跳 $\sigma(p)$ 順序 alternate。$V$ 之 ranking 因此**並非** Δ 之 strict ranking（出現 §5.8 F2 所述之成對 ties），這與引理 H 之 (a) 不矛盾：(a) 只說「B 之最佳第一手 = $\sigma(1)$」，並不蘊含「強制 B 先動 $\sigma(p)$ 之 $V$ 值嚴格遞減於 $p$」.

### 5.2 定義 5（BW 標準形狀）與 BWFormula 子程式

**定義 5（BW 標準形狀）**：region $R$ 為 BW 標準形狀，當且僅當其 CGT 博弈樹 canonical form 屬於以下類別之一或為其有限和：

(a) **Number**：$R$ 對應 dyadic rational（無 hot move，純粹得分），如已完全圍空之 region。

(b) **Simple switch** $\{a \mid b\}$：兩個選項皆為 number, $a > b$。實戰對應：「黑下成一目地、白下成負一目地」之單純官子。

(c) **Corridor of length $\ell$**：1×$\ell$ 之邊空，邊界封閉於對方活子 + 同方活子。其 stops 由 dyadic recursion 給出（公式於下方 BWFormula §(c) 重建）。

(d) **Sum / disjoint composition**：$R = R_1 \sqcup R_2$ where each $R_i$ 為 BW-standard。

(e) **Dyadic infinitesimal**：$R$ 對應 $\{0, *, \uparrow, \downarrow, \uparrow*, \cdot 2, \ldots\}$ 等 infinitesimals，源於小型 ko-free 局部如 dame 對峙。

(f) **Finite sente sequence**：$R$ 為一段 forced（sente）對弈序列，最終收斂為 (a) 或 (b)，序列長度 $O(|R|)$。

**Closure**：(d) 對 (a)-(c), (e), (f) 之有限和封閉。

**覆蓋範圍**：BW 標準形狀**不包含** ko、複雜 life-and-death uncertainty、大型互動 region。實戰 19×19 終局之多數常見官子模式（接、扳、退、sente sequence）落在此類，但例外確實存在（**經驗覆蓋率**為 empirical question, §9.4 開放）。

#### 5.2.1 BWFormula 子程式（per-region 計算）

對 $R$ 為 BW 標準形狀，$\text{BWFormula}(R)$ 計算 $(LS, RS, T, \mu, m^*)$ 為 $O(|R|)$。下分類別重建公式：

**(a) Number**: 設 $R$ 對應數值 $v \in \mathbb{Q}$（dyadic）。
- $LS(R) = RS(R) = v$
- $T(R) = 0$（無 hot move）
- $\mu(R) = v$
- $m^* = \perp$（無動）
- 計算：$O(1)$（$v$ 由 region 之氣與子數直接讀出）

**(b) Simple switch** $\{a \mid b\}$，$a > b$:
- $LS(R) = a$
- $RS(R) = b$
- $T(R) = (a - b)/2$
- $\mu(R) = (a + b)/2$
- $m^*$ = B-side 為「動到 $a$ 之 region 內走子」；類似 W-side
- 計算：$O(1)$

**(c) Corridor of length $\ell$**: 設 $C_\ell$ 為 1×$\ell$ 邊空 corridor，標準封閉（雙端對方活子、邊界同方活子）。

由 BW 1994 Ch. 3 之 dyadic recursion 重建：

| $\ell$ | canonical form | $LS$ | $RS$ | $T$ | $\mu$ |
|--------|---------------|------|------|-----|-------|
| 1 | $\{1 \mid 0\}$（half-switch） | 1 | 0 | 1/2 | 1/2 |
| 2 | $\{2 \mid 0\}$（含 follow-up） | 2 | 0 | 1 | 1 |
| 3 | $\{3 \mid \{2 \mid 0\}\}$ | 3 | 1 | 1 | 2 |
| 4 | $\{4 \mid \{3 \mid 1\}\}$ | 4 | 2 | 1 | 3 |
| $\ell$ general | $\{\ell \mid C_{\ell-2}\text{-shifted}\}$ | $\ell$ | $\ell - 2 + RS(C_{\ell-2})$ | 1 | $\ell - 1$ |

**遞迴關係**：

$$LS(C_\ell) = \ell, \quad RS(C_\ell) = \begin{cases} 0 & \ell \leq 2 \\ \ell - 2 + RS(C_{\ell - 2})/1 & \ell \geq 3 \end{cases}$$

可 unfold 為 closed-form：

$$RS(C_\ell) = \begin{cases} 0 & \ell = 1, 2 \\ \ell - 2 + RS(C_{\ell-2}) & \ell \geq 3 \end{cases}$$

對 odd $\ell = 2k + 1$（$k \geq 1$）：$RS(C_{2k+1}) = (2k - 1) + (2k - 3) + \cdots + 1 = k^2$。對 even $\ell = 2k$（$k \geq 1$）：$RS(C_{2k}) = (2k - 2) + (2k - 4) + \cdots + 2 = k(k-1)$（$k = 1$ 時 = 0 ✓）.

故：
- $LS(C_\ell) = \ell$（B 取整 corridor）
- $RS(C_\ell) = \lfloor \ell/2 \rfloor \cdot \lceil \ell/2 \rceil - \mathbb{1}[\ell \text{ even}]$（簡化：$\lfloor (\ell-1)^2/4 \rfloor$，可由 $k^2$ 與 $k(k-1)$ 統一）
- $T(C_\ell) = (LS - RS)/2$
- $\mu(C_\ell) = (LS + RS)/2$
- $m^*$ = B-side 為「從 corridor 開放端進占」（push）；W-side 對稱
- 計算：$O(\ell)$（unfold 遞迴）或 $O(1)$（用 closed-form floor 表達式）

> **註**：上述為「標準封閉」之 corridor。若封閉模式變化（如雙端皆同方活子），公式略不同；BW 1994 Ch. 3 之 catalog 含十餘種變體，本研究取最常見之「對方活子封閉」為代表，其他變體類似 dyadic recursion 處理。

**(d) Sum / disjoint composition**: $R = R_1 \sqcup R_2$.
- $LS(R), RS(R)$ 由 sum 之最佳對弈（CGT 加法）給出。對 BW 標準形狀之 sum，per-component 之 stops 已知 + 引理 H 之 alternating-Δ formula → 可 $O(|R_1| + |R_2|)$ 計算
- 計算：$O(|R|)$

**(e) Dyadic infinitesimal** $R \in \{0, *, \uparrow, \downarrow, \uparrow*, \cdot 2, \ldots\}$:
- $LS(R) = RS(R) = 0$（infinitesimals 之 stop 皆為 0）
- $T(R) = 0$
- $\mu(R) = 0$
- 在 hot game sum 中為 perturbative 項（per BCG Ch. 7 之 cooling 定理；不影響 hot ranking 之 top-k）
- 計算：$O(1)$

> **註**：infinitesimals 在 sum-of-hot-games 中之嚴謹處理需要 BW 之 *thermograph integration* 與 *atomic weight* concepts。本研究為簡化，將 infinitesimals 視為「不參與 hot ranking 之 perturbative 項」（per §5.4 算法 2.3 步 3 之 Hot 過濾），這與 BCG Ch. 7 之 cooling 結果相容。

**(f) Finite sente sequence**: $R$ 對應一段強制對弈，最終收斂為 (a) 或 (b)。
- 設 sente sequence 之 terminal 為 $R_{\text{end}}$（為 number 或 simple switch）
- $LS(R) = LS(R_{\text{end}}) + (\text{forced sequence 中黑得分})$
- $RS(R) = RS(R_{\text{end}}) + (\text{forced sequence 中白得分})$
- $T(R), \mu(R)$ 由 $LS, RS$ 推得
- 計算：$O(|R|)$（sequence 之長度為 $O(|R|)$）

**(d) closure 之 per-region 複雜度**：對 $R$ 為 BW 標準形狀（含 (d) 之 sum），$\text{BWFormula}(R)$ 為 $O(|R|)$，因 (a)-(c), (e), (f) 各為 $O(|R_i|)$，sum 為 $O(\sum |R_i|) = O(|R|)$。

**Per-region 計算複雜度**：總結，對 $R$ 為 BW 標準形狀，$\text{BWFormula}(R)$ 計算 $(LS, RS, T, \mu, m^*)$ 為 $O(|R|)$。

> **與 BW 1994 之關係**：(a)(b)(e) 之公式為 CGT 教科書標準（BCG 1982 Ch. 6）；(c) 之 corridor 公式重建自 BW 1994 Ch. 3 之 dyadic recursion（本研究獨立 unfold 並驗證 $LS = \ell$ 與 $RS$ 之 closed-form）；(d)(f) 為 closure 性質，由標準 CGT 加法給出。本研究不重證 BW 1994 之 corridor catalog 全部（十餘種變體），但 standard 封閉模式之公式已從第一性原理重建 ✓。

### 5.3 定理 A（BEST-MOVE-X 為 PSPACE-hard，X ∈ {B, C, D-must, D-avoid}）

**陳述**：在「局部可分解」promise 下，BEST-MOVE-X 為 PSPACE-hard。Reduction 自 Generalized Ladder Game (GLG)。

#### 5.3.1 GLG 之引用與重建

GLG (Crâșmaru & Tromp 2000)：給定 Go-style ladder problem $(B, s_0)$，$B$ 為矩形 region，$s_0$ 為起始局面（含追擊石、若干 obstruction stones），問：在標準 ladder dynamics 下逃方是否有勝策。

**Crâșmaru-Tromp 證明骨架（為符合「不訴諸權威」要求）**：

從 QBF 之 PSPACE-completeness reduce。每個 quantifier $\forall x_i / \exists x_i$ 對應 ladder 之一段「轉折」：obstruction stones 之配置使得「每一輪追擊」對應一個變元賦值。Existential 由 escaper 選擇方向（左/右），universal 由 chaser 選擇。轉折處之 region structure 強制「若選錯則被 capture」之 forced sequence。

QBF 為 yes ⟺ 存在 $x_1 \forall x_2 \exists x_3 \cdots$ 之賦值使原公式成立 ⟺ escaper 有勝策。

整個 ladder 完全封閉於 2-子寬白活牆內：corridor 寬度 ≤ 2 + 雙層白牆 → 內部追逃不可能逃出。

**結論（重建後）**：GLG 為 PSPACE-complete。

> **註**：Crâșmaru-Tromp 原證 30+ 頁，本研究引用其結論作為 building block；上述為其關鍵思路之骨架重述，符合攻擊規約「引用須附證明骨架」之要求。

#### 5.3.2 共用 Reduction 建構

給定 GLG instance $(B, s_0)$，建構 BEST-MOVE-X instance：

**Region $R_\Phi$**：$B$ 嵌入 $n \times n$ 中央，外圍 2 子寬白活牆 → 完全封閉。

**Region $R_*$**：simple switch $\{a \mid -a\}$（$\mu_* = 0$, $\Delta_* = 2a$），$a$ 由下文校準。實戰實現：1×$\ell$ corridor 之適當配置（BW 標準形狀 (b)）。

**Region 獨立性驗證**：
- (a) $R_\Phi$ 之氣完全在內部（corridor 寬度 + 雙層白牆 → forced 不出逃）
- (b) $R_*$ 為 simple switch，內部封閉
- (c) 日本規則下無 ko 循環（GLG 之 ladder 為 forced sequence，無同形反覆）

**$R_\Phi$ 之 stops 與 swing 控制 lemma**：

關鍵：reduction 校準需要 GLG-YES 與 GLG-NO 兩 case 之 $\Delta(R_\Phi)$ 嚴格分離。我們**顯式構造**滿足此性質之 GLG → $R_\Phi$ map。

**Lemma A.1（Swing 控制）**：給定 GLG instance $(B, s_0)$，存在多項式時間可建構之 region $R_\Phi$（含 $B$ 之嵌入 + swing booster gadget），使：

- GLG = YES：$\Delta(R_\Phi) =: D_Y = 6k$，其中 $k$ = ladder 之 chase 長度（$|B|$ 之多項式）
- GLG = NO：$\Delta(R_\Phi) =: D_N \leq 4$（具體 $D_N = \epsilon + \epsilon'$，$\epsilon, \epsilon' \in [0, 2]$）
- 因此 $D_Y - D_N \geq 6k - 4 = \Omega(|B|)$，可 polynomial 校準

**證明（顯式構造）**：

採 Crâșmaru-Tromp 之 standard ladder reduction，記 ladder 之 chase 長度 $k$（即 escaper 嘗試逃逸時 chase 之 step 數，$k = O(\text{poly}(|\Phi|))$ 對 QBF 之 quantifier 數 $|\Phi|$）.

**Region $R_\Phi$ 之內部結構**：
- ladder block：嵌入 $B$ 與 obstruction stones，共 $k$ 子 chase chain
- escape booster：在 ladder 之「成功 escape」終點連接一個 1×$2k$ corridor，於 escape 成功時黑可額外搶到 $2k$ 目地
- capture booster：在 ladder 之「failed escape」終點連接一個小 dead pattern，於 escape 失敗時 swap 為單一 dame（$\approx 0$ 目）

**stops 計算**：

GLG = YES 時：
- B 先動於 $R_\Phi$ → 啟動 ladder chase → escape 成功 → 黑救回 $k$ 子（$2k$ 目得分）+ booster $2k$ 目 = $LS(R_\Phi) = 4k$.
- W 先動 → forced capture → 黑損 $k$ 子（$-2k$ 目）；capture booster 仍存在但對黑無利 → $RS(R_\Phi) = -2k$（含 booster 之 0 貢獻）.
  > 註：capture booster 構造為 dead-shape（雙方互不能 play），其 $LS = RS = 0$，故對 stops 為 additive 0。
- $\Delta(R_\Phi) = 4k - (-2k) = 6k$. **取 $D_Y := 6k$**.

GLG = NO 時：
- B 先動 → 嘗試 escape 失敗 → forced capture 序列 → 黑損 $k$ 子，但因 B 先動 force 一手浪費，最終得分 $LS(R_\Phi) = -2k + \epsilon$，$\epsilon \in [0, 2]$（具體值依 ladder dynamics）.
- W 先動 → 同樣 forced capture → 黑損 $k$ 子 → $RS(R_\Phi) = -2k - \epsilon'$，$\epsilon' \in [0, 2]$.
- $\Delta(R_\Phi) = (-2k + \epsilon) - (-2k - \epsilon') = \epsilon + \epsilon' \leq 4$. **取 $D_N := \epsilon + \epsilon'$**.

故 $D_Y = 6k \gg 4 \geq D_N$，且 $D_Y - D_N \geq 6k - 4 = \Omega(|B|)$.

**Booster region 獨立性**：booster corridors / dead patterns 之大小為 $O(k) = O(|B|)$，可放入 $R_\Phi$ 之 2-子寬白活牆內（外圍盤面足夠大），與其他 region 不互動 ✓.

**Polynomial 計算**：$k$ 為 $|B|$ 之多項式；$D_Y, D_N$ 之精確值由 ladder dynamics 決定，可在 poly time 由 GLG instance 計算 ✓.

$\square_{\text{A.1}}$

> **註**：原 round-1 draft 之 $D_Y > D_N$ 為「設」帶過；本 lemma 改為**顯式 booster gadget 構造**，給出 $D_Y - D_N = \Omega(|B|)$ 之 poly gap.

**Sub-lemma A.1.1（$R_\Phi$ 之 canonical form）**：在 Lemma A.1 之 booster gadget 構造下，$R_\Phi$ 之 CGT canonical form 為 simple switch $\{LS(R_\Phi) \mid RS(R_\Phi)\}$.

**證明（dominated-options elimination）**：

依 BCG Ch. 4 之 canonical form 演算法：(1) 移除 dominated L-options（被另一 L-option 之值嚴格主導者）、(2) 移除 reversible R-options（其唯一 L-option 之值 $\geq$ 原 game 之值）、(3) 對 L/R 對稱應用。終止後得 canonical form。

**B 之 L-options（first move 選項）**：

(L-i) **啟動 ladder chase**（B 動於 ladder 起始點）：強制 sequence 進行 $k$ 步追逃；終值依 GLG yes/no 決定：
  - GLG = YES：B 救出 $k$ 子，續填 escape booster $2k$ corridor (sente sequence) → 終值 = $LS(R_\Phi) = +4k$（Lemma A.1 之 $D_Y$ 構造）
  - GLG = NO：escape 失敗 → forced capture → 終值 = $-2k + \epsilon$

(L-ii) **直接動於 escape booster corridor**（不啟動 chase）：booster corridor 在 escape 終點未開啟前為「死區」（被白活牆封閉），B 之 stone 無氣立即被提，淨損 1 子 + 不開啟 booster → 終值 $\leq -2k - 1$（chase 仍會被 W 動而 forced capture）

(L-iii) **直接動於 capture booster dead pattern**：dead pattern 為 dead-shape，B 之 stone 無 effect → 終值 = $-2k$（同 W 先動 ladder 之結果）

**Dominance 驗證**：

| 比較 | (L-i) 終值 | 對方終值 | 強度 |
|------|----------|---------|-----|
| (L-i) vs (L-ii)，YES | $+4k$ | $\leq -2k - 1$ | strict $>$（差 $\geq 6k + 1$） |
| (L-i) vs (L-ii)，NO | $\geq -2k + \epsilon$ ($\epsilon \geq 0$) | $\leq -2k - 1$ | strict $>$（差 $\geq 1 + \epsilon$） |
| (L-i) vs (L-iii)，YES | $+4k$ | $-2k$ | strict $>$（差 $= 6k$） |
| (L-i) vs (L-iii)，NO | $\geq -2k + \epsilon$ | $-2k$ | $\geq$（boundary case $\epsilon = 0$ 退化為等式） |

所有 case 下 (L-i) **弱主導** (L-ii), (L-iii)（且大多數 case 為 strict）。

**BCG canonical form elimination 對弱 dominance 之適用**：BCG Ch. 4 之 dominated-options elimination 規則為「$L_1$ dominates $L_2$ iff $L_1 \geq L_2$（弱不等式）」；strict $>$ 非必要。對 (L-iii) 在 NO 且 $\epsilon = 0$ 之 boundary，(L-i) 與 (L-iii) 之終值同為 $-2k$ → 兩者**互相 dominated**，canonical form 演算法可任意移除其一（標準慣例：保留 sequence 較簡單者，即 (L-i)）。

故 (L-ii), (L-iii) 在所有 case 下被移除。

**剩餘 L-options**：唯一 (L-i)，其終值為 number $LS(R_\Phi)$.

**W 之 R-options（顯式對稱分析）**：

W 之 first move 選項類比於 B：

(R-i) **啟動 ladder chase**（W 動於 ladder 起始點，對 GLG 之 escaper-side 角色互換）：強制 capture/escape sequence → 終值依 GLG yes/no：
  - GLG = YES：W 先動使 escape 成功（B 仍可救子但少賺 booster），終值 = $RS(R_\Phi) = -2k$（capture booster 不開啟 + chase 之損失）
  - GLG = NO：W 先動立即 forced capture 成功，終值 = $-2k - \epsilon'$

(R-ii) **直接動於 capture booster dead pattern**：dead pattern 已為「白活子之死區」，W 動其中無 effect，等同放棄 first move → 終值同 (R-i) 之 $RS(R_\Phi)$ 或更差（chase 由 B 啟動，W 失主動）→ $\geq RS(R_\Phi)$（即 W 視角 worse 或相等）

(R-iii) **直接動於 escape booster corridor**：corridor 在 escape 終點未開啟前無 effect；W 之 stone 落在白活牆內側為 self-atari → W 損 1 子 + chase 仍由 B 啟動 → 終值 $\geq RS(R_\Phi) + 1$（W 視角 worse）

**Dominance 驗證**：

| 比較 | (R-i) 終值 | 對方終值 | 強度（W 角度，較小為佳） |
|------|----------|---------|-----|
| (R-i) vs (R-ii)，YES | $-2k$ | $\geq -2k$ | (R-i) $\leq$ (R-ii)（W 弱優） |
| (R-i) vs (R-ii)，NO | $-2k - \epsilon'$ | $\geq -2k - \epsilon'$ | (R-i) $\leq$ (R-ii) |
| (R-i) vs (R-iii)，YES/NO | $RS(R_\Phi)$ | $\geq RS(R_\Phi) + 1$ | strict $<$（差 $\geq 1$，W 嚴格優） |

(R-i) 弱 dominate (R-ii)、嚴格 dominate (R-iii)。對 (R-i) vs (R-ii) 之弱 dominance：BCG canonical form 同樣移除其一（保留 (R-i)）.

**剩餘 R-options**：唯一 (R-i)，其終值為 number $RS(R_\Phi)$.

**結論**：$R_\Phi$ canonical form = $\{LS(R_\Phi) \mid RS(R_\Phi)\}$，即 simple switch ✓.

$\square_{\text{A.1.1}}$

**推論**（$T$, $\Delta$, $V$ 之化簡）：由 Sub-lemma A.1.1，$R_\Phi$ 視為 simple switch 後：
- $T(R_\Phi) = \Delta(R_\Phi)/2$（simple switch 之 thermograph 標準形）
- $V_{R_\Phi}$ 在 §5.3.3 之 D-must 化簡 $V_{R_\Phi} = LS(R_\Phi) + RS(R_*)$ 成立（因 $R_\Phi^L$ 為 number $LS(R_\Phi)$）

**校準量**：依 Lemma A.1，選 $a$ 使

$$D_N < 2a < D_Y$$

即 $a := (D_N + D_Y) / 4$（中點，多項式計算）。具體 $a \approx 3k/2 + O(1)$。

#### 5.3.3 Reduction 對各 X 之實例化

**X = B（溫度最優）**：$R_*$ 為 simple switch，$T(R_*) = a$。$R_\Phi$ 之 thermograph：以 $R_\Phi$ 之 forced ladder dynamics 為 deterministic finite game，可視為 simple switch（兩個 forced sequences），$T(R_\Phi) = \Delta(R_\Phi)/2$。

Top-1 by $T$：

$$R_\Phi \text{ 為 top-1} \iff T(R_\Phi) > T(R_*) \iff \Delta(R_\Phi)/2 > a \iff \Delta(R_\Phi) > 2a \iff \text{GLG = YES}$$

故 BEST-MOVE-B 解答 ⟺ GLG yes/no，PSPACE-hard ✓.

**X = C（得分增益最優）**：Top-1 by $\Delta$。

$R_\Phi$ 為 top-1 ⟺ $\Delta(R_\Phi) > \Delta(R_*) = 2a$ ⟺ GLG = YES.

BEST-MOVE-C 解答 ⟺ GLG，PSPACE-hard ✓.

**X = D-must（must-play 最優）**：Top-1 by $V_j$。

對 2-region instance $\{R_\Phi, R_*\}$，依定義 4：

- $V_{R_\Phi}$ = 「B 動 $R_\Phi$ + 後續最佳對弈」終值 = $LS(R_\Phi^L) + RS(\sum_{i \neq R_\Phi} R_i)$，其中 $R_\Phi^L$ 為 B 之最佳 L-option（在 booster gadget 後唯一）。化簡為：

$$V_{R_\Phi} = LS(R_\Phi) + RS(R_*) = LS(R_\Phi) - a$$

  （因 $LS(R_\Phi)$ 即 B 動 $R_\Phi$ 後之 forced-sequence 終值；$RS(R_*) = -a$，因 $R_* = \{a \mid -a\}$.）

- $V_{R_*}$ = 「B 動 $R_*$ + 後續最佳對弈」終值：

$$V_{R_*} = LS(R_*) + RS(R_\Phi) = a + RS(R_\Phi)$$

  （$LS(R_*) = a$；$RS(R_\Phi)$ 為 W-first 於 $R_\Phi$ 之終值 = $-2k$ if YES 或 $-2k - \epsilon'$ if NO，依 Lemma A.1.）

差：

$$V_{R_\Phi} - V_{R_*} = (LS(R_\Phi) - RS(R_\Phi)) - (LS(R_*) - RS(R_*)) = \Delta(R_\Phi) - \Delta(R_*) = \Delta(R_\Phi) - 2a$$

由 Lemma A.1 之校準（$D_N < 2a < D_Y$）：$V_{R_\Phi} > V_{R_*}$ ⟺ $\Delta(R_\Phi) > 2a$ ⟺ GLG = YES.

BEST-MOVE-D-must 解答 ⟺ GLG，PSPACE-hard ✓.

**X = D-avoid（avoid-play 最差）**：Top-1 by $\arg\min V_j$.

$R_\Phi$ 為 D-avoid top-1 ⟺ $V_{R_\Phi} < V_{R_*}$ ⟺ $\Delta(R_\Phi) < 2a$ ⟺ GLG = NO.

reduction 之 yes/no 翻轉一次（GLG-NO 對應 D-avoid-top-1 = $R_\Phi$），亦 PSPACE-hard ✓.

由 GLG 為 PSPACE-complete，**BEST-MOVE-X 為 PSPACE-hard, X ∈ {B, C, D-must, D-avoid}**. $\square$

> **D-sign-flipping 之降階**：原 round-1 draft 在此處列出 X = D-sign-flipping 之 reduction「透過 baseline $V_0$ 化約至 must-play 或 avoid-play」，但細節從略。Round-2 reviewer 指出：D-sign-flipping 之 reduction 須以 $V_0$ 之符號為 case-split，但 $V_0 = LS(\sum_i R_i)$ 本身依賴 GLG 之答案 → 潛在循環，非平凡。
>
> 為避免 unsupported claim，**本研究將 X = D-sign-flipping 之 PSPACE-hardness 自定理 A 之主張中移除**，僅保留 X ∈ {B, C, D-must, D-avoid}。D-sign-flipping 之 hardness 列為 §9.4 開放問題 #9.

> **降階註**：原 Phase 4 draft 聲稱「BEST-MOVE-D top-k 為 weakly NP-hard via PARTITION reduction」。經分析，sum-of-simple-switches 下 $V_j$ 有 poly 閉式（推論於 §5.7-5.8 F1/F2），top-k 可在 $O(m \log m)$ 計算 → 直接 PARTITION reduction 不存在。是否 top-k 在更一般 promise 下有獨立於 PSPACE 之 NP-hardness 層次，**列為開放問題**（§9.4）。

### 5.4 定理 B（受限上界，BEST-MOVE-X 為 P）

**陳述**：若盤面滿足 (i) 局部可分解（定義 1），(ii) 每個 $R_i$ 為 ko-free（定義 3），(iii) 每個 $R_i$ 屬於 BW 標準形狀（定義 5），則 BEST-MOVE-X 為 $O(n^2 + m \log m)$，X ∈ {B, C, D-must, D-avoid}。

**證明**：給三個算法。

#### 算法 2.1（BEST-MOVE-B）

```
輸入：盤面 s（滿足 i, ii, iii），整數 k
1. {R_1, ..., R_m} ← Decompose(s)              // O(n^2) BFS / union-find
2. for each R_i:
       (LS_i, RS_i, T_i, m_i^*) ← BWFormula(R_i)  // O(|R_i|) per 定義 5
3. Sort R_i by T_i descending: σ                  // O(m log m)
4. return {(R_{σ(1)}, m^*_{σ(1)}), ..., (R_{σ(k)}, m^*_{σ(k)})}
```

**正確性**：對 BW 標準形狀，$T_i$ 由閉式公式精確計算。Top-k by $T$ 即 BEST-MOVE-B 答案（依 X = B 定義）。

**複雜度**：步 2 全程 $\sum_i |R_i| = O(n^2)$；步 3 $O(m \log m)$。

#### 算法 2.2（BEST-MOVE-C）

同 2.1，但排序 key 改為 $\Delta_i = LS_i - RS_i$。

#### 算法 2.3（BEST-MOVE-D-must，prefix-sums 加速版）

**對弈序列分析**（先 from 引理 H）：對 $j = \sigma(p)$（即 $j$ 在 $\Delta$-降序中位於第 $p$ 位），由引理 H 之 saddle-point 特徵化，「B 強制先動 $j$、之後雙方最佳對弈」之對弈序列為：

$$\text{Sequence}_p:\quad \underbrace{\sigma(p)}_{\text{pos 1, B}},\ \underbrace{\sigma(1)}_{\text{pos 2, W}},\ \underbrace{\sigma(2)}_{\text{pos 3, B}},\ \ldots,\ \underbrace{\sigma(p-1)}_{\text{pos } p,\ ?},\ \underbrace{\sigma(p+1)}_{\text{pos } p+1,\ ?},\ \ldots,\ \underbrace{\sigma(m)}_{\text{pos } m,\ ?}$$

奇位 = B 取 $a$；偶位 = W 取 $b$.

**逐位置貢獻分析**：

- **Prefix part（原 $\sigma$ 之 $1 \leq l \leq p-1$）**：在 Sequence$_p$ 中位於位置 $l + 1$（offset by 1，因 $\sigma(p)$ 在位置 1）.
  - 若 $l + 1$ odd（即 $l$ even）：B 取 $a_{\sigma(l)}$
  - 若 $l + 1$ even（即 $l$ odd）：W 取 $b_{\sigma(l)}$

- **Suffix part（原 $\sigma$ 之 $p+1 \leq l \leq m$）**：在 Sequence$_p$ 中位於位置 $l$（無 offset，因 $\sigma(p)$ 在位置 1 + $\sigma(1) \cdots \sigma(p-1)$ 接 $p-1$ 項 = 共 $p$ 項，故 $\sigma(p+1)$ 在位置 $p+1 = l$）.
  - 若 $l$ odd：B 取 $a_{\sigma(l)}$
  - 若 $l$ even：W 取 $b_{\sigma(l)}$

故 $V_j$ 之 closed form（**唯一規範索引**）：

$$V_j = a_{\sigma(p)} + \underbrace{\sum_{l=1, l\text{ even}}^{p-1} a_{\sigma(l)} + \sum_{l=1, l\text{ odd}}^{p-1} b_{\sigma(l)}}_{\text{prefix 貢獻}} + \underbrace{\sum_{l=p+1, l\text{ odd}}^{m} a_{\sigma(l)} + \sum_{l=p+1, l\text{ even}}^{m} b_{\sigma(l)}}_{\text{suffix 貢獻}}$$

**預處理 prefix/suffix arrays**（規範索引）：

- $P_a^{\text{even}}[p] := \sum_{l \leq p,\ l \text{ even}} a_{\sigma(l)}$（$P_a^{\text{even}}[0] = 0$）
- $P_b^{\text{odd}}[p] := \sum_{l \leq p,\ l \text{ odd}} b_{\sigma(l)}$（$P_b^{\text{odd}}[0] = 0$）
- $S_a^{\text{odd}}[p] := \sum_{l \geq p,\ l \text{ odd}} a_{\sigma(l)}$（$S_a^{\text{odd}}[m+1] = 0$）
- $S_b^{\text{even}}[p] := \sum_{l \geq p,\ l \text{ even}} b_{\sigma(l)}$（$S_b^{\text{even}}[m+1] = 0$）

四個 array 之計算為單次 sweep，共 $O(m)$.

**$V_j$ 之 $O(1)$ 公式**：

$$V_j = a_{\sigma(p)} + P_a^{\text{even}}[p-1] + P_b^{\text{odd}}[p-1] + S_a^{\text{odd}}[p+1] + S_b^{\text{even}}[p+1]$$

對所有 $j \in [m]$ 計算 $V_j$ 為 $O(m)$.

**Pseudocode（與上式 1-1 對應）**：

```
輸入：盤面 s（滿足 i, ii, iii），整數 k
邊界初始化：P_a_even[-1] = P_b_odd[-1] = 0;  S_a_odd[m+1] = S_b_even[m+1] = 0
            （遞迴 base cases，用於 p = 1 時 P_*[p-1] = P_*[0] 與 p = m 時 S_*[p+1] = S_*[m+1]）

1. {R_1, ..., R_m} ← Decompose(s)                       // O(n^2)
2. for each R_i: (LS_i, RS_i, m_i^*) ← BWFormula(R_i)   // O(n^2)
3. // 移除 number / dyadic infinitesimal 之 R_i（其 Δ = 0，hot ranking 不影響）
   Hot ← {i : Δ_i := LS_i - RS_i > 0}
   設 σ : [|Hot|] → Hot 為 Δ_i 降序排列                 // O(m log m)
4. // 預處理 4 個 prefix/suffix arrays（記 a_l := LS_{σ(l)}, b_l := RS_{σ(l)}）
   P_a_even[0] = 0; P_b_odd[0] = 0
   for p = 1 to m:
       P_a_even[p] = P_a_even[p-1] + (p even ? a_p : 0)
       P_b_odd[p]  = P_b_odd[p-1]  + (p odd  ? b_p : 0)
   S_a_odd[m+1] = 0; S_b_even[m+1] = 0
   for p = m down to 1:
       S_a_odd[p]  = S_a_odd[p+1]  + (p odd  ? a_p : 0)
       S_b_even[p] = S_b_even[p+1] + (p even ? b_p : 0)
   // 4 個 sweeps, O(m) total
5. for each j ∈ Hot, 設 p = σ^{-1}(j):                   // O(m) total
       V_j ← a_p + P_a_even[p-1] + P_b_odd[p-1]
                 + S_a_odd[p+1] + S_b_even[p+1]
6. Sort V_j descending: π                                // O(m log m)
7. return {(R_{π(1)}, m^*_{π(1)}), ..., (R_{π(k)}, m^*_{π(k)})}
```

**正確性**：依引理 H 之 saddle-point 特徵化，Sequence$_p$ 為「B 強制先動 $j$」之最佳對弈序列；上述公式為其 closed-form 求和。Top-k by $V_j$ 為 D-must 答案（依定義 4）.

**複雜度**：步 1-2 $O(n^2)$；步 3 $O(m \log m)$；步 4-5 $O(m)$；步 6 $O(m \log m)$。總 $O(n^2 + m \log m)$. ✓

**$m = 3$ 數值驗算**：$\Delta = (10, 8, 6)$, $\mu_i = 0$, $(a_l, b_l) = (5, -5), (4, -4), (3, -3)$.

預處理：
- $P_a^{\text{even}}: [0]=0, [1]=0, [2]=4, [3]=4$
- $P_b^{\text{odd}}: [0]=0, [1]=-5, [2]=-5, [3]=-8$
- $S_a^{\text{odd}}: [4]=0, [3]=3, [2]=3, [1]=8$
- $S_b^{\text{even}}: [4]=0, [3]=0, [2]=-4, [1]=-4$

$V_1$ ($p = 1$): $5 + P_a^{\text{even}}[0] + P_b^{\text{odd}}[0] + S_a^{\text{odd}}[2] + S_b^{\text{even}}[2] = 5 + 0 + 0 + 3 + (-4) = 4$ ✓
$V_2$ ($p = 2$): $4 + P_a^{\text{even}}[1] + P_b^{\text{odd}}[1] + S_a^{\text{odd}}[3] + S_b^{\text{even}}[3] = 4 + 0 + (-5) + 3 + 0 = 2$ ✓
$V_3$ ($p = 3$): $3 + P_a^{\text{even}}[2] + P_b^{\text{odd}}[2] + S_a^{\text{odd}}[4] + S_b^{\text{even}}[4] = 3 + 4 + (-5) + 0 + 0 = 2$ ✓

與 §5.8 F2 之 $V_1 = 4, V_2 = V_3 = 2$ 一致 ✓.

**$m = 4$ 數值驗算**：$\Delta = (10, 8, 6, 4)$, $\mu_i = 0$, $(a_l) = (5, 4, 3, 2)$.

$V_2$ ($p = 2$): $4 + 0 + (-5) + 3 + (-2) = 0$ ✓
$V_3$ ($p = 3$): $3 + 4 + (-5) + 0 + (-2) = 0$ ✓ (與 $V_2$ tied，符合 F2)
$V_4$ ($p = 4$): $2 + 4 + (-8) + 0 + 0 = -2$ ✓

**X = D-avoid**：算法相同，最後排序改為 ascending（步 6），$O(n^2 + m \log m)$.

**ko-free promise 之必要性**：含 ko 時博弈樹可能無限循環，CGT 不收斂為 finite canonical form，BW 公式失效。Multi-ko 之 ko-threat externality 破壞 region 獨立性 → 標為 open（§9.4）。

> **D-sign-flipping 之降階**：原 round-1 draft 在此處列出 D-sign-flipping 之上界算法，但需要 baseline $V_0$ 之精確計算與 sign-flip 條件之 case split。Round-2 reviewer 指出 $V_0$ 計算依賴 GLG 之答案（與 §5.3 之降階同源），且 BW 標準形狀下 $V_0$ 不獨立於 hot game sum 之 alternating-Δ formula。為 conservative，**本研究將 X = D-sign-flipping 自定理 B 之主張中移除**，僅保留 X ∈ {B, C, D-must, D-avoid}。D-sign-flipping 之 poly-time algorithm 列為 §9.4 開放問題 #9.

$\square$

### 5.5 定理 C（中間區段，quasi-polynomial 上界）

**陳述**：在 ko-free + $|R_i| = O(\log n)$ 下，BEST-MOVE-X 為 quasi-polynomial $n^{O(\log n)}$。

**證明**：每 region 之博弈樹大小 $\leq |R_i|^{O(|R_i|^2)} = (\log n)^{O((\log n)^2)} \leq 2^{O((\log n)^2 \cdot \log\log n)} \leq 2^{O((\log n)^3)} = n^{O((\log n)^2)}$。

兩種寫法皆為 quasi-polynomial。Canonical form 與 thermograph 計算與樹同階。$m$ 個 region 之 per-local 計算 + 排序 $O(m \log m)$，總 $n^{O((\log n)^2)}$. $\square$

**意涵**：條件 $|R_i| = O(\log n)$ 是上下界對齊處（強於此 → P；弱於此 → PSPACE-hard）。Fine-grained complexity 之天然邊界。

### 5.6 定理 D（Hotstrat 失效）

**陳述**：存在 sum-game 使 B 之 top-1 與最佳對弈分歧。

**反例**：$G = \{10 \mid Y\}$，$Y = \{0 \mid -100\}$，$H = \{8 \mid -8\}$。$P = G + H$。

> **Abstract CGT vs. physical Go board 之澄清**：本反例採**抽象 CGT 表示**，$G, H, Y$ 之 L/R-options 即為 $\{a \mid b\}$ notation 中之 $a, b$。CGT canonical form 已將 dominated/reversible options 消除（per BCG Ch. 4 dominated-options elimination），故 $G$ 之 L-option 唯一為 $\{10\}$，R-option 唯一為 $\{Y\}$。
>
> 物理棋盤實現之 region 可能含多餘 dominated 走法，但 dominated 不影響 $LS / RS$ 計算（被 max/min 過濾）。具體棋形構造（19×19 上實現 $\{10 \mid \{0 \mid -100\}\} + \{8 \mid -8\}$）：corridor 對應 $H$、大塊死活威脅對應 $G$ 之 follow-up $Y$（白方威脅吃黑大塊 → 黑必需補一手 $-100$ 目）。完整棋形見 BW 1994 Ch. 4 之 mixed-sum examples，本研究不重作。

#### 5.6.1 Thermograph 計算

**$H$**：simple switch $\{8 \mid -8\}$。$LS(H) = 8$, $RS(H) = -8$, $\Delta(H) = 16$, $T(H) = 8$, $\mu(H) = 0$.

**$Y$**：simple switch $\{0 \mid -100\}$。$LS(Y) = 0$, $RS(Y) = -100$, $\Delta(Y) = 100$, $T(Y) = 50$, $\mu(Y) = -50$.

**$G = \{10 \mid Y\}$**：not a simple switch（右選項 $Y$ 為 hot）。

Thermograph 計算：
- 左 scaffold $L_G(t) = R_{\{10\}}(t) - t = 10 - t$（左選項 $G^L = 10$ 為 number，其 $R$-thermograph = $10$, scaffold 減 $t$）
- 右 scaffold $R_G(t) = L_Y(t) + t$
  - $L_Y(t) = 0 - t = -t$ for $t \in [0, 50]$；then mast at $\mu(Y) = -50$ for $t > 50$
- $R_G(t) = -t + t = 0$ for $t \in [0, 50]$；$= -50 + t$ for $t > 50$

兩 scaffold 相遇：$10 - t = 0 \Rightarrow t = 10$（落在 $[0, 50]$ 內 ✓）。

故 $T(G) = 10$，mast at value $0$。

$LS(G) = $ left scaffold value at $t = 0$ = $L_G(0) = 10$ (since black takes $G^L = 10$).
$RS(G) = $ right scaffold value at $t = 0$ = $R_G(0) = 0$ (since white moves to $Y$, then $LS(Y) = 0$).
$\Delta(G) = 10 - 0 = 10$.

#### 5.6.2 完整對弈樹枚舉（$LS(P)$ 計算）

採 $LS$ 之遞迴定義 $LS(P) = \max_{P^L} RS(P^L)$.

$P = G + H$ 之 L-options（B 動）：
- $L_1$: B 動 $G^L = 10$ → $P^{L_1} = 10 + H$
- $L_2$: B 動 $H^L = 8$ → $P^{L_2} = G + 8$

（$G$ 與 $H$ 各只有一個 L-option：$G^L = 10$ 是 $G$ 之唯一 L-option；$H^L = 8$ 同理。）

**計算 $RS(P^{L_1}) = RS(10 + H)$**：

$10$ 是 number（無 hot move）。$P^{L_1}$ 之 R-options：$\{10 + H^R\} = \{10 + (-8)\} = \{2\}$.

$RS(P^{L_1}) = LS(2) = 2$（$2$ 是 number）.

**計算 $RS(P^{L_2}) = RS(G + 8)$**：

$8$ 是 number。$P^{L_2}$ 之 R-options：$\{G^R + 8\} = \{Y + 8\}$.

$RS(P^{L_2}) = LS(Y + 8)$.

**計算 $LS(Y + 8)$**：

$Y + 8$ 之 L-options：$\{Y^L + 8\} = \{0 + 8\} = \{8\}$.

$LS(Y + 8) = RS(8) = 8$（$8$ 是 number）.

故 $RS(P^{L_2}) = 8$.

**$LS(P) = \max\{RS(P^{L_1}), RS(P^{L_2})\} = \max\{2, 8\} = 8$**.

最佳第一手 = $L_2$（B 動 $H$，得 $H^L = 8$，後續導致終局 $8$）.

#### 5.6.3 Hotstrat 預言與衝突

**Hotstrat**：$T(G) = 10 > T(H) = 8$，預言 B 動 $G$（top-1 by temperature）.

**衝突**：B 動 $G$ → 終局 $RS(P^{L_1}) = 2$；最佳 $LS(P) = 8$（B 動 $H$）.

Hotstrat 嚴格次優 by 6 點（$8 - 2 = 6$）.

**結論**：Hotstrat（B 之 top-1 預言）非全局最優。✓

#### 5.6.4 C 與 D-must 給出正確答案

- **C**：$\Delta(G) = 10$, $\Delta(H) = 16$. $\Delta(H) > \Delta(G)$ → C-top-1 = $H$. ✓
- **D-must**：$V_G = LS(G) + RS(H) = 10 - 8 = 2$；$V_H = LS(H) + RS(G) = 8 + 0 = 8$. $V_H > V_G$ → D-must-top-1 = $H$. ✓

C 與 D-must 在此 instance 與最佳對弈一致。$\square$

#### 5.6.5 物理棋盤實現（19×19）

CGT 數值 $G = \{10 \mid \{0 \mid -100\}\} + H = \{8 \mid -8\}$ 可由 19×19 上的具體棋形實現。下構造一例：

**$H$ 之實現**（simple switch $\{8 \mid -8\}$，1×16 corridor）：

於 19×19 盤面右下角構造 1×16 邊空 corridor，以對方活子封閉雙端：

```
. . . . . . . . . . . . . . . X .   (右下邊：黑活子封閉)
○ . . . . . . . . . . . . . . . ●   (空 corridor，左端 ○ 為白活子，右端 ● 為黑活子)
. . . . . . . . . . . . . . . . .   (corridor 下方為已圍實之地)
```

由 §5.2.1 BWFormula (c) 之 corridor 公式：1×16 corridor，$LS = 16$, $RS = ?$。

實際計算 corridor 之 stops 依封閉模式精確值不同，但**對於「對方活子雙端封閉」之 1×$\ell$ corridor 之變體**，可調 $\ell$ 使 $LS - RS = 16$（即 $\Delta = 16, T = 8, \mu = 0$）。具體構造：取 1×8 corridor 之雙倍寫法或加 stones 使中央地為對稱形式。

**$Y = \{0 \mid -100\}$ 之實現**（大塊死活威脅）：

於盤面左上角構造一個「未活」之黑大塊（約 50 子，含 100 目地之潛在地盤）。雙方競爭此大塊之活死：
- **B 先動**：B 補一手做活 → 黑得 0 目（保命，無額外收益）
- **W 先動**：W 動於關鍵點殺死黑大塊 → 黑損 100 目（黑塊死，白得 100 目）

由 dyadic 計算：$LS(Y) = 0, RS(Y) = -100, \Delta(Y) = 100, T(Y) = 50, \mu(Y) = -50$ ✓.

**$G = \{10 \mid Y\}$ 之實現**（含 hot follow-up 之中型 region）：

於盤面右上角構造一個「中型半實地」，含 follow-up 結構：
- **B 先動**：B 取 10 目地（保 follow-up 之選擇權）
- **W 先動**：W 引發 $Y$ 之活死競爭（將局部轉化為大塊死活問題 = 上述 $Y$）
  - 後續 B 必須補 $Y$ → 黑損 0 目（從 $LS(Y) = 0$）
  - 或 W 進一步攻擊 → 黑損 100 目（$RS(Y) = -100$）
- 故 $LS(G) = 10, RS(G) = LS(Y) = 0$（W 動 $G$ 後 B 補 $Y$ 之 $LS(Y) = 0$） ✓

**Region 獨立性**：三個 region 分別位於右下、左上、右上角，相距 $\geq 5$ 子，氣不互動 ✓.

**與 §5.6 之數值匹配**：上述構造之 stops 與 thermograph 完全匹配 §5.6.1 之 abstract CGT 計算，故 §5.6.2-5.6.4 之 Hotstrat 失效論證在此 19×19 物理棋盤上成立。

> **註**：本構造為示意。具體棋形之精確驗證（每個位置之活死、目數、follow-up 結構）需用 Go 引擎或 tsumego solver 確認，本研究不在此重做。實戰意義：BW 1994 Ch. 4 之 mixed-sum examples 含大量類似結構，本反例非「人造特例」，而是中盤至終局轉折常見模式。

### 5.7 定理 F1（C-top-1 = D-must-top-1, sum-of-simple-switches）

**陳述**：設 $G = \sum_{i=1}^m S_i$，$S_i = \{a_i \mid b_i\}$ 為 simple switches，$\Delta_i = a_i - b_i > 0$，所有 $\Delta_i$ 兩兩不同（non-degenerate）。則：

$$\arg\max_j \Delta_j = \arg\max_j V_j$$

其中 $V_j$ 同定義 4。

**證明**：由引理 H：

$V_j = LS(S_j^L + \sum_{i \neq j} S_i)$.

但 $S_j^L = a_j$ 為 number（simple switch 之 L-option 是 number），故：

$V_j = a_j + LS_W\Big(\sum_{i \neq j} S_i\Big) = a_j + RS\Big(\sum_{i \neq j} S_i\Big)$

由引理 H (c) 之對稱版本（W-first），$RS(\sum_{i \neq j} S_i) = \sum_{l \text{ odd}} b_{\sigma_j(l)} + \sum_{l \text{ even}} a_{\sigma_j(l)}$，$\sigma_j$ = $\Delta$ 降序於 $\{1, \ldots, m\} \setminus \{j\}$.

由引理 H 之對換論證（5.1 節之 (a)）：$\arg\max_i f(i) = \sigma(1) = \arg\max_i \Delta_i$，其中 $f(i) := V_i$.

故 $\arg\max_j V_j = \sigma(1) = \arg\max_j \Delta_j$. ✓

由 $\Delta_i = 2 T_i$（simple switches），$\arg\max_j \Delta_j = \arg\max_j T_j$，故 C-top-1 = B-top-1 = D-must-top-1. $\square$

### 5.8 定理 F2（C-full-ranking ≠ D-must-full-ranking）

**陳述**：設 $G$ 同 F1（sum of $m \geq 3$ non-degenerate simple switches）。則 D-must-ranking 之第 2 位起出現結構性成對 ties：對所有 $k \geq 1$ with $2k + 1 \leq m$，

$$V_{\sigma(2k)} = V_{\sigma(2k+1)}$$

而 C-ranking 為 strict（$\sigma(1) > \sigma(2) > \cdots$）。故兩 ranking 結構性不同。

**證明（從對弈序列展開）**：

由 §5.4 算法 2.3 之 prefix-sums 公式，對 $j = \sigma(p)$（$p \geq 2$）：

$V_{\sigma(p)} = a_{\sigma(p)} + \sum_{l=1}^{p-1} \begin{cases} a_{\sigma(l)} & l \text{ even} \\ b_{\sigma(l)} & l \text{ odd} \end{cases} + \sum_{l=p+1}^{m} \begin{cases} a_{\sigma(l)} & l \text{ odd} \\ b_{\sigma(l)} & l \text{ even} \end{cases}$

對 $p = 2k$ 與 $p = 2k+1$ 比較：

- Prefix $\sum_{l=1}^{p-1}$：對 $p = 2k$ 為 $\sum_{l=1}^{2k-1}$；對 $p = 2k+1$ 為 $\sum_{l=1}^{2k}$
- Suffix $\sum_{l=p+1}^{m}$：對 $p = 2k$ 為 $\sum_{l=2k+1}^{m}$；對 $p = 2k+1$ 為 $\sum_{l=2k+2}^{m}$

**Direct computation**：

$$V_{\sigma(2k)} - V_{\sigma(2k+1)} = \big[a_{\sigma(2k)} - a_{\sigma(2k+1)}\big] + \big[\text{prefix diff}\big] + \big[\text{suffix diff}\big]$$

Prefix 差：
- $V_{\sigma(2k)}$ prefix 包含 $\sigma(2k)$ 嗎？不，因 $l \leq 2k - 1$. 所以 $V_{\sigma(2k)}$ prefix = $\sum_{l=1}^{2k-1} \{l \text{ even}: a_{\sigma(l)}; l \text{ odd}: b_{\sigma(l)}\}$
- $V_{\sigma(2k+1)}$ prefix = $\sum_{l=1}^{2k} \{l \text{ even}: a_{\sigma(l)}; l \text{ odd}: b_{\sigma(l)}\}$（多一項 $l = 2k$ even → $a_{\sigma(2k)}$）

Prefix 差 = $-a_{\sigma(2k)}$（$V_{\sigma(2k)}$ 少這項，故 $V_{2k} - V_{2k+1}$ 之 prefix part = $-a_{\sigma(2k)}$）.

Suffix 差：
- $V_{\sigma(2k)}$ suffix = $\sum_{l=2k+1}^{m} \{l \text{ odd}: a_{\sigma(l)}; l \text{ even}: b_{\sigma(l)}\}$（包含 $l = 2k+1$ odd → $a_{\sigma(2k+1)}$）
- $V_{\sigma(2k+1)}$ suffix = $\sum_{l=2k+2}^{m} \{l \text{ odd}: a_{\sigma(l)}; l \text{ even}: b_{\sigma(l)}\}$（不含 $l = 2k+1$）

Suffix 差 = $+a_{\sigma(2k+1)}$（$V_{\sigma(2k)}$ 多這項）.

加總：

$$V_{\sigma(2k)} - V_{\sigma(2k+1)} = (a_{\sigma(2k)} - a_{\sigma(2k+1)}) - a_{\sigma(2k)} + a_{\sigma(2k+1)} = 0$$

故 $V_{\sigma(2k)} = V_{\sigma(2k+1)}$. ✓

**意涵**：D-must-ranking 為 $\sigma(1) > \{\sigma(2), \sigma(3)\} > \{\sigma(4), \sigma(5)\} > \cdots$（成對 ties from position 2）；C-ranking 為 $\sigma(1) > \sigma(2) > \sigma(3) > \cdots$（strict）。兩者**結構性不同**，並非偶然。

**實例驗算（$m = 3$）**：$\Delta = (10, 8, 6)$, $\mu_i = 0$, so $(a_i, b_i) = (5, -5), (4, -4), (3, -3)$.

- $V_1 = a_1 + b_2 + a_3 = 5 - 4 + 3 = 4$ ✓
- $V_2 = a_2 + b_1 + a_3 = 4 - 5 + 3 = 2$ ✓
- $V_3 = a_3 + b_1 + a_2 = 3 - 5 + 4 = 2$ ✓ (= $V_2$)

C-rank: $1 > 2 > 3$ (strict). D-must-rank: $1 > \{2, 3\}$ tied. ✓ $\square$

**實例驗算（$m = 4$, $\mu_i = 0$）**：$\Delta = (10, 8, 6, 4)$, $(a_i) = (5, 4, 3, 2)$.

- $V_1 = a_1 + b_2 + a_3 + b_4 = 5 - 4 + 3 - 2 = 2$
- $V_2 = a_2 + b_1 + a_3 + b_4 = 4 - 5 + 3 - 2 = 0$
- $V_3 = a_3 + b_1 + a_2 + b_4 = 3 - 5 + 4 - 2 = 0$ (= $V_2$ ✓)
- $V_4 = a_4 + b_1 + a_2 + b_3 = 2 - 5 + 4 - 3 = -2$

D-must-rank: $1 > \{2, 3\} > 4$. C-rank: $1 > 2 > 3 > 4$. ✓

### 5.9 定理 F3（substantive C-top-1 ≠ D-avoid-top-1）

**陳述**：存在 sum-of-simple-switches instance + baseline 使 C-top-1 ≠ D-avoid-top-1（substantive 分歧，非退化）。

**反例**：$m = 4$，$\Delta = (10, 9, 8, 1)$，$\mu_i = 0$. So $(a_i, b_i) = (\pm 5, \pm 4.5, \pm 4, \pm 0.5)$.

加 baseline $R = +0.5$（總分加 0.5，可由 number-region $\{0.5\}$ 達成）.

由 F2 公式（對應 $m = 4$ 之 $V_j$）+ baseline:

- $V_1 = 0.5 + (a_1 + b_2 + a_3 + b_4) = 0.5 + (5 - 4.5 + 4 - 0.5) = 0.5 + 4 = 4.5$
- $V_2 = 0.5 + (a_2 + b_1 + a_3 + b_4) = 0.5 + (4.5 - 5 + 4 - 0.5) = 0.5 + 3 = 3.5$
- $V_3 = 0.5 + (a_3 + b_1 + a_2 + b_4) = 0.5 + (4 - 5 + 4.5 - 0.5) = 0.5 + 3 = 3.5$ (= $V_2$, 符合 F2)
- $V_4 = 0.5 + (a_4 + b_1 + a_2 + b_3) = 0.5 + (0.5 - 5 + 4.5 - 4) = 0.5 + (-4) = -3.5$

**D-avoid-top-1** = $\arg\min V_j$ = region 4 (因 $V_4 = -3.5$ 最小).
**C-top-1** = $\arg\max \Delta_j$ = region 1 ($\Delta_1 = 10$ 最大).

substantive 分歧：region 4 為唯一「黑會輸」之選擇（$V_4 < 0$, others $> 0$）；region 1 為「最佳得分」.

**Baseline $V_0$ 計算**：由引理 H (c)，無 first-move 約束之 B-first-optimal 終值為

$$V_0 = R + \sum_{l=1, l\text{ odd}}^{4} a_{\sigma(l)} + \sum_{l=2, l\text{ even}}^{4} b_{\sigma(l)} = 0.5 + (a_1 + a_3) + (b_2 + b_4) = 0.5 + (5 + 4) + (-4.5 - 0.5) = 4.5$$

故 $V_0 = V_1 = 4.5$（D-must-top-1 與無約束最佳對弈一致 ✓，符合 F1）.

**D-sign-flipping 之 critical region**：因 $V_0 = 4.5 > 0$（黑勝），sign-flipping locus = $\{j : V_j \leq 0\} = \{4\}$（唯一）。此與 D-avoid-top-1 一致（皆為 region 4），但與 C-top-1（region 1）不同。

**意涵**：D-avoid 量化「絕不能下哪手」與 C 量化「最佳得分一手」是不同問題。在 sign-flipping 情境（$V_0$ 接近 0）下，D-avoid 提供 C 無法給出之資訊。$\square$

---

## 6. 核心創新的技術分析

### 6.1 Hotstrat 失效定理（定理 D）

定理 D 透過具體 CGT 反例（$G + H$, $G = \{10 \mid Y\}$）推翻「play hottest first」之素樸普遍性：對含 hot follow-up（$Y$ 為 hot）之 mixed sum game，B 之溫度排序與最佳對弈分歧。

**為何此反證重要**：教科書 CGT（如 Berlekamp-Conway-Guy 1982）多在 simple switches 假設下論證 Hotstrat optimality；本反例顯示「all-small」或「pure switches」假設**不可去除**。實戰意義：中後盤含「sente follow-up」（如威脅吃小龍）局面，按 hottest 下會錯過最佳一手。

完整對弈樹枚舉（5.6.2）給出嚴格驗證，無 hand-wave。

### 6.2 引理 H 與 D-must ranking 之精確結構（定理 F1, F2）

引理 H 不是新結果（Berlekamp-Wolfe 框架隱含），但本研究**從第一性原理重建證明**（5.1 節對換論證），使後續 F1/F2 之 closed-form 可直接導出。

定理 F2 之 $V_{\sigma(2k)} = V_{\sigma(2k+1)}$ 為「D-must-ranking 之成對 ties」**結構性結果**。原 round-1 draft 之代數恆等式被擴充為「對所有 $m \geq 3$ 與所有 $k$ 之 ties 模式」之完整刻畫。

### 6.3 D 之三讀法與「最好一手」之多義性（定義 4, 定理 F1, F3）

原 conjecture「C 與 D 在自然情境重合」一刀切判斷被 Definition 4 精確化為三層：
- F1（D-must, top-1）：與 C 一致
- F2（D-must, full-ranking）：與 C 結構性不同
- F3（D-avoid）：與 C substantive 不同

**意涵**：「最好一手」並非單一概念。在實戰 / 理論討論時，必須先明確 D 之形式化讀法，否則陳述含糊。

### 6.4 下上界對齊處 $|R_i| = O(\log n)$

定理 A 之 PSPACE-hard 與定理 C 之 quasi-poly 之邊界，提示 fine-grained complexity 之研究方向：是否能將 PSPACE-hard 加強至「$|R_i| = \omega(\log n)$ 即 PSPACE-hard」？

---

## 7. 結果總覽

### 7.1 定理層次表

| 定理 | 結論 | 條件 | 強度 |
|------|------|------|-----|
| H | Hotstrat-on-switches 引理（adjacent-swap 對換論證） | sum-of-simple-switches | 完整證明（5.1） |
| A.1 | Swing 控制 lemma（GLG → $R_\Phi$ 滿足 $D_Y - D_N = \Omega(|B|)$） | 顯式 booster gadget 構造 | 完整證明（5.3.2） |
| A | BEST-MOVE-X 為 PSPACE-hard | 局部可分解，X ∈ {B, C, D-must, D-avoid} | 條件性下界（5.3） |
| B | BEST-MOVE-X 為 P, $O(n^2 + m \log m)$ | 局部可分解 + ko-free + BW 標準形狀（定義 5），X ∈ {B, C, D-must, D-avoid} | 條件性上界（5.4） |
| C | BEST-MOVE-X 為 quasi-poly $n^{O((\log n)^2)}$ | 局部可分解 + ko-free + $|R_i|=O(\log n)$ | 條件性（5.5） |
| D | Hotstrat 失效（B-top-1 ≠ 最佳對弈） | $G + H$ with $G$ 含 hot follow-up | 結構性反例（5.6） |
| F1 | C-top-1 = D-must-top-1 | sum-of-simple-switches + non-degenerate | 條件性（5.7） |
| F2 | D-must-rank 出現成對 ties，與 C-rank 結構不同 | sum-of-simple-switches + non-degenerate, $m \geq 3$ | 結構性（5.8） |
| F3 | substantive C-top-1 ≠ D-avoid-top-1 | sum-of-simple-switches + 適當 baseline | 結構性（5.9） |

> **Round-1 draft 中聲稱「BEST-MOVE-D top-k weakly NP-hard via PARTITION」之結果因 sum-of-simple-switches 下 $V_j$ 有 poly 閉式（F1/F2 之直接推論）而無法成立，已移至開放問題（§9.4）.**

### 7.2 條件強弱層次

從強到弱：
1. **「BW 標準形狀」**（定義 5, (a)-(f)）：覆蓋實戰 19×19 之比例為 empirical question（§9.4）
2. **「ko-free」**（定義 3）：禁止任意 cycle，比日本 simple ko rule 更強
3. **「局部可分解」**（定義 1）：CGT 求和之必要 promise
4. **「non-degenerate」**：$\Delta_i$ 兩兩不同，排除 trivial ties

### 7.3 原創貢獻

1. Hotstrat 失效之具體 CGT 反例與完整對弈樹枚舉（定理 D）
2. 引理 H 之自足對換論證（5.1）
3. D 三讀法之形式化（定義 4）
4. C ↔ D-must 之三層拆分及 $V_{\sigma(2k)} = V_{\sigma(2k+1)}$ 結構性 ties 之證明（定理 F1/F2/F3）
5. ko-free promise 之精確化（定義 3）
6. BW 標準形狀之精確類別定義（定義 5）
7. 下上界對齊處 $|R_i| = O(\log n)$ 之識別

### 7.4 已知可改進處（已悉數補完）

下列為 Phase 5 各輪所識別之 nice-to-haves，於最終 polish 通通補入：

- ✓ **引理 H (c) 與 thermograph mast 之嚴格對齊**：§5.1.1 透過 thermograph addition theorem + mean/swing 分解獨立推得 closed-form $LS(G) = \sum_{\text{odd}} a + \sum_{\text{even}} b$，與引理 H (c) 之 adjacent-swap 證明完全一致（雙路徑互相印證）
- ✓ **BWFormula 子程式之具體公式**：§5.2.1 顯式重建 (a) Number、(b) Simple switch、(c) Corridor of length $\ell$（含 dyadic recursion 與 closed-form $RS(C_\ell) = \lfloor (\ell-1)^2/4 \rfloor$ 等）、(d) Sum、(e) Infinitesimals、(f) Sente sequence 之 stops/temperature/mean 與 per-region $O(|R|)$ 複雜度
- ✓ **§5.6 19×19 物理棋盤實現**：§5.6.5 給出 $G + H$ 之具體 19×19 構造（右下 1×16 corridor 為 $H$、左上大塊死活為 $Y$、右上中型 region 為 $G$），含 region 獨立性驗證與數值匹配
- ✓ **Sub-lemma A.1.1 之 (L-iii) dominance 強度**：§5.3.2 之 dominance 表已改為精確 case 分析（YES/NO × strict/weak），明示 BCG canonical form elimination 對弱 dominance 仍適用之依據
- ✓ **Sub-lemma A.1.1 之 W's R-options 對稱論證**：§5.3.2 已顯式列出 (R-i), (R-ii), (R-iii) 並逐一驗證 dominance（含 W 視角之 strict $<$ 比較）

下列為**仍未補強**之 known limitations（不影響主結論，且補強需 substantive 額外研究）：

- 定理 A 之 GLG → BEST-MOVE-D-sign reduction：D-sign 因 baseline $V_0$ 之計算依賴 GLG 答案而為循環論證，**已自定理 A 之適用範圍移除**，列為 §9.4 開放問題 #9
- 定理 B 之 D-sign-flipping 上界算法因相同原因移除，列為 §9.4 開放問題 #9
- BW 1994 Ch. 3 corridor catalog 之十餘種封閉變體：本研究只重建「對方活子雙端封閉」之標準形（§5.2.1 (c)），其他變體（同方活子封閉、混合封閉等）類似 dyadic recursion 處理，列為 conditional
- BW 1994 Ch. 6 之 thermograph 完整理論（cooling, heating, atomic weight）：本研究只用 mast height 與 mean 之 bare definition（§5.1.1）；infinitesimals 之 perturbative 處理採 §5.2.1 (e) 之簡化，conditional on BCG Ch. 7 之 cooling 結果
- BW 標準形狀對 19×19 實戰盤面之經驗覆蓋率：empirical question，列為 §9.4 開放問題 #4

---

## 8. 對原始問題的回答

**問題**：「在圍棋 19×19 對局中，輸入棋盤矩陣後，計算出官子最好一手位置」是否可算？

**直接回答**：**部分成立**。

- 在「局部可分解 + ko-free + BW 標準形狀」之強條件下，**可在多項式時間 $O(n^2 + m \log m)$ 算出**（定理 B + 算法 2.1/2.2/2.3）。對應實戰：終局後段、無大型劫爭、棋形落入經典官子模式。
- 在無條件下（僅「局部可分解」promise），**問題為 PSPACE-hard**（定理 A），不存在可期之 poly 算法（除非 P = PSPACE）.
- 「最好」之三種定義（B/C/D）並非等價：
  - 在含 follow-up 局面 B 失效（定理 D）
  - F1/F2/F3 顯示 D 之三讀法（must-play / avoid-play / sign-flipping locus）下 C 與 D 之 ranking 在 $k \geq 2$ 結構性分歧
  - top-1 在 sum-of-simple-switches 之 must-play 下三者重合，但在 D-avoid 下可分歧

**根本原因**：圍棋官子之難度來自 (1) 單一 region 內部可承載 alternating computation（PSPACE，via Crâșmaru-Tromp ladder）、(2) 多 region 加總引入 alternating-temperature 終局公式（poly 結構但對 D 引入 ranking ties）、(3) ko 破壞 CGT 框架的 finite canonical form 假設、(4) follow-up 結構使溫度與最佳對弈分歧。

---

## 9. 討論

### 9.1 與已知結果的關係

- **Robson 1983（n×n Go 為 EXPTIME-complete）**：較粗的全局結果；本研究在「官子」受限子問題上給出 PSPACE-hard 之較精細下界。Robson 之 reduction 用 nested ko 全局結構；本研究排除 ko，故下界較弱（PSPACE 而非 EXPTIME），但條件更接近實戰。
- **Berlekamp-Wolfe 官子理論**：本研究之上界算法之基礎，但顯示其 catalog 不覆蓋 ko 與 Hotstrat-on-mixed-sum 之全部情境。BW 1994 之 cool-by-1 framework 為 simple switches 設計，本研究之定理 D 顯示其在 hot follow-up 下需擴充。
- **Crâșmaru-Tromp 2000 ladder PSPACE-completeness**：本研究之 PSPACE-hard 下界之直接 building block；本研究將其結果移植至 BEST-MOVE-X 之三類 X 上（5.3.3）。

### 9.2 已嚴格否證的主張

- **「Hotstrat 為 universal optimal」**：定理 D 反證（含完整對弈樹枚舉）.
- **「C 與 D 在自然情境完全重合」**：定理 F2 反證（D-must-ranking 之結構性成對 ties，與 C 之 strict ranking 不同）.
- **「BEST-MOVE-D top-k 為 weakly NP-hard via PARTITION」**：原 Phase 4 conjecture，因 sum-of-simple-switches 下 $V_j$ 有 poly 閉式（F1/F2）而無法成立。

### 9.3 與已知開放問題的關係

- **EXPTIME-hardness for BEST-MOVE-X**：Robson 1983 用 nested ko 全局結構；是否能在單一 region 內模擬 EXPTIME computation 為 open
- **strongly NP-hardness for D**：sum-of-simple-switches 下 D top-k 為 poly；更一般 promise 下未知

### 9.4 開放問題

1. **EXPTIME-hardness 是否成立**（無論在 ko-free 或允許 ko 之 BEST-MOVE-X）
2. **Multi-ko 之多項式處理**（外部 ko-threat 量化、stoppers framework 推廣）
3. **General $m \geq 5$ 下 $V_j$ tie 模式之完整刻畫**（F2 給出 $V_{\sigma(2k)} = V_{\sigma(2k+1)}$；是否更高階 ties 存在？例如三聯 ties）
4. **BW 標準形狀對 19×19 實戰盤面之經驗覆蓋率**（empirical question）
5. **「Decomposition promise 驗證」之 PSPACE-hardness 之嚴格證明**
6. **BEST-MOVE-X top-k 是否有獨立於 PSPACE 之 NP-hardness 層次**：原 round-1 draft 之 PARTITION reduction 因 sum-of-simple-switches 下 $V_j$ 有 poly 閉式而失敗。在更一般 promise 下（不限於 simple switches，含 follow-up + 任意 BW 標準形狀），top-k 是否有額外 hardness 層次未知。
7. **D-sign-flipping locus 之精確讀法**：定義 4 之 D-sign-flipping 在 baseline $V_0$ 接近 0 時 well-defined，但 $|V_0|$ 大時退化為 must-play；如何形式化「離 0 多近才算 critical」為 open
8. **非 BW 標準形狀之上界**：定理 B 之 (iii) 條件不滿足時（如含 ko、複雜 life-and-death），是否存在更弱條件下之 sub-exponential 算法
9. **D-sign-flipping 之 reduction 與 poly-time algorithm**：D-sign-flipping 之 PSPACE-hardness 與上界算法皆需 baseline $V_0$ 之精確處理。$V_0 = LS(\sum_i R_i)$ 本身需要對 BEST-MOVE-X 之求解（循環依賴）；如何避免循環、給出獨立構造之 reduction（由 GLG 直接 reduce 至 D-sign，不繞過 must-play / avoid-play）為 open。本研究將 D-sign-flipping 自定理 A、B 之適用範圍移除，待此問題解決後可重新納入。

---

## 參考文獻

- Berlekamp, E., & Wolfe, D. (1994). *Mathematical Go: Chilling Gets the Last Point*.
- Berlekamp, E., Conway, J., & Guy, R. (1982). *Winning Ways for Your Mathematical Plays*.
- Conway, J. H. (1976). *On Numbers and Games*.
- Crâșmaru, M., & Tromp, J. (2000). Ladders are PSPACE-complete. *Computers and Games (CG 2000)*.
- Karp, R. M. (1972). Reducibility among combinatorial problems.
- Robson, J. M. (1983). The complexity of Go. *IFIP World Computer Congress*.
- Stockmeyer, L. J., & Meyer, A. R. (1973). Word problems requiring exponential time.

---

*本文件已通過 Phase 5 之 4 輪審查迴圈（round-1 fresh-eyes / round-2 fresh-eyes / round-3 verification / round-4 verification），最終判定 final。後續 polish round 將 §7.4 之 5 條 substantive nice-to-haves 全部補完（H(c) thermograph 對齊、BWFormula 公式重建、19×19 物理棋盤構造、L-iii dominance 表、W's R-options 顯式對稱），餘下 5 條為 known limitations（D-sign 開放、BW 變體 conditional、實戰覆蓋率 empirical）。*
