# Paper B — Hotstrat Optimality Fails: Structural Counterexamples in Mixed-Sum Combinatorial Games

## Summary

Establishes three distinct failure modes for the standard
``play-the-hottest-region'' (Hotstrat) heuristic in disjunctive sums of
combinatorial games. (1) An explicit two-summand mixed-sum game $G + H$
with hot follow-up showing Hotstrat is suboptimal by 6 points. (2) A
structural pairwise-tie identity $V_{\sigma(2k)} = V_{\sigma(2k+1)}$ for
the must-play ranking on simple-switch sums of size $m \geq 3$, in stark
contrast to the strict swing ranking. (3) A substantive divergence
between the avoid-play top-1 and the swing top-1 region. The three
results together fully describe the divergence among the three standard
formalizations of ``best move'' in Berlekamp--Wolfe-style endgame
analysis.

## Key Result

**Main Theorem (Theorem 3.1):** There exists a two-summand mixed-sum
game $P = G + H$ with $\Tt(G) > \Tt(H)$ in which the unique Black-optimal
first move is in $H$ and Hotstrat is suboptimal by $\LS(P) -
\LS(P \mid \text{play } G) = 8 - 2 = 6$ points.

**Companion Theorems (Theorems 5.1, 6.1):**
- The must-play ranking on $\sum_{i=1}^m \{a_i \mid b_i\}$ exhibits
  pairwise ties $V_{\sigma(2k)} = V_{\sigma(2k+1)}$ for every $k$ with
  $2k+1 \leq m$, while the swing ranking is strict.
- There exists a sum-of-simple-switches plus baseline number summand for
  which the avoid-play top-1 differs from the swing top-1.

## Target Journals (ranked)

1. **INTEGERS** (Combinatorial Game Theory) — natural specialty venue;
   the structural-ties identity (Theorem 5.1) is the kind of clean
   algebraic-combinatorial result they value. Estimated acceptance:
   55--65%.
2. **The Electronic Journal of Combinatorics** — also natural for
   game-theoretic combinatorics. Estimated: 40--50%.
3. **Theoretical Computer Science** — viable if framed as a
   negative/structural result for game-theoretic algorithms. Estimated:
   30--40%.
4. **arXiv preprint (math.CO + cs.GT)** — first deposit for community
   feedback.

## MSC 2020 Classification

- **91A46** (Combinatorial games) — primary
- **91A05** (2-person games) — secondary
- **05A05** (Permutations, words, matrices) — secondary

## Submission Strategy

1. Post to **arXiv** (math.CO + cs.GT) for community feedback.
2. Solicit informal feedback from CGT community (Siegel's network).
3. After 2--4 weeks, submit to INTEGERS (specialty venue with native
   audience for this material).

## Must-Cite Related Work

- Conway 1976 (On Numbers and Games) — foundational CGT framework.
- Berlekamp, Conway & Guy 1982 (Winning Ways) — thermograph theory and
  hotstrat-on-switches for the all-small / pure-switch case.
- Berlekamp & Wolfe 1994 (Mathematical Go: chilling gets the last
  point) — cool-by-temperature framework that resolves the
  follow-up-aware analysis missing from naive Hotstrat.
- Siegel 2013 (Combinatorial Game Theory) — modern textbook treatment.
- Cr\^{a}\c{s}maru & Tromp 2000, Robson 1983 — complexity-theoretic
  context.
- Spight 2002 (Go thermography) — applied thermograph analysis on real
  endgame positions.

## Known Limitations (address before submission)

1. **The 19$\times$19 realization is schematic.** Section 7 sketches
   how each summand can be realized on a real Go board, but a fully
   verified life-and-death analysis would require a tsumego solver. The
   reader is reminded explicitly (Remark 7.1).
2. **Theorem 5.1 (pairwise ties) is restricted to simple-switch sums.**
   Extension to corridor sums or general BW standard shapes is open
   (Discussion 8.2.2).
3. **Quantitative loss bound for Hotstrat is missing.** We exhibit a
   specific 6-point loss; bounding worst-case loss in terms of the
   follow-up swing is open (Discussion 8.2.4).
4. **No classification of failure cases.** We give one explicit failing
   instance; a structural classification of all mixed-sum games where
   Hotstrat fails is open (Discussion 8.2.3).

## Reviewer's Most Likely Objection

"Hotstrat failure on mixed sums with hot follow-ups is folklore;
practitioners have known this for decades, and the BW cool-by-temperature
framework is precisely the response. What is genuinely new here?"

Response strategy: (a) The fully enumerated counterexample with
explicit thermograph computation and complete game-tree enumeration
(Theorem 3.1 + Proposition 3.2) appears not to be in the published
literature in this clean self-contained form. (b) The structural-ties
theorem (Theorem 5.1, $V_{\sigma(2k)} = V_{\sigma(2k+1)}$) is, to the
author's knowledge, new as an isolated structural identity. (c) The
substantive divergence between avoid-play and swing top-1 (Theorem 6.1)
is also new. (d) The unified treatment of the three readings on a
single instance (Section 8.1) is a contribution to clarifying the
folklore.

## File Info

- **Source:** paper.tex (single-file LaTeX, amsart)
- **Estimated PDF length:** 6--8 pages compiled
- **Bibliography:** 7 references
