// tool.mjs — Phase 1+2+3 (port of tool.py)
//
// Exports bestMove(boardStr, options) for end-to-end best-move computation.
//
// Annotations format (Map):
//   new Map([
//     ['r,c', { shape: 'switch', a: 8, b: -8, bestMove: [r, c] }],
//   ])

import {
  aggregateXB,
  aggregateXC,
  aggregateXDMust,
  aggregateXDAvoid,
} from './demo.mjs';

const aggregators = {
  B: aggregateXB,
  C: aggregateXC,
  'D-must': aggregateXDMust,
  'D-avoid': aggregateXDAvoid,
};

// ===============================================================
// Board parsing
// ===============================================================

export function parseBoard(boardStr) {
  const rows = [];
  for (const line of boardStr.trim().split('\n')) {
    const clean = line.replace(/[\s|]/g, '').trim();
    if (clean) rows.push([...clean]);
  }
  if (rows.length > 0 && !rows.every((r) => r.length === rows[0].length)) {
    throw new Error('Board rows have inconsistent lengths');
  }
  return rows;
}

export function boardSize(board) {
  return [board.length, board[0]?.length ?? 0];
}

// ===============================================================
// Phase 1: Decomposition
// ===============================================================

export function findRegions(board) {
  const [nr, nc] = boardSize(board);
  const visited = Array.from({ length: nr }, () => new Array(nc).fill(false));
  const regions = [];

  for (let i = 0; i < nr; i++) {
    for (let j = 0; j < nc; j++) {
      if (board[i][j] === '.' && !visited[i][j]) {
        const cells = [];
        const stack = [[i, j]];
        while (stack.length > 0) {
          const [r, c] = stack.pop();
          if (
            r >= 0 &&
            r < nr &&
            c >= 0 &&
            c < nc &&
            board[r][c] === '.' &&
            !visited[r][c]
          ) {
            visited[r][c] = true;
            cells.push([r, c]);
            for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
              stack.push([r + dr, c + dc]);
            }
          }
        }
        cells.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
        regions.push(cells);
      }
    }
  }
  return regions;
}

export function boundaryColors(board, cells) {
  const [nr, nc] = boardSize(board);
  const cellSet = new Set(cells.map(([r, c]) => `${r},${c}`));
  const counts = { B: 0, W: 0, edge: 0 };
  const seen = new Set();

  for (const [r, c] of cells) {
    for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
      const nr_ = r + dr;
      const nc_ = c + dc;
      const key = `${nr_},${nc_}`;
      if (cellSet.has(key) || seen.has(key)) continue;
      seen.add(key);
      if (nr_ < 0 || nr_ >= nr || nc_ < 0 || nc_ >= nc) {
        counts.edge++;
      } else if (board[nr_][nc_] === 'B' || board[nr_][nc_] === 'W') {
        counts[board[nr_][nc_]]++;
      }
    }
  }
  return counts;
}

// ===============================================================
// Phase 2: Classification
// ===============================================================

export function classifyNumber(board, cells) {
  const bc = boundaryColors(board, cells);
  if (bc.B > 0 && bc.W === 0) {
    return { shape: 'number', value: cells.length, cells, bestMove: null };
  }
  if (bc.W > 0 && bc.B === 0) {
    return { shape: 'number', value: -cells.length, cells, bestMove: null };
  }
  if (bc.B === 0 && bc.W === 0) {
    return { shape: 'number', value: 0, cells, bestMove: null };
  }
  return null;
}

export function classifyCorridor(board, cells) {
  if (cells.length === 0) return null;
  const rows = [...new Set(cells.map(([r]) => r))].sort((a, b) => a - b);
  const cols = [...new Set(cells.map(([, c]) => c))].sort((a, b) => a - b);

  if (rows.length === 1) {
    const r = rows[0];
    const cs = cells.map(([, c]) => c).sort((a, b) => a - b);
    let consecutive = true;
    for (let i = 0; i < cs.length - 1; i++) {
      if (cs[i + 1] - cs[i] !== 1) {
        consecutive = false;
        break;
      }
    }
    if (consecutive) {
      const ordered = cs.map((c) => [r, c]);
      return checkCorridor(board, ordered, 'H');
    }
  } else if (cols.length === 1) {
    const c = cols[0];
    const rs = cells.map(([r]) => r).sort((a, b) => a - b);
    let consecutive = true;
    for (let i = 0; i < rs.length - 1; i++) {
      if (rs[i + 1] - rs[i] !== 1) {
        consecutive = false;
        break;
      }
    }
    if (consecutive) {
      const ordered = rs.map((r) => [r, c]);
      return checkCorridor(board, ordered, 'V');
    }
  }
  return null;
}

function checkCorridor(board, orderedCells, orientation) {
  const [nr, nc] = boardSize(board);
  const ell = orderedCells.length;
  const bc = boundaryColors(board, orderedCells);

  if (bc.B === 0 || bc.W === 0) return null;

  const endFirst = orderedCells[0];
  const endLast = orderedCells[orderedCells.length - 1];

  let endFirstColor;
  let endLastColor;
  if (orientation === 'H') {
    const r = endFirst[0];
    const cMin = endFirst[1];
    const cMax = endLast[1];
    endFirstColor = cMin > 0 ? board[r][cMin - 1] : 'edge';
    endLastColor = cMax < nc - 1 ? board[r][cMax + 1] : 'edge';
  } else {
    const c = endFirst[1];
    const rMin = endFirst[0];
    const rMax = endLast[0];
    endFirstColor = rMin > 0 ? board[rMin - 1][c] : 'edge';
    endLastColor = rMax < nr - 1 ? board[rMax + 1][c] : 'edge';
  }

  const longSide = { B: 0, W: 0 };
  for (const [r, c] of orderedCells) {
    const perps =
      orientation === 'H'
        ? [[r - 1, c], [r + 1, c]]
        : [[r, c - 1], [r, c + 1]];
    for (const [nr_, nc_] of perps) {
      if (nr_ >= 0 && nr_ < nr && nc_ >= 0 && nc_ < nc) {
        const cell = board[nr_][nc_];
        if (cell === 'B' || cell === 'W') longSide[cell]++;
      }
    }
  }

  if (longSide.B === 0 && longSide.W === 0) return null;
  const owner = longSide.B >= longSide.W ? 'B' : 'W';
  const invader = owner === 'B' ? 'W' : 'B';

  let bestMove;
  if (endFirstColor === invader) bestMove = endFirst;
  else if (endLastColor === invader) bestMove = endLast;
  else return null;

  return {
    shape: 'corridor',
    length: ell,
    cells: orderedCells,
    bestMove,
    orientation,
    owner,
    invader,
  };
}

export function autoClassify(board, cells) {
  let result = classifyNumber(board, cells);
  if (result) return result;
  result = classifyCorridor(board, cells);
  if (result) return result;
  return { shape: 'unknown', cells, bestMove: null };
}

// ===============================================================
// BWFormula
// ===============================================================

export function bwFormula(classification) {
  const shape = classification.shape;
  const base = {
    id: classification.id ?? 'R?',
    cells: classification.cells,
    bestMove: classification.bestMove,
  };

  if (shape === 'number') {
    const v = classification.value;
    return { ...base, shape: `number(${v})`, LS: v, RS: v, T: 0, mu: v };
  }
  if (shape === 'corridor') {
    const ell = classification.length;
    const LS = ell;
    const RS = Math.floor((ell - 1) ** 2 / 4);
    return {
      ...base,
      shape: `corridor(ell=${ell})`,
      LS,
      RS,
      T: (LS - RS) / 2,
      mu: (LS + RS) / 2,
    };
  }
  if (shape === 'switch') {
    const a = classification.a;
    const b = classification.b;
    return {
      ...base,
      shape: `switch(${a}|${b})`,
      LS: a,
      RS: b,
      T: (a - b) / 2,
      mu: (a + b) / 2,
    };
  }
  return null;
}

// ===============================================================
// Main entry: bestMove
// ===============================================================

export function bestMove(boardStr, options = {}) {
  const X = options.X ?? 'C';
  const k = options.k ?? 1;
  const annotations = options.annotations ?? new Map();
  const onProgress = options.onProgress; // optional callback for UI

  const log = (phase, msg) => {
    if (onProgress) onProgress({ phase, msg });
  };

  log(0, 'Parsing board...');
  const board = parseBoard(boardStr);
  log(0, `Board parsed: ${board.length}×${board[0]?.length || 0}`);

  log(1, 'Decomposing into regions...');
  const rawRegions = findRegions(board);
  log(1, `Found ${rawRegions.length} region(s)`);

  log(2, 'Classifying each region...');
  const classified = [];
  const unknowns = [];

  for (let idx = 0; idx < rawRegions.length; idx++) {
    const cells = rawRegions[idx];
    let ann = null;
    for (const cell of cells) {
      const key = `${cell[0]},${cell[1]}`;
      if (annotations.has(key)) {
        ann = annotations.get(key);
        break;
      }
    }

    let classification;
    if (ann) {
      classification = { ...ann, cells, id: `R${idx + 1}` };
      if (!classification.bestMove) classification.bestMove = cells[0];
    } else {
      classification = autoClassify(board, cells);
      classification.id = `R${idx + 1}`;
    }

    const result = bwFormula(classification);
    if (result) {
      classified.push(result);
      log(2, `R${idx + 1}: ${result.shape}, Δ=${result.LS - result.RS}`);
    } else {
      unknowns.push({
        id: `R${idx + 1}`,
        cells,
        reason: 'unknown shape; please annotate',
      });
      log(2, `R${idx + 1}: unknown shape (${cells.length} cells)`);
    }
  }

  log(3, `Aggregating by X=${X}...`);
  const hot = classified.filter((r) => r.LS - r.RS > 0);

  if (!(X in aggregators)) {
    throw new Error(`Unknown X: ${X}; expected one of ${Object.keys(aggregators)}`);
  }

  const topK = hot.length > 0 ? aggregators[X](hot, k) : [];
  log(3, `Returning top-${Math.min(k, topK.length)}`);

  return { topK, allRegions: classified, unknowns };
}

// ===============================================================
// Self-test
// ===============================================================

if (
  typeof process !== 'undefined' &&
  import.meta.url === `file://${process.argv[1]}`
) {
  const board5 = `
    W W W W W . . . . . W W W W W W W .
    W . . . B . . . . . W . . . . . B .
    W W W W B . . . . . W W W W W W B .
    . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . .
    . . . . . . W W W . . . . . . . . .
    . . . . . . W . W . . . . . . . . .
    . . . . . . W W W . . . . . . . . .
    . . . . . . . . . . . . . . . . . .
  `;
  const annotations = new Map([
    ['6,7', { shape: 'switch', a: 8, b: -8, bestMove: [6, 7] }],
  ]);

  for (const X of ['B', 'C', 'D-must', 'D-avoid']) {
    console.log(`\n=== Test (X=${X}) ===`);
    const result = bestMove(board5, { X, k: 3, annotations });
    console.log('Classified:');
    for (const r of result.allRegions) {
      console.log(
        `  ${r.id} ${r.shape} LS=${r.LS} RS=${r.RS} Δ=${r.LS - r.RS}`
      );
    }
    console.log('Top-k:');
    for (const e of result.topK) {
      console.log(
        `  rank=${e.rank} region=${e.regionId} move=[${e.bestMove}] ` +
          `score=${e.score.toFixed(2)}`
      );
    }
  }
}
