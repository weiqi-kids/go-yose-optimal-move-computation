// demo.mjs — Phase 3 aggregators (port of demo.py)
//
// Exports four aggregateXX functions for X ∈ {B, C, D-must, D-avoid}
// + helper computeV for D-must / D-avoid.
//
// Region input shape:
//   { id: string, cells: [[r,c],...], LS: number, RS: number, bestMove: [r,c] }
//
// Output shape: array of {rank, regionId, cells, bestMove, score, stops:[LS,RS]}

function entry(rank, region, score) {
  return {
    rank,
    regionId: region.id,
    cells: region.cells,
    bestMove: region.bestMove,
    score,
    stops: [region.LS, region.RS],
  };
}

// X = B: rank by temperature T = (LS - RS) / 2 descending.
export function aggregateXB(regions, k) {
  const ranked = [...regions].sort(
    (a, b) => (b.LS - b.RS) / 2 - (a.LS - a.RS) / 2
  );
  return ranked.slice(0, k).map((r, i) => entry(i + 1, r, (r.LS - r.RS) / 2));
}

// X = C: rank by swing Δ = LS - RS descending.
export function aggregateXC(regions, k) {
  const ranked = [...regions].sort((a, b) => b.LS - b.RS - (a.LS - a.RS));
  return ranked.slice(0, k).map((r, i) => entry(i + 1, r, r.LS - r.RS));
}

// Compute V_j for each region using prefix-sums (per algorithm.md / proof.md §5.4).
export function computeV(regions) {
  const m = regions.length;
  // sigma: indices sorted by Δ descending
  const sigma = [...Array(m).keys()].sort(
    (i, j) => regions[j].LS - regions[j].RS - (regions[i].LS - regions[i].RS)
  );
  const a = sigma.map((idx) => regions[idx].LS);
  const b = sigma.map((idx) => regions[idx].RS);

  // 1-indexed prefix/suffix arrays with sentinels at 0 / m+1
  const PaEven = new Array(m + 2).fill(0);
  const PbOdd = new Array(m + 2).fill(0);
  for (let p = 1; p <= m; p++) {
    PaEven[p] = PaEven[p - 1] + (p % 2 === 0 ? a[p - 1] : 0);
    PbOdd[p] = PbOdd[p - 1] + (p % 2 === 1 ? b[p - 1] : 0);
  }

  const SaOdd = new Array(m + 2).fill(0);
  const SbEven = new Array(m + 2).fill(0);
  for (let p = m; p >= 1; p--) {
    SaOdd[p] = SaOdd[p + 1] + (p % 2 === 1 ? a[p - 1] : 0);
    SbEven[p] = SbEven[p + 1] + (p % 2 === 0 ? b[p - 1] : 0);
  }

  const V = new Array(m).fill(0);
  for (let p = 1; p <= m; p++) {
    const j = sigma[p - 1];
    V[j] =
      a[p - 1] +
      PaEven[p - 1] +
      PbOdd[p - 1] +
      SaOdd[p + 1] +
      SbEven[p + 1];
  }
  return regions.map((r, j) => ({ id: r.id, V: V[j] }));
}

// X = D-must: rank by V_j descending.
export function aggregateXDMust(regions, k) {
  const V = computeV(regions);
  const byId = new Map(regions.map((r) => [r.id, r]));
  const ranked = [...V].sort((x, y) => y.V - x.V);
  return ranked.slice(0, k).map((x, i) => entry(i + 1, byId.get(x.id), x.V));
}

// X = D-avoid: rank by V_j ascending.
export function aggregateXDAvoid(regions, k) {
  const V = computeV(regions);
  const byId = new Map(regions.map((r) => [r.id, r]));
  const ranked = [...V].sort((x, y) => x.V - y.V);
  return ranked.slice(0, k).map((x, i) => entry(i + 1, byId.get(x.id), x.V));
}

export const aggregators = {
  B: aggregateXB,
  C: aggregateXC,
  'D-must': aggregateXDMust,
  'D-avoid': aggregateXDAvoid,
};

// Self-test if executed directly via Node
if (
  typeof process !== 'undefined' &&
  import.meta.url === `file://${process.argv[1]}`
) {
  const example = [
    { id: 'R1', cells: [[0, 0], [0, 1], [0, 2]], LS: 3, RS: 1, bestMove: [0, 2] },
    {
      id: 'R2',
      cells: [[0, 5], [0, 6], [0, 7], [0, 8], [0, 9]],
      LS: 5,
      RS: 4,
      bestMove: [0, 9],
    },
    { id: 'R3', cells: [[5, 5]], LS: 8, RS: -8, bestMove: [5, 5] },
  ];

  console.log('=== demo.mjs self-test (matches algorithm.md §範例) ===\n');
  for (const X of ['B', 'C', 'D-must', 'D-avoid']) {
    console.log(`X=${X}, top-3:`);
    const out = aggregators[X](example, 3);
    for (const r of out) {
      console.log(
        `  rank=${r.rank} region=${r.regionId} ` +
          `move=[${r.bestMove}] score=${r.score.toFixed(2)} ` +
          `stops=[${r.stops}]`
      );
    }
    console.log();
  }
}
