# 乾淨官子最佳一手計算工具

從 deep-proof 研究抽出之實作工具。給定 $n \times n$ 圍棋盤面，輸出官子階段最佳一手座標。

## 安裝 / 執行

純 Python 3，無外部依賴。

```bash
python3 tool.py        # 跑內建 5 個測試
```

## 用法

```python
from tool import best_move

board = """
W W W W W . . . . . W W W W W W W .
W . . . B . . . . . W . . . . . B .
W W W W B . . . . . W W W W W W B .
. . . . . . . . . . . . . . . . . .
"""
result = best_move(board, X='C', k=1)
print(result['top_k'][0])
# {'rank': 1, 'region_id': 'R2', 'cells': [...], 'best_move': (1, 3), ...}
```

### 輸入

- `board`: 多行字串，每格 ∈ `{'B', 'W', '.'}`；空白與 `|` 會被忽略
- `X`: 排序準則
  - `'B'`: 溫度最高（CGT Hotstrat）
  - `'C'`: swing 最大（默認，最常用）
  - `'D-must'`: 黑該下哪手最有利
  - `'D-avoid'`: 黑絕不能下哪手
- `k`: 回傳前 k 名，預設 1
- `annotations`（選填）: 用戶手動標記非 corridor / 非 number 之 region

### 輸出

```python
{
    'top_k': [
        {
            'rank': 1,
            'region_id': 'R2',
            'cells': [(1, 1), (1, 2), (1, 3)],
            'best_move': (1, 3),       # 推薦的 (row, col)
            'score': 2.00,             # 排序量
            'stops': (3, 1),           # (LS, RS)
        },
        ...
    ],
    'all_regions': [...],              # debug 用
    'unknowns': [...]                  # 無法自動分類之區域
}
```

## 自動分類能力

| 形狀 | 自動偵測 | 公式 |
|------|---------|------|
| Number（單色封閉地）| ✓ | $LS = RS = $ 目數 |
| Corridor 1×ℓ（線性邊空，雙色邊界）| ✓ | $LS = \ell$, $RS = \lfloor (\ell-1)^2/4 \rfloor$ |
| Simple switch $\{a \mid b\}$ | ✗（需手動標）| $LS = a$, $RS = b$ |
| 其他（含未活、follow-up、infinitesimals）| ✗ | 不支援，列入 unknowns |

對複雜形狀，用 `annotations` 手動標：

```python
annotations = {
    (5, 5): {                          # region 內任一座標
        'shape': 'switch',
        'a': 8,                        # B 先動結局
        'b': -8,                       # W 先動結局
        'best_move': (5, 5),           # 推薦座標
    }
}
result = best_move(board, X='C', annotations=annotations)
```

## 已知限制

1. **不處理含劫盤面**：演算法假設 ko-free（per `proof.md` 定義 3）
2. **不處理 region 互動**：演算法假設 (P1) 局部可分解
3. **死活引擎缺**：未活 / 半活之大塊需手動標為 switch
4. **複雜形狀只能標 switch**：sente sequence、infinitesimals 等不支援

實戰應用：
- 適用於終局後段、各塊已穩定、純收 corridor 之局面
- 中盤含 fight 不適用
- 邊界場景請參考 `practical.md` 之「三個邊界提醒」

## 檔案結構

### 程式（兩種語言、三種型態）

```
Python：
  demo.py     # Phase 3 (排序), 純 prefix-sums 算 V_j
  tool.py     # Phase 1 (decompose) + Phase 2 (classify) + 整合

JavaScript ES Module：
  demo.mjs    # Phase 3，Node 18+ 或現代瀏覽器可 import
  tool.mjs    # Phase 1+2+3，import demo.mjs

Web App：
  index.html  # 自包含單檔（30KB），純 inline JS+CSS
              # 開檔即用，無需 server，無外部依賴
              # 含 19×19 SVG 棋盤、檔案匯入、進度條、結果視覺化
```

### 文件

```
proof.md          # 完整證明（1091 行）
math-solution.md  # 純函數合成
algorithm.md      # 含 pseudocode 之算法
practical.md      # 一頁 cheatsheet
readme.md         # 本文件
```

### 內部研究紀錄

```
attack-spec.md / formalization.md / decisions.md   # Phase 1-2 + 全程決策
exploration/    # Phase 3 多路線探索（routes-design, route-1~3, selection）
gap-attacks/    # Phase 4 間隙攻擊（001 gadget, 002 ko, 003 C≡D 拆分）
reviews/        # Phase 5 四輪審查（round-1~4 review + fixes）
```

## 三種使用方式

| 想做什麼 | 用哪個 |
|---------|--------|
| 在 terminal 跑 Python 算 best move | `python3 tool.py` |
| 在 Node 跑 JS 算 best move | `node tool.mjs` |
| 用瀏覽器互動操作（含視覺化）| 直接開 `index.html` |
| 部署成公開網頁 | 把 `index.html` 放任意靜態 host（GitHub Pages、Netlify 等）|

`demo.py` 之 4 個 `aggregate_X_*` 函數實作了 §5.4 算法 2.1/2.2/2.3 之核心；`tool.py` 補了實際盤面處理；`*.mjs` 為其 JS 1:1 port；`index.html` 為自包含 web demo。

## 對應理論文件

| 看什麼 | 看哪份 |
|--------|--------|
| 一頁 cheatsheet（最簡） | `practical.md` |
| 純數學公式（函數合成）| `math-solution.md` |
| 完整算法（含 pseudocode）| `algorithm.md` |
| 完整證明（含 PSPACE-hardness）| `proof.md` |
| 工具用法（本文）| `readme.md` |
| Python 程式碼 | `tool.py` + `demo.py` |
| JavaScript 程式碼 | `tool.mjs` + `demo.mjs` |
| Web 互動 demo | `index.html`（直接開啟）|

## 範例輸出（Test 5）

```
=== Test 5 (X=D-must): 1x3 corridor + 1x5 corridor + switch{8|-8} ===
Classified regions:
  R2   corridor(ell=3)           LS=  3 RS=  1  Δ=  2 T=1.0  (3 cells)
  R3   corridor(ell=5)           LS=  5 RS=  4  Δ=  1 T=0.5  (5 cells)
  R4   switch(8|-8)              LS=  8 RS= -8  Δ= 16 T=8.0  (1 cell)
Unknown regions (need user annotation):
  R1   117 cells starting at (0, 5): unknown shape; please annotate
Top-k:
  rank=1 region=R4 move=(6, 7)  score=14.00 stops=(8, -8)
  rank=2 region=R2 move=(1, 3)  score= 0.00 stops=(3, 1)    ← tied (F2)
  rank=3 region=R3 move=(1, 15) score= 0.00 stops=(5, 4)    ← tied (F2)
```

數值與 `algorithm.md §範例` 完全一致。`R2`/`R3` 之 V=0 tied 對應 proof.md 定理 F2 之結構性成對 ties。

---

Maintained by Light. I build and maintain websites with AI as a service: [arthurs.tw](https://arthurs.tw/?utm_source=github&utm_medium=readme&utm_campaign=oss)
