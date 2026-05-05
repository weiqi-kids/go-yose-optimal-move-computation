"""
tool.py: 乾淨官子最佳一手計算工具

完整實作 Phase 1 (decompose) + Phase 2 (classify + BWFormula) + Phase 3 (aggregate).

Phase 2 的自動分類目前支援：
    - Number: 完全被單色邊界封閉的空地
    - Corridor 1×ℓ: 線性連通的空點，兩端被對方活子封閉
    - Switch: 需用戶手動標記（passing in `annotations`）
其他形狀（含未活、follow-up、infinitesimals）不支援，會標為 'unknown'。

Usage:
    from tool import best_move

    board = '''
    . . . . . W . W
    B B B B B W . W
    B . . . B W W W
    B B B B B . . .
    '''
    result = best_move(board, X='C', k=2)
    for r in result:
        print(r)

    # 用戶手動標 switch:
    annotations = {
        (5, 5): {'shape': 'switch', 'a': 8, 'b': -8, 'best_move': (5, 5)}
    }
    result = best_move(board, X='D-must', k=3, annotations=annotations)
"""

from typing import List, Dict, Tuple, Optional, Any
from demo import (
    aggregate_X_B,
    aggregate_X_C,
    aggregate_X_D_must,
    aggregate_X_D_avoid,
)


# ===============================================================
# Board parsing
# ===============================================================

def parse_board(board_str: str) -> List[List[str]]:
    """Parse multi-line string. Each cell ∈ {'B', 'W', '.'}.

    Whitespace and pipe '|' are stripped. Blank lines ignored.
    """
    rows = []
    for line in board_str.strip().split('\n'):
        clean = line.replace(' ', '').replace('|', '').strip()
        if clean:
            rows.append(list(clean))
    # Sanity: all rows same length
    if rows and not all(len(r) == len(rows[0]) for r in rows):
        raise ValueError("Board rows have inconsistent lengths")
    return rows


def board_size(board: List[List[str]]) -> Tuple[int, int]:
    return (len(board), len(board[0]) if board else 0)


# ===============================================================
# Phase 1: Decomposition
# ===============================================================

def find_regions(board: List[List[str]]) -> List[List[Tuple[int, int]]]:
    """4-connected components of empty cells."""
    nr, nc = board_size(board)
    visited = [[False] * nc for _ in range(nr)]
    regions = []
    for i in range(nr):
        for j in range(nc):
            if board[i][j] == '.' and not visited[i][j]:
                cells = []
                stack = [(i, j)]
                while stack:
                    r, c = stack.pop()
                    if (0 <= r < nr and 0 <= c < nc
                            and board[r][c] == '.' and not visited[r][c]):
                        visited[r][c] = True
                        cells.append((r, c))
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            stack.append((r + dr, c + dc))
                regions.append(sorted(cells))
    return regions


def boundary_colors(board: List[List[str]],
                    cells: List[Tuple[int, int]]) -> Dict[str, int]:
    """Count boundary cells by color."""
    nr, nc = board_size(board)
    cell_set = set(cells)
    counts = {'B': 0, 'W': 0, 'edge': 0}
    seen = set()
    for r, c in cells:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr_, nc_ = r + dr, c + dc
            if (nr_, nc_) in cell_set:
                continue
            if (nr_, nc_) in seen:
                continue
            seen.add((nr_, nc_))
            if not (0 <= nr_ < nr and 0 <= nc_ < nc):
                counts['edge'] += 1
            elif board[nr_][nc_] in ('B', 'W'):
                counts[board[nr_][nc_]] += 1
    return counts


# ===============================================================
# Phase 2: Classification (auto)
# ===============================================================

def classify_number(board, cells) -> Optional[Dict]:
    """If region surrounded by single color (with optional edges), it's a number."""
    bc = boundary_colors(board, cells)
    if bc['B'] > 0 and bc['W'] == 0:
        # Black's territory
        return {'shape': 'number', 'value': len(cells), 'cells': cells, 'best_move': None}
    if bc['W'] > 0 and bc['B'] == 0:
        # White's territory (negative for Black)
        return {'shape': 'number', 'value': -len(cells), 'cells': cells, 'best_move': None}
    if bc['B'] == 0 and bc['W'] == 0:
        # Only edges (open sea, dame)
        return {'shape': 'number', 'value': 0, 'cells': cells, 'best_move': None}
    return None  # Mixed boundary, not a number


def classify_corridor(board, cells) -> Optional[Dict]:
    """If region is a 1×ℓ strip with proper closure, it's a corridor."""
    if len(cells) == 0:
        return None
    rows = sorted(set(r for r, c in cells))
    cols = sorted(set(c for r, c in cells))

    if len(rows) == 1:
        # Horizontal strip
        r = rows[0]
        cs = sorted(c for _, c in cells)
        if all(cs[i+1] - cs[i] == 1 for i in range(len(cs) - 1)):
            return _check_corridor(board, [(r, c) for c in cs], orientation='H')
    elif len(cols) == 1:
        # Vertical strip
        c = cols[0]
        rs = sorted(r for r, _ in cells)
        if all(rs[i+1] - rs[i] == 1 for i in range(len(rs) - 1)):
            return _check_corridor(board, [(r, c) for r in rs], orientation='V')
    return None


def _check_corridor(board, ordered_cells, orientation) -> Optional[Dict]:
    """Verify the strip is a contested corridor and identify owner/invader/key-point.

    Standard contested corridor:
        - 1×ℓ strip of empty cells
        - Long sides (perpendicular to strip) are mostly one color = OWNER
        - At least one end has stones of the OPPOSITE color = INVADER
        - Key point = empty cell adjacent to invader's stones (entry for push)
    """
    nr, nc = board_size(board)
    ell = len(ordered_cells)
    bc = boundary_colors(board, ordered_cells)

    if bc['B'] == 0 or bc['W'] == 0:
        return None  # Not contested

    # Identify end neighbors (in strip's direction)
    end_first, end_last = ordered_cells[0], ordered_cells[-1]
    if orientation == 'H':
        r = end_first[0]
        c_min, c_max = end_first[1], end_last[1]
        end_first_color = board[r][c_min - 1] if c_min > 0 else 'edge'
        end_last_color = board[r][c_max + 1] if c_max < nc - 1 else 'edge'
    else:
        c = end_first[1]
        r_min, r_max = end_first[0], end_last[0]
        end_first_color = board[r_min - 1][c] if r_min > 0 else 'edge'
        end_last_color = board[r_max + 1][c] if r_max < nr - 1 else 'edge'

    # Long-side boundary colors (perpendicular to strip)
    long_side = {'B': 0, 'W': 0}
    for r, c in ordered_cells:
        if orientation == 'H':
            neighbors_perp = [(r - 1, c), (r + 1, c)]
        else:
            neighbors_perp = [(r, c - 1), (r, c + 1)]
        for nr_, nc_ in neighbors_perp:
            if 0 <= nr_ < nr and 0 <= nc_ < nc and board[nr_][nc_] in ('B', 'W'):
                long_side[board[nr_][nc_]] += 1

    if long_side['B'] == 0 and long_side['W'] == 0:
        return None  # No long-side closure
    owner = 'B' if long_side['B'] >= long_side['W'] else 'W'
    invader = 'W' if owner == 'B' else 'B'

    # Key point = the end whose neighbor is the invader's color
    if end_first_color == invader:
        best_move = end_first
    elif end_last_color == invader:
        best_move = end_last
    else:
        # No invader at either end (e.g., both ends are owner or edge)
        # Strip is fully sealed — should be a number, not corridor
        return None

    return {
        'shape': 'corridor',
        'length': ell,
        'cells': ordered_cells,
        'best_move': best_move,
        'orientation': orientation,
        'owner': owner,
        'invader': invader,
    }


def auto_classify(board, cells) -> Dict:
    """Try number, then corridor; fall back to 'unknown'."""
    result = classify_number(board, cells)
    if result:
        return result
    result = classify_corridor(board, cells)
    if result:
        return result
    return {'shape': 'unknown', 'cells': cells, 'best_move': None}


# ===============================================================
# BWFormula
# ===============================================================

def bw_formula(classification: Dict) -> Optional[Dict]:
    """Apply BWFormula. Returns standardized region dict or None for 'unknown'."""
    shape = classification['shape']
    base = {
        'id': classification.get('id', 'R?'),
        'cells': classification['cells'],
        'best_move': classification.get('best_move'),
    }

    if shape == 'number':
        v = classification['value']
        return {**base, 'shape': f'number({v})', 'LS': v, 'RS': v,
                'T': 0, 'mu': v}

    if shape == 'corridor':
        ell = classification['length']
        LS = ell
        RS = ((ell - 1) ** 2) // 4
        return {**base, 'shape': f'corridor(ell={ell})', 'LS': LS, 'RS': RS,
                'T': (LS - RS) / 2, 'mu': (LS + RS) / 2}

    if shape == 'switch':
        a = classification['a']
        b = classification['b']
        return {**base, 'shape': f'switch({a}|{b})', 'LS': a, 'RS': b,
                'T': (a - b) / 2, 'mu': (a + b) / 2}

    return None  # 'unknown' or unsupported


# ===============================================================
# Main entry: best_move
# ===============================================================

def best_move(
    board_str: str,
    X: str = 'C',
    k: int = 1,
    annotations: Optional[Dict[Tuple[int, int], Dict]] = None,
) -> Dict[str, Any]:
    """
    Find top-k best moves on a clean endgame board.

    Args:
        board_str: Multi-line string ('B' / 'W' / '.').
        X: Criterion ∈ {'B', 'C', 'D-must', 'D-avoid'}.
        k: How many top moves to return.
        annotations: Optional dict mapping a cell coord to {
            'shape': 'switch',
            'a': value if Black plays first,
            'b': value if White plays first,
            'best_move': (r, c) — defaults to the annotation key
        }

    Returns:
        {
            'top_k': list of top-k recommendations,
            'all_regions': debug info (all classified regions),
            'unknowns': regions that couldn't be classified
        }
    """
    board = parse_board(board_str)
    raw_regions = find_regions(board)
    annotations = annotations or {}

    classified = []
    unknowns = []

    for idx, cells in enumerate(raw_regions):
        # Check if user annotated any cell in this region
        ann = None
        for cell in cells:
            if cell in annotations:
                ann = annotations[cell]
                break

        if ann:
            classification = {**ann, 'cells': cells, 'id': f'R{idx+1}'}
            if 'best_move' not in classification:
                classification['best_move'] = cells[0]
        else:
            classification = auto_classify(board, cells)
            classification['id'] = f'R{idx+1}'

        result = bw_formula(classification)
        if result:
            classified.append(result)
        else:
            unknowns.append({'id': f'R{idx+1}', 'cells': cells,
                             'reason': 'unknown shape; please annotate'})

    # Filter out cold (Δ = 0) regions
    hot = [r for r in classified if (r['LS'] - r['RS']) > 0]

    # Phase 3
    dispatch = {
        'B': aggregate_X_B,
        'C': aggregate_X_C,
        'D-must': aggregate_X_D_must,
        'D-avoid': aggregate_X_D_avoid,
    }
    if X not in dispatch:
        raise ValueError(f"Unknown X: {X}; expected {list(dispatch.keys())}")

    top_k = dispatch[X](hot, k) if hot else []

    return {
        'top_k': top_k,
        'all_regions': classified,
        'unknowns': unknowns,
    }


# ===============================================================
# Tests
# ===============================================================

def _print_result(name, result):
    print(f"=== {name} ===")
    print(f"Classified regions:")
    for r in result['all_regions']:
        cells_repr = (f"{len(r['cells'])} cells starting at "
                      f"{r['cells'][0]}")
        print(f"  {r['id']:4s} {r['shape']:25s} "
              f"LS={r['LS']:3} RS={r['RS']:3}  "
              f"Δ={r['LS']-r['RS']:3} T={r['T']:.1f}  "
              f"({cells_repr})")
    if result['unknowns']:
        print(f"Unknown regions (need user annotation):")
        for u in result['unknowns']:
            print(f"  {u['id']:4s} {len(u['cells'])} cells starting at "
                  f"{u['cells'][0]}: {u['reason']}")
    print(f"Top-k:")
    if not result['top_k']:
        print(f"  (no hot moves; all classified regions are cold)")
    for entry in result['top_k']:
        print(f"  rank={entry['rank']} region={entry['region_id']} "
              f"move={entry['best_move']} score={entry['score']:.2f} "
              f"stops={entry['stops']}")
    print()


if __name__ == '__main__':
    # Test 1: Single corridor of length 3
    board1 = """
    B B B B B
    B . . . B
    B B B B B
    """
    result = best_move(board1, X='C', k=1)
    _print_result("Test 1: Single 1x3 region (Black's territory, 3 points)", result)
    # Expect: classified as number(+3), Δ=0, no hot moves

    # Test 2: One corridor (mixed boundary)
    board2 = """
    W W W W W W
    W . . . . B
    W W W W W B
    B B B B B B
    """
    result = best_move(board2, X='C', k=1)
    _print_result("Test 2: 1x4 corridor (W boundary 3 sides + B at one end)", result)
    # Expect: classified as corridor(ell=4), LS=4, RS=2, Δ=2

    # Test 3: Two corridors (different lengths)
    board3 = """
    W W W W W W . . . . . . W W W W W W
    W . . . . B . . . . . . W . . . . B
    W W W W W B . . . . . . W W W W W B
    B B B B B B . . . . . . B B B B B B
    """
    result = best_move(board3, X='C', k=2)
    _print_result("Test 3: Two corridors (1x4 and 1x4) — should tie", result)

    # Test 4: With manual switch annotation
    board4 = """
    . . . . . . . . .
    . W W W W W . . .
    . W . . . B . . .
    . W W W W B . . .
    . . . . . B . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    """
    annotations = {
        (2, 2): {  # The contested point in the middle
            'shape': 'switch',
            'a': 8,
            'b': -8,
            'best_move': (2, 2),
        }
    }
    result = best_move(board4, X='C', k=3, annotations=annotations)
    _print_result("Test 4: Manual switch (a=8, b=-8) at (2,2)", result)

    # Test 5: 3-region board matching algorithm.md example (1x3 + 1x5 + manual switch)
    # Layout: top-left = 1x3 corridor (W territory, B invades from right)
    #         top-right = 1x5 corridor (W territory, B invades from right)
    #         middle = manual switch (annotation)
    board5 = """
    W W W W W . . . . . W W W W W W W .
    W . . . B . . . . . W . . . . . B .
    W W W W B . . . . . W W W W W W B .
    . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . .
    . . . . . . W W W . . . . . . . . .
    . . . . . . W . W . . . . . . . . .
    . . . . . . W W W . . . . . . . . .
    . . . . . . . . . . . . . . . . . .
    """
    annotations5 = {
        (6, 7): {  # The switch's contested point
            'shape': 'switch',
            'a': 8,
            'b': -8,
            'best_move': (6, 7),
        }
    }

    for X in ['B', 'C', 'D-must', 'D-avoid']:
        result = best_move(board5, X=X, k=3, annotations=annotations5)
        _print_result(f"Test 5 (X={X}): 1x3 corridor + 1x5 corridor + switch{{8|-8}}", result)

    print("All tests done.")
