# REGISTRATION — EXP G: Q-PVL as a spectral graph-theory engine
Frozen 2026-07-21 BEFORE any pipeline output is computed on any testbed.
Setup measurements below were taken first (testbed characterization only,
mirrors the P1 pattern of freezing spectrum bounds with the testbed).

## 0. Problem statement (the graph-theory target)
Compute, for large sparse graphs, three classically expensive spectral
invariants from ONE set of qubitized-walk Chebyshev moment measurements:

  T1. Pairwise effective resistance R_uv = (e_u-e_v)^T L^+ (e_u-e_v),
      including the full regularized curve R_uv(s) = 2<b|(L+s)^{-1}|b>,
      b=(e_u-e_v)/sqrt(2), and its s->0 endpoint EXTRAPOLATION.
      Combinatorial meaning (matrix-tree): R_uv = F_uv / tau(G), the ratio
      of (# 2-forests separating u,v) to (# spanning trees).
  T2. Kirchhoff index R_tot = n * tr(L^+) = n * sum_{i>=2} 1/lambda_i
      (total effective resistance; Hutchinson probes).
  T3. Spanning-tree count: ln tau(G) = sum_{i>=2} ln(lambda_i) - ln(n)
      (matrix-tree theorem; same probes, log kernel).

This is outside chip design: the quantities are combinatorial counts and
random-walk invariants, and the deliverable is a per-port/per-probe
POSITIVE spectral measure ("graph atlas") from which any spectral
functional is read off.

## 1. What is inherited-validated vs new-at-risk
Inherited unchanged from the validated PDN campaign (not re-tested):
qubitized-walk moments <b|T_k(Y)|b> per Moebius rung Y=2s(S+s)^{-1}-1;
undamped truncation depth D_d=ceil(4*sqrt(alpha/sigma_d)); NNLS positive
quadrature on a 400-point log grid with k=0 row x100; nearest-rung
evaluation; two-flag protocol (g emptiness G_CUT=5e-3, f fragility <0.51
-> eps/10 on survivors); Gaussian eps-per-moment noise as validated
conservative proxy (R3); NO inverse-variance weighting of Hutchinson
probes (falsified boundary experiment: that noise is naturally uniform).

NEW, at risk, tested here:
  N1. Singular operator: L has known kernel span{1}. Handled by EXACT
      deflation (project every Y_apply output onto 1-perp). Graph analog
      of the exact capless Schur: structurally known subspace removed
      exactly, never modeled.
  N2. ENDPOINT EXTRAPOLATION s->0: PDN only ever evaluated inside the
      measured band. R_eff lives AT s=0, below the smallest rung. The
      pole model gives R_eff = 2*sum_j W_j/lambda_j analytically.
  N3. GLOBAL functionals (T2, T3) need one measure across all decades,
      not nearest-rung: PRIMARY = decade-stitched composite (each grid
      pole assigned to its nearest rung in log-lambda; take that rung's
      NNLS weights on its own band; concatenate). Mass-defect gate below.
  N4. Log kernel (T3) — new functional class, endpoint-sensitive.
  N5. C = I everywhere (all nodes "cap-bearing"): R_inf = 0, S = L.

## 2. Frozen testbeds (setup measurements, no pipeline touched)
CONTROL: G0 = connected ER, n=60, m=193, lambda_2=0.6556,
lambda_max=14.640 (dense; exact eig + exact matrix-tree determinants).
Saved control_A.npy, rng seed 7.

PRIMARY: LastFM Asia social network (SNAP-published; Rozemberczki-Sarkar
2020; fetched from karateclub mirror). n=7,624, m=27,806, connected,
degrees 1..216 (mean 7.29). Power-iter lambda_max ~ 217.05, alpha=271.32
(x1.25 margin), deflated-inverse-iteration lambda_2 ~ 0.06687. Span
lambda_2..lambda_max ~ 3.5 decades. Reference = dense eigendecomposition
(exact R_uv(s), exact R_tot, exact ln tau, exact per-probe quadratic
forms — quadrature error isolable from Hutchinson error EXACTLY).

PRUNING TESTBED: designed weighted SBM, n=4096: 8 communities x 512,
intra ER p=0.02 weight 1; 3 bridges weight 1e-3 between adjacent
communities (path topology). Setup: alpha=33.36, lambda_2 ~ 8.9e-7 —
mass normalization puts the 7 community modes at ~1e-6..1e-5, bulk
~[0.5, 27]. DESIGNED-EMPTY decades: 1e-4, 1e-3, 1e-2, 1e-1 (four).
Saved sbm_W.npz, rng seed 7 stream (same generator run).

## 3. Frozen protocol configuration
- Ladders: LastFM sigma in {1e-2,1e-1,1,1e1,1e2,1e3} (6 rungs).
  SBM sigma in {1e-6,...,1e2} (9 rungs). Control {1e-1,1,1e1,1e2}.
- K = 24 moments per rung, all rungs. mu_0 = 1 exact (normalization);
  noise applied to k>=1 only.
- NNLS grid: 400 log points on [1e-3, 1.2*alpha] (LastFM/control);
  [1e-7, 1.2*alpha] (SBM). Grid floor >= one decade below lambda_2 est
  (tb06 lesson). k=0 row and target x100 (inherited).
- Evaluation: R(s) curves by nearest-rung model (log-s), 25 log-spaced s
  in [sigma_min, alpha]. R_eff at s=0 from the SMALLEST SURVIVING rung's
  model. Global functionals from the stitched composite (N3).
- Deflation ON for all ports and probes (N1).
- Ports, LastFM (frozen selection rule, rng seed 2026): 6 uniform random
  pairs; 3 pairs = top-3 degree hubs each with a uniform random partner;
  3 pairs = BFS-eccentric node from random start paired with the 3
  farthest nodes. 12 ports total.
- Ports, SBM (seed 2026): far inter-community pair (comm0,comm7),
  adjacent inter (comm0,comm1), intra-community pair (comm3), hub+random.
- Probes: M=8 Rademacher, projected off 1, per graph (seed 31337).
  Uniform average (no weighting — inherited falsification).
- Noise arms: eps in {3e-4, 1e-3}, T=100 trials, iid N(0,eps^2) per
  moment k>=1 per rung. f<0.51 rungs get eps/10 (inherited R2 repair;
  logged in cost ledger as x100 shots on those rungs).
- Cost ledger (reported, no bars): D_d = ceil(4*sqrt(alpha/sigma_d)),
  SumD full vs pruned; Sum_d K*D_d.

## 4. Frozen predictions and kill lines
Metric convention: relative error vs dense-eig (LastFM/control) truth.
"med/p90" over the declared port or probe sets; noise arms additionally
med/p90 over T=100 trials of the per-port median.

P-G1 (control identities, noiseless): (a) Foster's theorem:
  |sum_{edges} R_hat_uv - (n-1)|/(n-1) <= 0.5%. (b) Forest-ratio: for 10
  frozen edges (seed 2026), R_hat_uv vs det-ratio tau(G/uv)/tau(G)
  agree <= 0.5% each. KILL if either > 5% (wiring bug; stop and fix
  with mechanism before any other run).

P-G2 (LastFM resistance, noiseless): (a) in-band sweep: per-port
  band-max relative error over the 25-point s-grid, median over 12
  ports <= 0.5%. (b) s->0 extrapolated R_eff: median <= 2%, p90 <= 5%.
  KILL if (b) median > 25% (extrapolation unusable).

P-G3 (LastFM R_eff under noise): eps=3e-4: median-over-ports of
  per-port trial-median <= 5%; per-port trial-p90, median over ports
  <= 12%. eps=1e-3: trial-median median <= 10%. KILL if 3e-4 median
  > 40%.

P-G4 (Kirchhoff index): (a) quadrature leg, noiseless: per-probe
  stitched-composite value vs per-probe EXACT quadratic form
  <z|L^+|z>, median over 8 probes <= 2%. (b) end-to-end R_tot_hat
  (M=8, noiseless) <= 8%. (c) eps=3e-4 trial-median <= 10%.
  KILL if (b) > 50% (probe-variance blowup mechanism).

P-G5 (spanning trees): (a) quadrature leg noiseless: per-probe
  |sum_j W_j ln(lambda_j) - <z|ln L|z>_exact| aggregated to
  |Delta sum_{i>=2} ln lambda_i|/n <= 0.02 nats/node. (b) end-to-end
  |ln tau_hat - ln tau|/n <= 0.10 nats/node (M=8, noiseless);
  (c) eps=3e-4 trial-median <= 0.15 nats/node. KILL if (b) > 0.5.

P-G6 (SBM two-flag pruning, noiseless, all 4 ports): g-rule with
  INHERITED G_CUT=5e-3 (not retuned) prunes ALL FOUR designed-empty
  rungs {1e-4,1e-3,1e-2,1e-1} and prunes NEITHER 1e-5 nor 1e0 for the
  two inter-community ports. Pruned-ladder R_eff error <= 2x full-ladder
  error per port. Depth saving reported (no bar).
  NAMED RISK (P-D3 mechanism): inter-community small-mode mass is
  ~4e-3 — BELOW G_CUT. If g prunes the informative 1e-6/1e-5 rungs on
  inter-community ports, this prediction FAILS and the failure is the
  result: g is a mass detector and R_eff is 1/lambda-weighted, so
  low-mass/high-leverage structure is exactly its blind spot.

P-G7 (stitch mass gate): |sum_stitched W - nb2|/nb2 <= 5%, median over
  all LastFM ports+probes. If violated, report defect and fall back to
  the declared exploratory joint fit for global functionals.

P-G8 (deflation drift gate): max over all recursions of
  |<1_hat, v_k>| <= 1e-8 with deflation ON. (Protocol gate, not
  physics.)

EXPLORATORY (thresholds declared now, per house rule):
  X-G1 joint-NNLS (single fit, rows = all rungs' k=1..23 plus one mass
  row x100): "improves" only if it beats the stitched composite on
  R_tot AND ln tau quadrature legs on >= 6/8 probes; otherwise verdict
  "no improvement", regardless of partial wins.
  X-G2 scale-up to MUSAE Facebook page-page (n=22,470, fetched) if
  session time allows: P-G2/3 bars apply unchanged; reference by sparse
  solves; tau leg by sparse-LU logdet only. Not running it is not a
  failure.

## 5. Named failure mechanisms (pre-declared, for honest autopsy)
  M-A null-leak: float mass at lambda=0 inflating 1/lambda sums.
      Gate P-G8; mitigation = deflation (declared protocol, not repair).
  M-B grid-floor misplacement (tb06 analog): spectrum mass below the
      NNLS grid floor. Mitigated by floor >= decade below lambda_2 est.
  M-C endpoint extrapolation: smallest-pole misplacement by factor r
      shifts R_eff by (small-lambda mass share) x (r-1).
  M-D stitch double-count/gap at decade seams (P-G7 gate).
  M-E probe-variance blowup for 1/lambda under heavy small-lambda mass
      (P-G4 kill line).
  M-F g-blind-spot on low-mass/high-leverage modes (P-G6 named risk).

## 6. Analysis plan
Run order: control (P-G1 gate) -> LastFM noiseless (P-G2, G4a/b, G5a/b,
G7, G8) -> LastFM noise arms (P-G3, G4c, G5c) -> SBM (P-G6) ->
exploratory. Every prediction reported pass/fail in a ledger table; any
failure gets a mechanism autopsy against Sec. 5 before any repair, and
repairs are labeled as such. Frozen numbers in this file are never
edited after runs begin.
