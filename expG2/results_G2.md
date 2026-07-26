# EXP G2 results — leverage-weighted pruning: the repair works; three frozen clauses fail anyway, and all three failures are ours

Date: 2026-07-21 · Frozen registrations: `registration_G2.md` (main, frozen last session), `registration_G2_addendum.md` (hypercube testbed, frozen this session before any addendum number). Zero new quantum shots anywhere: LastFM scored from the archived `stage2a.npz` models; SBM rebuilt deterministically; hypercube via the P-H1-validated synthesis.

## 0. Authenticity gates (SBM rebuild after container reset)

Rebuilt from `sbm_W.npz` + seed 2026: recomputed g-flags, port truths, and full-ladder errors match the archived EXP G record **bit-exactly** (all three gates = 0.0). Every SBM number below is scored on the authentic frozen instance.

## 1. Main ledger (registration_G2.md, scored verbatim)

| Clause | Frozen bar | Measured | Verdict |
|---|---|---|---|
| P-G2R1a: LWP prunes all 4 designed-empty decades, every port | — | none of {1e-4..1e-1} kept anywhere | **PASS** |
| P-G2R1b: retains BOTH 1e-6 and 1e-5 on the 3 inter-type ports | — | all three keep exactly {1e-6, 1e-5} | **PASS** |
| P-G2R1c: pruned/full error ratio ≤ 2, every port | kill > 10 | ratios [1.0, 1.0, **3.52**, 1.0] | **FAIL** (declared-risk band R-G2a; no kill) |
| P-G2R2: intra drops ≥ 6/9 rungs incl. 1e-6, 1e-5 | — | keeps only {10}: drops 8/9 | **PASS** |
| P-G2R3: LastFM alive sets change on ≤ 2/20 columns | **kill > 4** | **20/20 columns changed** | **FAIL — KILL FIRED** |
| P-G2R3 accuracy clause: s→0 median ≤ 0.0017% | kill > 0.5% | **1.11e-7%** (was 8.31e-4% under g) | pass, ×7500 improvement |

## 2. What the repair actually did (the substance)

**SBM — M-F fixed on the exact failing instance.** The three inter-type ports go from the g-rule's 68–1183% to **0.008–0.32%** — identically full-ladder accuracy (ratio 1.0), because LWP retains the two rungs where the resistance actually lives. The honest depth price comes with it: ΣD for those ports is 30,410 of the full 33,793 (D(1e-6)=23,104 is not optional; community resistance is intrinsically deep — consistent with Prop. 1's corollary in the paper). Where structure is absent, LWP is *more* frugal than g: the intra port keeps one rung (ΣD **8** vs g's 35 vs full 33,793 — a 4,200× saving at 4.6e-7% error).

**LastFM — the kill, and why it is a registration design error, not a rule defect.** All 20 columns changed because LWP is target-aware by construction: for the frozen weight w = 1/λ it correctly drops the top rungs (σ=10³, often 10²) whose bands contribute negligibly to any resistance, and — the substantive finding — it **adds σ=0.1 on five columns (0, 5, 6, 7, 8) where the g-rule had been silently discarding sub-cut small-λ mass that matters**: latent mini-M-F cases on the real graph. That is why the median error *improves* 7,500× (8.31e-4% → 1.11e-7%). The frozen "≤2 columns" bar encoded the wrong expectation — it asked a target-aware rule to behave like a target-agnostic one. Per discipline the kill stands as a kill: **LWP is not a drop-in regression-safe patch; it is a different pruner that was strictly more accurate on every testbed measured.** The set-stability framing is dead; the accuracy framing is what the next registration should carry.

**P-G2R1c's miss is a ratio-of-floors artifact.** Intra: full-ladder 1.31e-7% vs LWP 4.63e-7%. Both are numerical-noise-floor numbers; their ratio (3.52) is meaningless but the bar is the bar — reported as the declared-risk miss R-G2a anticipated, with no within-session retune of C_REL.

## 3. Addendum ledger (registration_G2_addendum.md)

| Clause | Frozen bar | Measured | Verdict |
|---|---|---|---|
| A1: ℓ=14 — LWP keeps σ=1e-3 on all 3 weak-support ports; ratio ≤ 2 each | kill > 10 | kept on all three; errors **0.059% / 0.123% / 0.123%** (g-rule: 109% / 155.5% / 155.6%), ratios 1.0 | **PASS — the EXP H P-H2 failure is repaired** (×1263 → ×1.0) |
| A2: d1 prunes ≥2/6 incl. 1e-3; ratio ≤ 2 | — | prunes 4/6 incl. 1e-3 ✓; **ratio 9.7e8** | **FAIL as written** (floor artifact: full-ladder error 9e-13%, LWP 8.7e-4% — the same absolute value EXP H accepted from the g-rule) |
| A3: ℓ=266 — LWP alive ⊆ {1e2,1e3} every column; ΣD=13 unchanged | kill: any σ≤10 kept | alive = **{100}** everywhere; no kill; ΣD **10** | **PASS** on subset + kill clauses; "unchanged" sub-clause missed in the favorable direction (13 → 10: LWP also drops σ=10³, D=3, as irrelevant to 1/λ) |

## 4. A bar-design defect, demonstrated twice, with the fix for future freezes

Two ratio clauses (P-G2R1c at 3.52, A2 at 9.7e8) failed purely because the denominator sat at machine floor while both absolute errors were far inside every accuracy bar in the campaign. Unfloored ratios are a defective bar form. Proposed form for all future registrations (NOT retro-applied to any score above): `err_LWP ≤ max(2 × err_full, 0.01%)`. Under that form both clauses would pass; under the frozen forms they fail, and they are reported as failures.

## 5. Status of Assumption 1 (pruning soundness) after G2

Measured under LWP with w = 1/λ: **holds on every testbed in the campaign** — SBM (the original counterexample), LastFM (including five latent cases the g-rule was quietly getting slightly wrong), hypercube ℓ=14 (the second counterexample), hypercube ℓ=266 (concentration savings preserved and slightly improved, ΣD 13→10). Open, unchanged: C_REL=1e-3 remains untuned (frozen; no within-session retune per R-G2a); the ln λ target weight is unregistered (R-G2c); no noise arms (out of frozen scope). The paper's Assumption-1 and limitations text updated accordingly (v0.3).

## 6. Plainly

The emptiness detector was pruning by "is there mass here?" when the right question is "does the answer care about the mass here?" Asking the right question fixes every failure we had — the community graphs that were wrong by up to ×1263 are now as accurate as running everything, the giant graphs stay as cheap as before or cheaper, and the method even quietly fixed five small errors on the real social network nobody had flagged. Three of our own pre-frozen test clauses still failed: one because we asked the new rule to imitate the old rule's decisions (it shouldn't), and two because we wrote error-ratio tests that divide by numbers at the machine's noise floor. All three are our registration mistakes, reported as failures, with the corrected bar form written down for next time.

## 7. Repro map

`g2_main.py` (LastFM from archived `stage2a.npz` + SBM deterministic rebuild + gates) → `res_G2.json` · `g2_addendum.py` (ℓ=14, ℓ=266 synthesis) → `res_G2_addendum.json` · registrations: `registration_G2.md` (frozen prior session), `registration_G2_addendum.md` (frozen this session, pre-run). C_REL=1e-3, w=1/λ, band map = stitcher-identical nearest-log assignment. No new shots.
