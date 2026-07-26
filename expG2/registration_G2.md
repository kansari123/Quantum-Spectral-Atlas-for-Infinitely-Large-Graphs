# EXP G2 pre-registration — leverage-weighted pruning (LWP) repair for M-F

STATUS: FROZEN 2026-07-21, before any LWP number has been computed. Everything not stated here is inherited unchanged from `registration_G.md`: same SBM testbed and seeds, same 4 ports, same LastFM setup, K=24, same grids, same noise model, G_CUT=5e-3 retained as a reported diagnostic.

## The rule (the only change)

Motivation (from the P-G6 autopsy): g measures *mass*; the target functionals weight mass by w(λ). Prune on estimated functional contribution instead.

For a resolvent-family target with weight w(λ) = 1/(λ + s_t) (s_t = 0 for R_eff):

- For each rung d, using rung d's OWN per-rung NNLS model Ŵ_d (already fitted from the K=24 moments — zero additional shots), compute the band-restricted contribution
  ĉ_d = Σ_{grid points g ∈ band(d)} Ŵ_d(g) · w(g),
  where band(d) is the nearest-log-rung assignment over the FULL ladder (identical band map to the stitcher).
- Prune rung d iff ĉ_d < C_REL · Σ_{d'} ĉ_{d'}, with **C_REL = 1e-3** (frozen).

Design notes, stated in advance: (i) the band restriction is the guard against M-C floor garbage — a rung's spurious sub-band mass lies outside its own band and cannot inflate its ĉ; (ii) the rule is self-referential (models judge themselves), same epistemic status as g, accepted; (iii) for multi-target sessions the alive set is the union over targets' alive sets.

## Frozen predictions

- **P-G2R1 (SBM, the failed case):** on the identical testbed/ports, LWP (a) still prunes all four designed-empty decades {1e-4,1e-3,1e-2,1e-1} on every port, (b) retains BOTH σ=1e-6 and σ=1e-5 for the three inter-type ports (far, adjacent, hub+rand), and (c) pruned-vs-full R_eff error ratio ≤ 2 on every port. KILL: any port ratio > 10.
- **P-G2R2 (savings preserved where structure is absent):** the intra-community port drops ≥ 6 of 9 rungs, including σ=1e-6 (D=23,104) and σ=1e-5 (D=7,306).
- **P-G2R3 (LastFM regression guard):** LWP alive sets differ from the current g-rule sets on ≤ 2 of 20 columns, and the s→0 R_eff error median stays ≤ 2× the EXP G value (0.00083% → ≤ 0.0017%). KILL: median > 0.5% or > 4 columns changed.

## Declared risks

- R-G2a: C_REL=1e-3 untuned; if P-G2R1c fails with ratio in (2,10], report as bar miss, do not retune within-session.
- R-G2b: band-edge leakage (a mode sitting exactly at a band boundary splits its ĉ between rungs) — prime suspect if P-G2R3 fails.
- R-G2c: for targets outside the resolvent family (e.g. ln λ), w must be re-declared; this registration covers w=1/(λ+s_t) only.

## Not in scope

No re-run of stitched functionals (superseded by promoted joint fit), no G_CUT retuning, no new testbeds, no noise arms (LWP decision uses noiseless flags per existing protocol).
