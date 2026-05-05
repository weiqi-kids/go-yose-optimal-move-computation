# Paper A — On the Computational Complexity of the Optimal Yose Move in Go via Combinatorial Game Theory

## Summary

Establishes a tight complexity dichotomy for the problem of computing the
optimal endgame move in Go under four standard CGT-based definitions of
"optimal" (temperature, swing, must-play, avoid-play). Lower bound: the
problem is PSPACE-hard for all four definitions, via a polynomial-gap
reduction from the Cr\^{a}\c{s}maru--Tromp Generalized Ladder Game with an
explicit swing-control booster gadget. Upper bound: under the standard
Berlekamp--Wolfe shape promise plus ko-freeness, the problem admits an
$O(n^2 + m \log m)$ algorithm via closed-form region values and an $O(m)$
prefix-sum evaluation of optimal-sequel scores.

## Key Result

**Main Theorem (Theorem 3.1):** For every
$X \in \{B, C, D\text{-must}, D\text{-avoid}\}$, BEST-MOVE-X is
PSPACE-hard under the local-decomposition promise. Conversely
(Theorem 4.4), under the Berlekamp--Wolfe standard-shape and ko-free
promises, BEST-MOVE-X is solvable in $O(n^2 + m \log m)$.

The technical heart is the swing-control lemma (Lemma 3.2): a
polynomial-time gadget construction that maps every GLG instance
$(B, s_0)$ to a Go region $R_\Phi$ with $\Delta(R_\Phi) = 6k$ on yes-instances
and $\Delta(R_\Phi) \leq 4$ on no-instances, where $k = \mathrm{poly}(|B|)$.

## Target Journals (ranked)

1. **Theoretical Computer Science** — best fit for combined complexity
   lower-bound + matched algorithmic upper-bound result with a clean
   game-theoretic story. Estimated acceptance after revision: 35--45%.
2. **Algorithmica** — good fit for the matched upper-bound algorithm and
   prefix-sum technique; may want a stronger algorithmic emphasis.
   Estimated: 30--40%.
3. **INTEGERS** (Combinatorial Game Theory) — natural specialty venue;
   may prefer expanded examples on the BW catalogue. Estimated: 50--60%.
4. **arXiv preprint (cs.CC + cs.GT)** — first-stop deposit for community
   feedback before formal submission.

## MSC 2020 Classification

- **91A46** (Combinatorial games) — primary
- **68Q17** (Computational difficulty of problems) — secondary
- **91A05** (2-person games) — secondary

## Submission Strategy

1. Post to **arXiv** (cs.CC + cs.GT + math.CO) for community feedback.
2. Solicit a sanity-check reading from the CGT community (Berlekamp's
   academic network, Tromp on the GLG details).
3. After 2--4 weeks of arXiv exposure, submit to TCS or Algorithmica.

## Must-Cite Related Work

- Cr\^{a}\c{s}maru & Tromp 2000 (PSPACE-completeness of Go ladders) — the
  building block for our lower bound.
- Robson 1983 (n×n Go is EXPTIME-complete) — the global counterpart to our
  yose-restricted bound.
- Berlekamp & Wolfe 1994 (Mathematical Go: chilling gets the last point) —
  the source of the standard-shape catalogue used in the upper bound.
- Berlekamp, Conway & Guy 1982 (Winning Ways) — canonical-form algorithm
  used in Lemma 3.3 (canonical form of $R_\Phi$).
- Conway 1976 (On Numbers and Games) — foundational CGT framework.

## Known Limitations (address before submission)

1. **Sign-flipping reading $D$-sign is excluded.** The reduction template
   does not directly extend to the $|V_j - V_0|$ ordering because the
   baseline $V_0$ is itself a global optimum that depends on the GLG
   answer; we leave this as an open problem (Discussion §5.2).
2. **Standard-shape coverage is empirical.** The class of BW standard
   shapes does not include multi-ko, large life-and-death uncertainty,
   or unusual closure patterns. The fraction of real $19 \times 19$
   endgames covered is an empirical question (open problem 4).
3. **Ko-freeness is strictly stronger** than Japanese simple-ko rule.
   Multi-ko situations are not handled.
4. **GLG cited as black box.** The 30-page Cr\^{a}\c{s}maru--Tromp proof
   is used as a building block; we do not re-prove it.

## Reviewer's Most Likely Objection

"The lower bound is just a packaging of Cr\^{a}\c{s}maru--Tromp; the upper
bound is just standard BW theory. Where is the new content?"

Response strategy: (a) The swing-control lemma (Lemma 3.2) is genuinely new
and was the missing calibration step in informal accounts; the explicit
polynomial gap $D_Y - D_N = \Omega(|B|)$ closes a previously hand-waved
step. (b) The unification across four readings $X \in \{B, C, D\text{-must},
D\text{-avoid}\}$ in a single reduction template is new. (c) The
prefix-sum closed-form evaluation of optimal-sequel scores in
Theorem 4.4 is new and reduces $D$-must from naive $O(m^2)$ to $O(m)$.

## File Info

- **Source:** paper.tex (single-file LaTeX, amsart)
- **Estimated PDF length:** 6--8 pages compiled
- **Bibliography:** 7 references
