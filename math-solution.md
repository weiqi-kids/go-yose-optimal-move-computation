# 乾淨官子之最佳一手：數學解（純函數合成）

> 從 proof.md 抽出之純數學表述。本文件只給「輸入 → 輸出」之函數合成與封閉公式，不含任何算法步驟、pseudocode、複雜度討論。所有正確性陳述指向 proof.md 之對應定理。

---

## 0. 符號與輸入空間

**設**：$n \in \mathbb{N}$（$n \geq 2$），$\mathcal{S}_n := \{B, W, \emptyset\}^{n \times n}$ 為 $n \times n$ 盤面狀態空間。

**輸入**：

$$(s, X, k) \in \mathcal{S}_n \times \{B, C, D_{\text{must}}, D_{\text{avoid}}\} \times \mathbb{N}_{\geq 1}$$

**前提**（precondition），盤面 $s$ 須同時滿足：

- **(P1)** $s$ 局部可分解（formalization.md 定義 1）
- **(P2)** 每個 region 為 ko-free（定義 3）
- **(P3)** 每個 region 為 BW 標準形狀（定義 5）

記滿足 (P1)+(P2)+(P3) 之 $s$ 集合為 $\mathcal{S}_n^{\text{clean}}$。

**輸出空間**：

$$\mathcal{O}_n := \big( [n] \times [n] \big)^k$$

每個元素為 $k$ 個座標 $(r_1, c_1), \ldots, (r_k, c_k)$。

**目標**：構造函數

$$\Phi_X^{(k)} : \mathcal{S}_n^{\text{clean}} \to \mathcal{O}_n$$

使 $\Phi_X^{(k)}(s)$ 為「依 X 排序之 top-k 最佳一手座標」。

---

## 1. 函數合成

$\Phi_X^{(k)}$ 為四個子函數之合成：

$$\Phi_X^{(k)} \;=\; \pi_k \;\circ\; \rho_X \;\circ\; \mathcal{B} \;\circ\; \mathcal{D}$$

```
        s ∈ 𝒮_n^clean
        |
        | 𝓓  (decomposition)
        ↓
        {R_1, ..., R_m}
        |
        | 𝓑  (BWFormula, per-region)
        ↓
        {(LS_i, RS_i, T_i, μ_i, m*_i)}_{i=1}^m
        |
        | ρ_X  (ranking by X)
        ↓
        排序 π : [m] → [m]
        |
        | π_k  (取 top-k 之座標)
        ↓
        ((r_1, c_1), ..., (r_k, c_k)) ∈ 𝒪_n
```

下逐節定義四個子函數。

---

## 2. 分解函數 $\mathcal{D}$

**定義**：$\mathcal{D}: \mathcal{S}_n^{\text{clean}} \to \mathcal{P}([n] \times [n])^*$（盤面映至 region 序列）

$$\mathcal{D}(s) := \big( R_1, R_2, \ldots, R_m \big)$$

其中 $\{R_i\}$ 為 $s$ 之空點集合 $E(s) := \{(r, c) : s_{rc} = \emptyset\}$ 之**4-連通分塊**：

$$R_i \subseteq E(s), \quad R_i \cap R_j = \emptyset \,(i \neq j), \quad \bigcup_i R_i = E(s)$$

且每個 $R_i$ 在 $s$ 之鄰接圖中為極大連通子集（$(r, c) \sim (r', c') \iff |r - r'| + |c - c'| = 1$ 且兩者皆 $\in E(s)$）。

**Well-definedness**：由 (P1)，分解唯一存在（formalization.md 定理）。$m$ 由 $s$ 決定，$m \leq |E(s)| \leq n^2$。

---

## 3. Per-region 函數 $\mathcal{B}$（BWFormula）

**定義**：$\mathcal{B}: \mathcal{P}([n] \times [n]) \to \mathbb{Q} \times \mathbb{Q} \times \mathbb{Q}_{\geq 0} \times \mathbb{Q} \times \big([n] \times [n]\big)_{\perp}$

$$\mathcal{B}(R) := \big(LS(R), RS(R), T(R), \mu(R), m^*(R)\big)$$

由 (P3)，$R$ 之 canonical form 屬六類之一，$\mathcal{B}$ 由下列分段公式給出。

### 3.a Number

$R$ 為 number $v \in \mathbb{Q}$：

$$LS(R) = RS(R) = v, \quad T(R) = 0, \quad \mu(R) = v, \quad m^*(R) = \perp$$

### 3.b Simple switch $\{a \mid b\}$

$R$ 為 simple switch（$a, b \in \mathbb{Q}$, $a > b$）：

$$LS(R) = a, \quad RS(R) = b, \quad T(R) = \frac{a - b}{2}, \quad \mu(R) = \frac{a + b}{2}, \quad m^*(R) = \kappa(R)$$

其中 $\kappa(R)$ 為 $R$ 之 unique key point（由 (P3) 保證唯一）。

### 3.c Corridor of length $\ell$

$R$ 為標準封閉之 1×$\ell$ corridor，$\ell \in \mathbb{N}_{\geq 1}$：

$$LS(R) = \ell, \quad RS(R) = \left\lfloor \frac{(\ell - 1)^2}{4} \right\rfloor, \quad T(R) = \frac{LS(R) - RS(R)}{2}, \quad \mu(R) = \frac{LS(R) + RS(R)}{2}$$

$m^*(R) = $ corridor 之開放端進占點。

**註（公式來源）**：由 BW 1994 Ch. 3 之 dyadic recursion $RS(C_\ell) = \ell - 2 + RS(C_{\ell - 2})$ 與 $RS(C_1) = RS(C_2) = 0$ 解得（見 proof.md §5.2.1 (c)）。

### 3.d Sum / disjoint composition

$R = R^{(1)} \sqcup R^{(2)}$（disjoint union），兩子 region 各為 BW 標準形狀：

$$\mathcal{B}(R) = \mathcal{B}(R^{(1)}) \boxplus \mathcal{B}(R^{(2)})$$

其中 $\boxplus$ 為 stops 之 sum operator，由引理 H（proof.md §5.1）給出之 alternating-Δ 公式：

$$LS(R) = \mu^{(1)} + \mu^{(2)} + \frac{1}{2} \big( \Delta^{(\sigma_1)} - \Delta^{(\sigma_2)} \big)$$

其中 $\sigma$ 為 $\{1, 2\}$ 按 $\Delta$ 降序之排列，$\Delta^{(i)} = LS^{(i)} - RS^{(i)}$。對 $m \geq 3$ 之 sum，遞迴展開（per 引理 H (c)）。

### 3.e Dyadic infinitesimal

$R$ 為 infinitesimal $\in \{0, *, \uparrow, \downarrow, \uparrow*, n \cdot \uparrow, \ldots\}$:

$$LS(R) = RS(R) = 0, \quad T(R) = 0, \quad \mu(R) = 0, \quad m^*(R) = \perp$$

（infinitesimals 對 hot game sum 之 stops 為 perturbative 0；不影響 hot ranking。）

### 3.f Finite sente sequence

$R$ 為強制對弈序列，終於形態 $R_{\text{end}} \in$ {(a), (b)}，序列中累計分數 $S_B$（B 得）、$S_W$（W 得）：

$$LS(R) = LS(R_{\text{end}}) + S_B, \quad RS(R) = RS(R_{\text{end}}) + S_W$$

$T(R), \mu(R)$ 由 $LS, RS$ 推得；$m^*(R) = $ sente 之第一手座標。

---

## 4. Ranking 函數 $\rho_X$

設 $\mathcal{B}(\mathcal{D}(s)) = \big( (LS_i, RS_i, T_i, \mu_i, m^*_i) \big)_{i=1}^m$，記 $\Delta_i := LS_i - RS_i$。

$\rho_X$ 之輸出為 $[m] \to [m]$ 之 ranking permutation $\pi$，使 $\pi(1) = $ top-1 之 region 索引，依此類推。

### 4.B  X = B（溫度最優）

$$\pi_B := \arg\text{sort}_{i \in [m]} \big(- T_i\big)$$

### 4.C  X = C（swing 最優）

$$\pi_C := \arg\text{sort}_{i \in [m]} \big(- \Delta_i\big)$$

**性質**（proof.md §5.4 註）：對 simple switches，$\Delta_i = 2 T_i$，故 $\pi_B = \pi_C$；對 BW 標準形狀整體（含 corridor、sente sequence 等），二者排序仍一致（因 corridor 之 $T = \Delta / 2$）。

### 4.D-must  X = $D_{\text{must}}$（黑強制先動 region 之 V 排序）

設 $\sigma := \arg\text{sort}_{i \in [m]} \big(- \Delta_i\big)$（descending Δ），記 $a_l := LS_{\sigma(l)}, b_l := RS_{\sigma(l)}$。

對 $j \in [m]$，$p := \sigma^{-1}(j)$，定義：

$$\boxed{\;V_j \;:=\; a_p \;+\; \sum_{\substack{l = 1 \\ l \text{ even}}}^{p-1} a_{\sigma(l)} \;+\; \sum_{\substack{l = 1 \\ l \text{ odd}}}^{p-1} b_{\sigma(l)} \;+\; \sum_{\substack{l = p+1 \\ l \text{ odd}}}^{m} a_{\sigma(l)} \;+\; \sum_{\substack{l = p+1 \\ l \text{ even}}}^{m} b_{\sigma(l)}\;}$$

則：

$$\pi_{D_{\text{must}}} := \arg\text{sort}_{j \in [m]} \big(- V_j\big)$$

**封閉公式來源**：proof.md §5.4 之 prefix-sums 推導，正確性由引理 H (b) 之 saddle-point 對弈序列保證。

**性質**（proof.md §5.8 定理 F2）：對所有 $k \geq 1$ with $2k + 1 \leq m$，

$$V_{\sigma(2k)} = V_{\sigma(2k+1)}$$

即 D-must 之 ranking 在第 2 位起出現結構性成對 ties。

### 4.D-avoid  X = $D_{\text{avoid}}$

$$\pi_{D_{\text{avoid}}} := \arg\text{sort}_{j \in [m]} \big(+ V_j\big)$$

（同 $V_j$ 公式，但 ascending 排序）

---

## 5. Top-k 提取函數 $\pi_k$

設 $\rho_X$ 輸出 ranking $\pi$，per-region BWFormula 已給出 $\{m^*_i\}_{i \in [m]}$。

$$\boxed{\; \pi_k\big(\pi, \{m^*_i\}\big) \;:=\; \big( m^*_{\pi(1)}, \, m^*_{\pi(2)}, \, \ldots, \, m^*_{\pi(k)} \big) \;\in\; \mathcal{O}_n \;}$$

**Tie-breaking**：若 $\pi$ 含 ties（如 $D_{\text{must}}$ 之 F2 成對 ties），$\pi$ 為等價類之代表元；輸出之 top-k 在 ties 之內可任選 deterministic 排序（如按 region id 字典序）。

---

## 6. 主定理（數學解之正確性）

$$\boxed{\; \Phi_X^{(k)}(s) \;:=\; \pi_k\big(\rho_X(\mathcal{B}(\mathcal{D}(s))), \mathcal{B}(\mathcal{D}(s))\big) \;}$$

**定理（proof.md §5.4 之 Theorem B）**：對 $s \in \mathcal{S}_n^{\text{clean}}$ 與 $X \in \{B, C, D_{\text{must}}, D_{\text{avoid}}\}$，$\Phi_X^{(k)}(s)$ 為 BEST-MOVE-X 問題之解（依定義 4 與 §2.4 之問題陳述）。

**證明依存**：
- $\mathcal{D}$ well-defined：由 (P1)
- $\mathcal{B}$ well-defined：由 (P3) 與 §5.2.1 BW catalog
- $\rho_X$ well-defined：對 X = B / C 為純排序；對 X = D-must / D-avoid 由 $V_j$ 之 closed-form 給出，後者正確性由引理 H（§5.1, §5.1.1）保證
- $\pi_k$ well-defined：純投影

四子函數皆為 mathematical 良定，故 $\Phi_X^{(k)}$ 為良定函數。$\square$

---

## 7. 數學解之 explicit form（完整展開）

把所有合成展開，$\Phi_X^{(k)}(s)$ 之顯式公式為：

**對 X = B**：

$$\Phi_B^{(k)}(s) = \big( m^*_{\sigma_T(1)}, \ldots, m^*_{\sigma_T(k)} \big), \quad \text{其中 } \sigma_T = \arg\text{sort}_i \big(- T(R_i)\big)$$

**對 X = C**：

$$\Phi_C^{(k)}(s) = \big( m^*_{\sigma_\Delta(1)}, \ldots, m^*_{\sigma_\Delta(k)} \big), \quad \text{其中 } \sigma_\Delta = \arg\text{sort}_i \big(- (LS_i - RS_i)\big)$$

**對 X = $D_{\text{must}}$**：

$$\Phi_{D_{\text{must}}}^{(k)}(s) = \big( m^*_{\sigma_V(1)}, \ldots, m^*_{\sigma_V(k)} \big), \quad \sigma_V = \arg\text{sort}_j \big(- V_j\big)$$

其中 $V_j$ 由 §4.D-must 之 boxed 公式給出，$LS_i, RS_i$ 由 §3 之 BWFormula 給出，$\{R_i\}$ 由 §2 之 $\mathcal{D}(s)$ 給出，$m^*_i$ 由 §3 給出。

**對 X = $D_{\text{avoid}}$**：

$$\Phi_{D_{\text{avoid}}}^{(k)}(s) = \big( m^*_{\sigma_V^-(1)}, \ldots, m^*_{\sigma_V^-(k)} \big), \quad \sigma_V^- = \arg\text{sort}_j \big(+ V_j\big)$$

---

## 8. 數值代入範例

設 $\mathcal{D}(s) = (R_1, R_2, R_3)$，依 §3 算得：

| $i$ | shape | $LS_i$ | $RS_i$ | $T_i$ | $\Delta_i$ | $m^*_i$ |
|-----|-------|--------|--------|-------|------------|---------|
| 1 | corridor $\ell = 3$ | 3 | 1 | 1 | 2 | $(0, 0)$ |
| 2 | corridor $\ell = 5$ | 5 | 4 | 0.5 | 1 | $(0, 5)$ |
| 3 | switch $\{8, -8\}$ | 8 | -8 | 8 | 16 | $(5, 5)$ |

**X = B** 套 §4.B：$\sigma_T = (3, 1, 2)$ → $\Phi_B^{(3)}(s) = ((5,5), (0,0), (0,5))$

**X = C** 套 §4.C：$\sigma_\Delta = (3, 1, 2)$ → $\Phi_C^{(3)}(s) = ((5,5), (0,0), (0,5))$

**X = $D_{\text{must}}$** 套 §4.D-must：

$\sigma = (3, 1, 2)$，$(a, b) = ((8, -8), (3, 1), (5, 4))$

| $j$ | $p$ | $V_j$ 公式展開 | 值 |
|-----|-----|----------------|----|
| 3 | 1 | $a_1 + 0 + 0 + (a_3) + (b_2)$ = $8 + 0 + 0 + 5 + 1$ | 14 |
| 1 | 2 | $a_2 + 0 + b_1 + (a_3) + 0$ = $3 + 0 + (-8) + 5 + 0$ | 0 |
| 2 | 3 | $a_3 + a_2 + b_1 + 0 + 0$ = $5 + 3 + (-8) + 0 + 0$ | 0 |

$\sigma_V = (3, \{1, 2\}_{\text{tied}})$

$\Phi_{D_{\text{must}}}^{(3)}(s) = ((5,5), (0,0), (0,5))$（top-2/3 在 ties 內按 region id 排）

**X = $D_{\text{avoid}}$** 套 §4.D-avoid：

$\sigma_V^- = (\{1, 2\}_{\text{tied}}, 3)$

$\Phi_{D_{\text{avoid}}}^{(3)}(s) = ((0,0), (0,5), (5,5))$

**驗證點**（與 proof.md §5.7-5.9 之數學定理對齊）：
- $\Phi_B^{(1)} = \Phi_C^{(1)} = \Phi_{D_{\text{must}}}^{(1)} = (5, 5) = m^*_3$（**F1 之具體實例**：top-1 重合）
- $V_{\sigma(2)} = V_{\sigma(3)} = 0$（**F2 之具體實例**：成對 ties）
- $\Phi_C^{(1)} = (5, 5) \neq \Phi_{D_{\text{avoid}}}^{(1)} = (0, 0)$（**F3 之具體實例**：substantive 分歧）

---

## 9. 摘要：數學解之三句話

1. **輸入**：$(s, X, k) \in \mathcal{S}_n^{\text{clean}} \times \{B, C, D_{\text{must}}, D_{\text{avoid}}\} \times \mathbb{N}$
2. **輸出**：$\Phi_X^{(k)}(s) = (\pi_k \circ \rho_X \circ \mathcal{B} \circ \mathcal{D})(s) \in ([n] \times [n])^k$
3. **公式**：四個子函數 $\mathcal{D}, \mathcal{B}, \rho_X, \pi_k$ 各為 §2-§5 之顯式定義；正確性由 proof.md §5.4 之 Theorem B 保證。

**關鍵 closed-form**：

- $LS, RS$ 由 §3 之 BWFormula 分段公式（依 BW 形狀 (a)-(f)）給出
- $V_j$ 由 §4.D-must 之 alternating-sum 公式給出（為本研究之主要新公式，per 引理 H + 對弈序列展開）
- 排序 $\sigma$ 為 standard `argsort`（descending / ascending）
- $\pi_k$ 為投影（取前 $k$ 名之 $m^*_i$）
