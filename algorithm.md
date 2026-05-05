# 乾淨官子下最佳一手計算之解法（generic $n \times n$）

> 從 proof.md §5.4 抽出之實作層級算法。本文件對應 proof 之**定理 B**（受限上界）的具體執行步驟。
>
> **參數化**：算法以 $n$（盤面邊長）為輸入參數，**不限定於 19×19**。19×19 為其 special instance，n×n 漸近分析與 generic implementation 同源（per formalization.md §3.1 與 attack-spec.md 區塊三）。

---

## 命題（precondition）

設 $n \in \mathbb{N}$（盤面邊長，$n \geq 2$），盤面 $s \in \{B, W, \emptyset\}^{n \times n}$ 滿足以下三個 promise：

1. **(P1) 局部可分解**：$s$ 之空點區塊 $\{R_1, \ldots, R_m\}$ 兩兩不共享氣，無跨區劫爭。
2. **(P2) ko-free**：每個 $R_i$ 之局部博弈樹無同形反覆。
3. **(P3) BW 標準形狀**：每個 $R_i$ 之 canonical form 屬於下列六類之一（或為其和）：
   - **(a) Number**：純空點地，無爭議
   - **(b) Simple switch** $\{a \mid b\}$：兩種先動結局已知
   - **(c) Corridor** 1×$\ell$：標準封閉之邊空
   - **(d) Sum**：上述之 disjoint 組合
   - **(e) Dyadic infinitesimal**：$\{*, \uparrow, \downarrow, \ldots\}$
   - **(f) Finite sente sequence**：強制對弈終於 (a) 或 (b)

**結論**：BEST-MOVE-X 可在 $O(n^2 + m \log m)$ 時間內計算，X ∈ {B, C, D-must, D-avoid}。

**參數說明**：
- $n$：盤面邊長（自由參數）。標準圍棋 $n = 19$；mini Go $n = 9$ 或 13；理論討論之漸近 $n \to \infty$
- $m$：region 數量，$m \leq O(n^2)$（最壞每個空點獨立一塊）；實戰中 $m \ll n^2$
- 算法本身**不依賴 $n$ 之具體值**，純粹以 $n^2$（盤面格點數）與 $m$ 為參數

---

## 算法總覽

三階段流水線：

```
盤面 s → [Phase 1: Decompose] → {R_1, ..., R_m}
                                     ↓
                                [Phase 2: BWFormula per R_i]
                                     ↓
                              {(LS_i, RS_i, T_i, μ_i, m^*_i)}
                                     ↓
                                [Phase 3: Aggregate by X]
                                     ↓
                                  Top-k 最佳一手
```

---

## Phase 1：盤面分解

**輸入**：$n \times n$ 棋盤矩陣 $s \in \{B, W, \emptyset\}^{n \times n}$（$n$ 為自由參數）

**輸出**：region 集合 $\{R_1, \ldots, R_m\}$，每個 $R_i$ 為「空點 cluster + 邊界石」

**算法**：

```
1. 對所有空點建立 union-find；同 chain 合併（4-連通）。
2. 對每個 connected empty component E_j：
   2a. 收集 E_j 周邊所有相鄰 boundary stones B_j
   2b. R_j ← (E_j, B_j)
3. 驗證 promise (P1)：對每對 R_i ≠ R_j：
   - R_i ∩ R_j = ∅（disjoint）
   - 對 R_i 之邊界石之外部氣，不應屬於另一 R_j
   - 若違反 → return "promise violated, algorithm not applicable"
4. 返回 {R_1, ..., R_m}
```

**複雜度**：$O(n^2)$（union-find 對 $n^2$ 格點 + 邊界檢查）.

---

## Phase 2：Per-region BWFormula

對每個 $R_i$，分類至 (a)-(f) 之一，計算 $(LS_i, RS_i, T_i, \mu_i, m^*_i)$。

### (a) Number

**識別**：$R_i$ 之空點完全被同一色棋子圍繞（已成定地）。

**公式**：
- $v \leftarrow$ count(空點) – count(對方仍可侵入處)（依日本規則計算地）
- $LS_i = RS_i = v$
- $T_i = 0$
- $\mu_i = v$
- $m^*_i = \perp$（無動）

**複雜度**：$O(|R_i|)$（簡單計數）

### (b) Simple switch $\{a \mid b\}$

**識別**：$R_i$ 之關鍵點唯一，B 動或 W 動分別導致兩種 forced 結局，無中間 follow-up。

**算法**：
```
key_point ← R_i 中之唯一 hot 點（兩方都想搶）
a ← simulate(R_i 從 key_point 開始 B 先動)（forced 至終局，計算地）
b ← simulate(R_i 從 key_point 開始 W 先動)
LS_i ← a; RS_i ← b
T_i ← (a - b) / 2
μ_i ← (a + b) / 2
m^*_i ← key_point
```

**複雜度**：$O(|R_i|)$（兩次 forced simulation）

### (c) Corridor 1×$\ell$

**識別**：$R_i$ 為單行邊空，雙端被對方活子封閉，無內部爭議。

**Closed-form 公式**（從 BW 1994 Ch. 3 之 dyadic recursion 重建）：
- $LS_i = \ell$（B 取整 corridor）
- $RS_i = \lfloor (\ell - 1)^2 / 4 \rfloor$
- $T_i = (LS_i - RS_i) / 2$
- $\mu_i = (LS_i + RS_i) / 2$
- $m^*_i = $ corridor 之開放端進占點（push）

**驗算**：

| $\ell$ | $LS$ | $RS$ | $\Delta = LS - RS$ | $T$ |
|--------|------|------|-------------------|-----|
| 1 | 1 | 0 | 1 | 0.5 |
| 2 | 2 | 0 | 2 | 1 |
| 3 | 3 | 1 | 2 | 1 |
| 4 | 4 | 2 | 2 | 1 |
| 5 | 5 | 4 | 1 | 0.5 |
| 6 | 6 | 6 | 0 | 0 |
| 7 | 7 | 9 | -2 | (cold) |

> **註**：$\ell \geq 6$ 起 $LS \leq RS$，corridor 已 collapsed 為 number；$T = 0$，B/W 先動皆無利。

**複雜度**：$O(1)$（直接公式）

### (d) Sum / disjoint composition

**識別**：$R_i = R_{i,1} \sqcup R_{i,2}$，兩子 region 無互動。

**算法**：遞迴 + sum 之 stops。

```
(LS_{i,1}, RS_{i,1}, ...) ← BWFormula(R_{i,1})
(LS_{i,2}, RS_{i,2}, ...) ← BWFormula(R_{i,2})
// 兩子 region 之 stops 用引理 H 之 alternating-Δ 公式合併
LS_i, RS_i ← compose_stops((LS_{i,1}, RS_{i,1}), (LS_{i,2}, RS_{i,2}))
T_i ← (LS_i - RS_i) / 2
μ_i ← (LS_i + RS_i) / 2
m^*_i ← argmax over {m^*_{i,1}, m^*_{i,2}} by sub-T
```

**複雜度**：$O(|R_i|)$（攤分）

### (e) Dyadic infinitesimal $R_i \in \{*, \uparrow, \downarrow, \uparrow*, \cdots\}$

**識別**：$R_i$ 為小型平衡局部（如 dame 對峙、雙方都不想動之 tedomari）。

**公式**：
- $LS_i = RS_i = 0$
- $T_i = 0$
- $\mu_i = 0$
- 標記 type（影響 tiebreaking but not top-k for hot games）

**複雜度**：$O(1)$

### (f) Finite sente sequence

**識別**：$R_i$ 之第一手為 sente（forced response），最終收斂為 (a) 或 (b)。

**算法**：
```
simulate forced sequence from R_i
collect accumulated score along the way
terminal_R ← 最終 region 形態
(LS_term, RS_term, ...) ← BWFormula(terminal_R)  // 遞迴
LS_i ← LS_term + (forced sequence 中 B 之累計得分)
RS_i ← RS_term + (forced sequence 中 W 之累計得分)
T_i, μ_i ← 由 LS_i, RS_i 推得
m^*_i ← sente 之第一手座標
```

**複雜度**：$O(|R_i|)$（sequence 長度有限）

---

## Phase 3：依 X 排序與選 top-k

依用戶選定的「最好」定義 X，分支處理。

### X = B（溫度最優，即 Hotstrat）

```
Sort {R_i} by T_i descending → π
return [(R_{π(1)}, m^*_{π(1)}), ..., (R_{π(k)}, m^*_{π(k)})]
```

**複雜度**：$O(m \log m)$

### X = C（得分增益最優）

```
for each R_i: Δ_i ← LS_i - RS_i
Sort {R_i} by Δ_i descending → π
return top-k
```

**複雜度**：$O(m \log m)$

> **註**：對 simple switch，$\Delta_i = 2 T_i$，故 X = B 與 X = C 之 ranking 一致。對含 follow-up 之 region 兩者可不同（見定理 D 之反例）。

### X = D-must（黑該下哪手最有利，prefix-sums 加速版）

「黑強制先動 $R_j$ 之後雙方最佳對弈」之終局值 $V_j$ 由引理 H 給出 closed-form：

```
// 預處理
σ ← {R_i} 按 Δ_i = LS_i - RS_i 降序排列
記 a_l := LS_{σ(l)}, b_l := RS_{σ(l)}

// 4 個 prefix/suffix arrays（base cases: P_*[0] = 0, S_*[m+1] = 0）
P_a_even[0] ← 0; P_b_odd[0] ← 0
for p = 1 to m:
    P_a_even[p] ← P_a_even[p-1] + (p even ? a_p : 0)
    P_b_odd[p]  ← P_b_odd[p-1]  + (p odd  ? b_p : 0)
S_a_odd[m+1] ← 0; S_b_even[m+1] ← 0
for p = m down to 1:
    S_a_odd[p]  ← S_a_odd[p+1]  + (p odd  ? a_p : 0)
    S_b_even[p] ← S_b_even[p+1] + (p even ? b_p : 0)

// V_j 之 closed form (依引理 H 之對弈序列展開)
for each j ∈ [m]:
    p ← σ^{-1}(j)
    V_j ← a_p + P_a_even[p-1] + P_b_odd[p-1] + S_a_odd[p+1] + S_b_even[p+1]

Sort {V_j} descending → π
return [(R_{π(1)}, m^*_{π(1)}), ..., (R_{π(k)}, m^*_{π(k)})]
```

**複雜度**：$O(m \log m)$（排序兩次 + prefix/suffix sum 為 $O(m)$）

> **特性**（定理 F2）：$V_{σ(2k)} = V_{σ(2k+1)}$ 必然出現結構性成對 ties。即「top-1 唯一，但 top-2 與 top-3 一定 tied」（在 non-degenerate 假設下）.

### X = D-avoid（黑絕不能下哪手）

同 D-must 之計算，最後排序改為 **ascending**：
```
Sort {V_j} ascending → π
return [(R_{π(1)}, m^*_{π(1)}), ..., (R_{π(k)}, m^*_{π(k)})]
```

---

## 總複雜度

| Phase | 複雜度 |
|-------|--------|
| 1. Decompose | $O(n^2)$ |
| 2. Per-region BWFormula | $O(\sum |R_i|) = O(n^2)$ |
| 3. Aggregate (X = B / C) | $O(m \log m)$ |
| 3. Aggregate (X = D-must / D-avoid) | $O(m \log m)$ |
| **Total** | $O(n^2 + m \log m)$ |

**典型實例之數量級**（algorithm 本身泛用，不依賴特定 $n$）：

| $n$ | 用途 | $n^2$ | 典型 $m$ | wall-clock（CPython 估計） |
|-----|------|-------|---------|--------------------------|
| 9 | mini Go | 81 | $\leq 15$ | < 0.1 ms |
| 13 | 教學棋 | 169 | $\leq 25$ | < 0.5 ms |
| 19 | 標準棋盤 | 361 | $\leq 50$ | < 1 ms |
| 25 | 大棋盤實驗 | 625 | $\leq 80$ | < 3 ms |
| $n \to \infty$ | 理論分析 | $n^2$ | $O(n^2)$ | $O(n^2 \log n)$ |

漸近上界 $O(n^2 + m \log m)$ 在 $m = O(n^2)$ 時為 $O(n^2 \log n)$（worst case），但實戰局面 $m \ll n^2$。

---

## 範例：三 region 局面之全程演算

設盤面分解為三個獨立 region：

| Region | 形狀 | 公式 | $(LS, RS, T, \Delta)$ |
|--------|------|------|----------------------|
| $R_1$ | 1×3 corridor | (c) | $(3, 1, 1, 2)$ |
| $R_2$ | 1×5 corridor | (c) | $(5, 4, 0.5, 1)$ |
| $R_3$ | simple switch $\{8 \mid -8\}$ | (b) | $(8, -8, 8, 16)$ |

### Phase 3 各 X 之結果

**X = B（按 T 排）**：
- $T_3 = 8 > T_1 = 1 > T_2 = 0.5$
- top-1 = $R_3$，top-2 = $R_3, R_1$，top-3 = $R_3, R_1, R_2$

**X = C（按 Δ 排）**：
- $\Delta_3 = 16 > \Delta_1 = 2 > \Delta_2 = 1$
- top-3 同 B（因均為 simple switch / corridor，$\Delta = 2T$）

**X = D-must（按 $V_j$ 排）**：

預處理：$\sigma = (3, 1, 2)$（按 $\Delta$ 降序），$(a_l, b_l) = (8, -8), (3, 1), (5, 4)$

- $P_a^{\text{even}}: [0, 0, 3, 3]$
- $P_b^{\text{odd}}: [0, -8, -8, -8 + 4 = -4]$
- $S_a^{\text{odd}}: [4]=0, [3]=5, [2]=5, [1]=5+8=13$
- $S_b^{\text{even}}: [4]=0, [3]=0, [2]=1, [1]=1$

計算 $V_j$：

- $j = R_3$（$p = 1$）：$V_{R_3} = 8 + 0 + 0 + S_a^{\text{odd}}[2] + S_b^{\text{even}}[2] = 8 + 5 + 1 = 14$
- $j = R_1$（$p = 2$）：$V_{R_1} = 3 + P_a^{\text{even}}[1] + P_b^{\text{odd}}[1] + S_a^{\text{odd}}[3] + S_b^{\text{even}}[3] = 3 + 0 + (-8) + 5 + 0 = 0$
- $j = R_2$（$p = 3$）：$V_{R_2} = 5 + P_a^{\text{even}}[2] + P_b^{\text{odd}}[2] + S_a^{\text{odd}}[4] + S_b^{\text{even}}[4] = 5 + 3 + (-8) + 0 + 0 = 0$

排序：$V_{R_3} = 14 > V_{R_1} = V_{R_2} = 0$.

- top-1 = $R_3$
- top-2 = $\{R_1, R_2\}$（**tied**，符合 F2 之成對 ties）

**X = D-avoid**：排序 ascending：$V_{R_2} = V_{R_1} = 0 < V_{R_3} = 14$.

**B / C / D-must / D-avoid 之比較**：

| Top-1 | B | C | D-must | D-avoid |
|-------|---|---|--------|---------|
| 結果 | $R_3$ | $R_3$ | $R_3$ | $R_2$ 或 $R_1$（tied） |

四種定義在此例中：B / C / D-must 之 top-1 一致為 $R_3$（符合 F1）；D-avoid 不同（黑該避開 $R_2/R_1$ 而下 $R_3$，因 $R_3$ 給最高得分；如果黑下 $R_1$ 或 $R_2$ 反而得分較少）。

**實戰意涵**：黑方優先下 $R_3$（CGT swing 最大），然後依次處理 $R_1, R_2$ 之小官子。具體手順見「對弈序列」（Sequence$_p$ in §5.4）.

---

## Python 參考實作（核心 Phase 3）

```python
def best_move_d_must(regions, k):
    """
    regions: list of (LS_i, RS_i, hottest_move_i)
    k: top-k 數量
    return: top-k regions with hottest moves
    """
    m = len(regions)
    # σ: 按 Δ_i 降序排列之 region 索引
    sigma = sorted(range(m), key=lambda i: -(regions[i][0] - regions[i][1]))
    a = [regions[sigma[l]][0] for l in range(m)]
    b = [regions[sigma[l]][1] for l in range(m)]

    # 4 個 prefix/suffix arrays（1-indexed, 用 [0..m+1]）
    P_a_even = [0] * (m + 2)
    P_b_odd  = [0] * (m + 2)
    for p in range(1, m + 1):
        P_a_even[p] = P_a_even[p-1] + (a[p-1] if p % 2 == 0 else 0)
        P_b_odd[p]  = P_b_odd[p-1]  + (b[p-1] if p % 2 == 1 else 0)

    S_a_odd  = [0] * (m + 2)
    S_b_even = [0] * (m + 2)
    for p in range(m, 0, -1):
        S_a_odd[p]  = S_a_odd[p+1]  + (a[p-1] if p % 2 == 1 else 0)
        S_b_even[p] = S_b_even[p+1] + (b[p-1] if p % 2 == 0 else 0)

    # 計算 V_j
    V = [0] * m
    for p in range(1, m + 1):
        j = sigma[p-1]  # 該位置對應之 original region 索引
        V[j] = a[p-1] + P_a_even[p-1] + P_b_odd[p-1] + S_a_odd[p+1] + S_b_even[p+1]

    # Top-k by V descending
    pi = sorted(range(m), key=lambda j: -V[j])
    return [(pi[i], regions[pi[i]][2]) for i in range(k)]
```

---

## 實作重點與已知限制

### 真正的瓶頸不是 Phase 3 而是 Phase 2 之分類

Phase 3 之算法清晰且 $O(m \log m)$。**Phase 2 才是工程困難點**：
- 對任意盤面，**判斷 $R_i$ 是否為 BW 標準形狀**本身需要：
  - 死活分析（distinguish 已活 vs 半活 vs 死）
  - Canonical form 計算（dominated/reversible elimination）
  - Sente sequence 之終止判定

實戰實作時，Phase 2 通常以**規則庫匹配**（ pattern matching against a catalog of common shapes）為主，配合 lightweight 死活引擎處理邊界 case。完整 BW 1994 Ch. 3-4 之 catalog 含十餘種變體。

### 不滿足 promise 時 algorithm 失效

若任一 promise 不滿足：
- **(P1) 局部不可分解**：region 互動破壞 sum 結構，stops 計算失效 → 退回一般 minimax（EXPTIME）
- **(P2) 含 ko**：博弈樹無限循環，CGT canonical form 不收斂
- **(P3) 含 non-BW 形狀**（如複雜死活、未活之大塊）：BWFormula 無法分類

實戰：先用 detector 檢查三 promise；若不滿足，給出 fallback heuristic（如 KataGo 之 policy network）+ warning。

### top-k 之 D-must ranking 之成對 ties 是「特性」而非 bug

定理 F2 顯示 $V_{\sigma(2)} = V_{\sigma(3)}, V_{\sigma(4)} = V_{\sigma(5)}, \ldots$ 為**結構性恆等**。實作時要明示給用戶「top-2 與 top-3 數學上同樣好」，避免誤導為某個 deterministic 排序。

---

## 結論

**「乾淨官子下最佳一手」之計算解法**：

1. 三階段流水線：Decompose → BWFormula → Aggregate
2. 總複雜度 $O(n^2 + m \log m)$（generic in $n$；19×19 為 special instance，並非算法之內建假設）
3. 四種「最好」定義（B / C / D-must / D-avoid）共享 building blocks，僅 Phase 3 之排序準則不同
4. 工程瓶頸在 Phase 2 之分類（需 BW shape recognition + 死活引擎輔助）
5. 算法只在三 promise 同時滿足下適用；否則退回 heuristic

對應 proof.md：本文件 Phase 1-3 = §5.4 算法 2.1/2.2/2.3，BW 公式 = §5.2.1，正確性 = §5.1 引理 H + §5.3 定理 A 之上界對偶（受限上界 = 定理 B）.
