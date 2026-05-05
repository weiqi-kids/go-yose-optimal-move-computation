"""
Demo: Phase 3 of best-move algorithm (D-must variant).

Input contract:
    region_data: list of dicts, each containing:
        'id'         : region identifier
        'cells'      : list of (row, col) — which empty cells belong to this region
        'shape'      : BW standard shape type (one of 'number', 'switch', 'corridor', ...)
        'LS', 'RS'   : stops (computed by Phase 2's BWFormula)
        'best_move'  : (row, col) — the in-region key point recommended

Output contract:
    list of length k, each entry containing:
        'rank'         : 1, 2, 3, ...
        'region_id'    : from input
        'cells'        : from input
        'best_move'    : recommended coordinate
        'score'        : ranking value (V_j for D-must, T_i for B, etc.)
        'stops'        : (LS, RS)

Run:
    python3 demo.py
"""

from typing import List, Dict, Tuple


def aggregate_X_B(regions: List[Dict], k: int) -> List[Dict]:
    """X = B: rank by temperature T_i = (LS_i - RS_i) / 2."""
    ranked = sorted(regions, key=lambda r: -(r['LS'] - r['RS']) / 2)
    return [
        {
            'rank': i + 1,
            'region_id': r['id'],
            'cells': r['cells'],
            'best_move': r['best_move'],
            'score': (r['LS'] - r['RS']) / 2,
            'stops': (r['LS'], r['RS']),
        }
        for i, r in enumerate(ranked[:k])
    ]


def aggregate_X_C(regions: List[Dict], k: int) -> List[Dict]:
    """X = C: rank by swing Delta_i = LS_i - RS_i."""
    ranked = sorted(regions, key=lambda r: -(r['LS'] - r['RS']))
    return [
        {
            'rank': i + 1,
            'region_id': r['id'],
            'cells': r['cells'],
            'best_move': r['best_move'],
            'score': r['LS'] - r['RS'],
            'stops': (r['LS'], r['RS']),
        }
        for i, r in enumerate(ranked[:k])
    ]


def compute_V(regions: List[Dict]) -> List[Tuple[int, float]]:
    """
    Compute V_j for D-must: 'B forced to play R_j first, then optimal play'.
    Uses prefix-sums per algorithm.md §Phase 3 / proof.md §5.4.

    Returns list of (region_id, V_j).
    """
    m = len(regions)
    # sigma: indices sorted by Delta descending
    sigma = sorted(range(m), key=lambda i: -(regions[i]['LS'] - regions[i]['RS']))
    a = [regions[sigma[l]]['LS'] for l in range(m)]
    b = [regions[sigma[l]]['RS'] for l in range(m)]

    # 1-indexed prefix/suffix arrays with sentinel at 0 / m+1
    P_a_even = [0.0] * (m + 2)
    P_b_odd  = [0.0] * (m + 2)
    for p in range(1, m + 1):
        P_a_even[p] = P_a_even[p - 1] + (a[p - 1] if p % 2 == 0 else 0)
        P_b_odd[p]  = P_b_odd[p - 1]  + (b[p - 1] if p % 2 == 1 else 0)

    S_a_odd  = [0.0] * (m + 2)
    S_b_even = [0.0] * (m + 2)
    for p in range(m, 0, -1):
        S_a_odd[p]  = S_a_odd[p + 1]  + (a[p - 1] if p % 2 == 1 else 0)
        S_b_even[p] = S_b_even[p + 1] + (b[p - 1] if p % 2 == 0 else 0)

    V = [0.0] * m
    for p in range(1, m + 1):
        original_idx = sigma[p - 1]
        V[original_idx] = (
            a[p - 1]
            + P_a_even[p - 1]
            + P_b_odd[p - 1]
            + S_a_odd[p + 1]
            + S_b_even[p + 1]
        )
    return [(regions[j]['id'], V[j]) for j in range(m)]


def aggregate_X_D_must(regions: List[Dict], k: int) -> List[Dict]:
    """X = D-must: rank by V_j (B-forced-first then optimal play) descending."""
    V = compute_V(regions)
    region_by_id = {r['id']: r for r in regions}
    ranked = sorted(V, key=lambda x: -x[1])
    return [
        {
            'rank': i + 1,
            'region_id': rid,
            'cells': region_by_id[rid]['cells'],
            'best_move': region_by_id[rid]['best_move'],
            'score': v,
            'stops': (region_by_id[rid]['LS'], region_by_id[rid]['RS']),
        }
        for i, (rid, v) in enumerate(ranked[:k])
    ]


def aggregate_X_D_avoid(regions: List[Dict], k: int) -> List[Dict]:
    """X = D-avoid: rank by V_j ascending (smallest V = biggest mistake)."""
    V = compute_V(regions)
    region_by_id = {r['id']: r for r in regions}
    ranked = sorted(V, key=lambda x: x[1])
    return [
        {
            'rank': i + 1,
            'region_id': rid,
            'cells': region_by_id[rid]['cells'],
            'best_move': region_by_id[rid]['best_move'],
            'score': v,
            'stops': (region_by_id[rid]['LS'], region_by_id[rid]['RS']),
        }
        for i, (rid, v) in enumerate(ranked[:k])
    ]


def best_move(regions: List[Dict], X: str, k: int) -> List[Dict]:
    """Main entry: dispatch by X."""
    dispatch = {
        'B':       aggregate_X_B,
        'C':       aggregate_X_C,
        'D-must':  aggregate_X_D_must,
        'D-avoid': aggregate_X_D_avoid,
    }
    if X not in dispatch:
        raise ValueError(f"Unknown X: {X}")
    return dispatch[X](regions, k)


# ---------------------------------------------------------------
# Worked example: 3-region position from algorithm.md
# ---------------------------------------------------------------
example_regions = [
    {
        'id': 'R1',
        'cells': [(0, 0), (0, 1), (0, 2)],          # 1x3 corridor
        'shape': 'corridor',
        'LS': 3, 'RS': 1,                            # ell=3 → LS=3, RS=floor(4/4)=1
        'best_move': (0, 0),                         # entry point
    },
    {
        'id': 'R2',
        'cells': [(0, 5), (0, 6), (0, 7), (0, 8), (0, 9)],  # 1x5 corridor
        'shape': 'corridor',
        'LS': 5, 'RS': 4,                            # ell=5 → LS=5, RS=floor(16/4)=4
        'best_move': (0, 5),
    },
    {
        'id': 'R3',
        'cells': [(5, 5)],                           # simple switch (single key point)
        'shape': 'switch',
        'LS': 8, 'RS': -8,                           # {8 | -8}
        'best_move': (5, 5),
    },
]


if __name__ == '__main__':
    print("=" * 70)
    print("Demo: best-move algorithm (Phase 3 only; Phase 1+2 pre-computed)")
    print("=" * 70)
    print()
    print("Input regions:")
    for r in example_regions:
        delta = r['LS'] - r['RS']
        T = delta / 2
        print(f"  {r['id']}: shape={r['shape']:8s}  "
              f"LS={r['LS']:3}  RS={r['RS']:3}  "
              f"Δ={delta:3}  T={T:.1f}  best_move={r['best_move']}")

    print()
    for X in ['B', 'C', 'D-must', 'D-avoid']:
        print(f"--- X = {X}, top-3 ---")
        result = best_move(example_regions, X=X, k=3)
        for entry in result:
            print(f"  rank {entry['rank']}: "
                  f"region={entry['region_id']}  "
                  f"move={entry['best_move']}  "
                  f"score={entry['score']:.2f}  "
                  f"stops=(LS={entry['stops'][0]}, RS={entry['stops'][1]})")
        print()
