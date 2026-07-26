# EXP G results — Q-PVL graph atlas (spectral graph invariants from qubitized-walk moments)

Date: 2026-07-21 · Engine: qpvl_core (per-rung Möbius warp, K=24 Chebyshev moments, NNLS positive quadrature, two-flag protocol) · Frozen registration: `registration_G.md` (bars set before any pipeline number existed).

Targets: T1 pairwise effective resistance R_uv incl. regularized curve R(s) and s→0 endpoint; T2 Kirchhoff index R_tot = n·tr(L⁺); T3 spanning-tree count ln τ via matrix-tree. Graphs: LastFM Asia (SNAP, n=7,624, m=27,806, λ₂=0.0669, λ_max=217.05), designed 8-decade SBM (n=4,096, 8 communities, three w=1e-3 bridges, four designed-empty decades), n=60 ER control.

## 1. Prediction ledger

| ID | Quantity | Frozen bar (kill) | Measured | Verdict |
|---|---|---|---|---|
| P-G1 | Control: Foster's theorem / forest-ratio identity | ≤0.5% (5%) | 0.0016% / 0.002% max | **PASS** |
| P-G2a | LastFM in-band R(s) sweep, median | ≤0.5% | 0.00033% (worst port 0.31%) | **PASS** |
| P-G2b | s→0 R_eff extrapolation, med / p90 | ≤2% / ≤5% (med>25%) | 0.00083% / 0.019% | **PASS** |
| P-G3 | Noisy R_eff ε=3e-4, trial-median med / p90 | ≤5% / ≤12% | 0.255% / 1.385% | **PASS** |
| P-G3 | Noisy R_eff ε=1e-3, trial-median med | ≤10% (40%) | 1.064% | **PASS** |
| P-G4a | ⟨z\|L⁺\|z⟩ quadrature leg, median | ≤2% | 0.328% (worst probe 1.96%) | **PASS** |
| P-G4b | R_tot end-to-end (M=8 Hutchinson) | ≤8% (50%) | 0.686% | **PASS** |
| P-G4c | R_tot under noise ε=3e-4 | ≤10% | 1.305% | **PASS** |
| P-G5a | ⟨z\|ln L\|z⟩ quadrature leg, median | ≤0.02 nats/node (0.5) | **0.0422** (range 0.014–0.089) | **FAIL — M-D** |
| P-G5b | ln τ end-to-end | ≤0.10 nats/node | 0.0436 (+333 nats on 9479) | PASS † |
| P-G5c | ln τ under noise ε=3e-4 | ≤0.15 nats/node | 0.0225 | **PASS** |
| P-G6 | SBM: g-rule prunes 4 empty decades, keeps 1e-6/1e-5 for inter ports, pruned err ≤2× full | (any port >10× = kill) | empty decades pruned ✓, **but 1e-6/1e-5 also pruned on all ports**; pruned/full = 212× / 1.4e5× / 584× / 4587× | **FAIL — M-F (named risk fired)** |
| P-G7 | Stitched mass defect, med / max | ≤5% | 0.80% / 3.52% | PASS ‡ |
| P-G8 | Deflation drift | ≤1e-8 | 3.9e-16 (LastFM), 3-16 class (SBM) | **PASS** |
| X-G1 | Joint-NNLS beats stitched on both quad legs | ≥6/8 probes | **8/8** | PASS → promoted |
| X-G2 | Facebook MUSAE n=22,470 scale-up | optional | not run | — (declared non-failure) |

† Passed its loose end-to-end bar while its own quadrature leg failed P-G5a: the bar pair was inconsistent. Do not cite P-G5b as validation of the stitched log route.
‡ Gate passed yet did not protect the log functional — the 5% mass bar is mis-calibrated for log-class kernels (ln λ spans ±7 over the grid; a +1% seam defect at ln λ≈+5 is ~0.05 nats/node by itself). R3-style annotation: gate needs a kernel-weighted form.

Registered: 11 pass, 2 fail, both failures with pre-named mechanisms confirmed quantitatively below.

## 2. Failure autopsies

**P-G5a → M-D (stitch seam overcount).** Signed stitched-mass defects are positive on all 8 probes: +0.5% to +3.5%. Each rung's model is individually unit-mass (1.0000 ±1e-4), but adjacent rungs apportion seam decades differently — e.g. rung σ=0.1 places 65.9% of its mass in decade [1,10) where rung σ=10 places 52.8% — so nearest-rung band-taking sums to >1, concentrated at high λ. Overcount δm ≈ +1–3% × ⟨ln λ⟩_seam ≈ +4.5 × nb² ≈ 7623 reproduces the observed +333 nats. Consistency check: the 1/λ functional de-weights exactly those decades and came in 10× cleaner (0.33%). Additional finding stored for the record: rung σ=1e3 parks 15% of its model mass at the grid floor (unresolvable below σ/100) — harmless under nearest-rung evaluation, poison if any composite construction ever admits it.

**P-G6 → M-F compounded by M-C.** Measured inter-community small-mode mass (modes 2–8, λ ∈ [8.9e-7, 2.3e-5]) is 1.953e-3 on all three inter-type ports — below G_CUT = 5e-3, and below the ~4e-3 pre-run estimate. The g flag is a *mass* detector; R_eff at s=0 is a *1/λ-weighted* functional; community bridges are precisely low-mass/high-leverage. So g pruned the only informative rungs. The >100% pruned errors (1089%, 1183%) are M-C: with the small rungs gone, R_eff extrapolates from the σ=1 rung's model, whose sub-band mass is unconstrained fit garbage at the 1e-7 grid floor with ×1e7 leverage. Full-ladder control on the same ports: 0.008–0.32% across 8 spectral decades — the pipeline handles the spectrum; only the pruning decision fails. Intra-community port: mass 6.8e-15, pruned correctly, 7.7e-5% error — the flag's intended regime works. Repair is scoped and frozen in `registration_G2.md` (leverage-weighted pruning, zero extra shots); per discipline, not run this session.

## 3. X-G1 promotion and the span mechanism

The joint fit (one NNLS over the union of all alive rungs' moments, single exact mass row) reaches 1.2e-9 median error on ⟨z|L⁺|z⟩ and 2.5e-12 nats/node on ⟨z|ln L|z⟩ — machine precision, 9–12 orders below stitched. This is not luck; it is quadrature exactness inherited from the dictionary:

**Prop-G (sketch).** For any positive measure ŵ matching the rung moments, |∫f dŵ − ∫f dw_z| ≤ ‖b‖²·2E_N(f) + (moment noise)·‖coeffs‖₁, where E_N(f) is the best uniform approximation of f on [λ₂, λ_max] by span{1} ∪ {T_k(y_{σ_d}(λ))}. That span is a rational family with log-spaced poles — Zolotarev class — so for f ∈ {ln λ, 1/λ}, E_N ~ e^(−cN/log(λ_max/λ₂)); at N≈116 across 4.5 decades this is ≲1e-12, matching observation. The practical consequence: **one measured moment set answers every functional in the rational span at dictionary-limited accuracy**, which is the graph-atlas claim with a mechanism attached. Candidate Proposition 2 for a graphs paper.

End-to-end, the joint route is Hutchinson-limited as it should be: R_tot 0.169%, ln τ 0.00130 nats/node (M=8, probe RSD 1.43%/√8 ≈ 0.5%). Under noise, ln τ is effectively noise-immune (0.00126 at ε=3e-4, 0.00118 at 1e-3 — the log coefficient norm is tiny), while R_tot degrades to 0.81%/3.12% — at ε=1e-3 slightly *worse* than stitched (2.64%): the 1/λ span coefficients amplify moment noise. Reported as measured; the promotion claim is for accuracy class and log-family robustness, not uniform dominance.

## 4. Amendments log (all pre-comparison, none affecting frozen bars)

1. **Reference generator replaced.** Registered plan used dense eigendecomposition for LastFM truth. The 4 GB/1-core sandbox killed it twice (wall-clock, then silent OOM on values-only). Amended to: sparse LU solves for R(s)/R_eff/⟨z|L⁺|z⟩ (shift 1e-9), reduced-Laplacian sparse-LU logdet for ln τ (exact matrix-tree), fully reorthogonalized Lanczos (k=500) for per-probe log quads, and n=7,624 blocked exact solves for tr L⁺. Cross-validation between independent generators: Lanczos vs solves 2.0e-9 (limited by the solve shift), Lanczos k=300 vs k=500 self-consistency 2.5e-14. Amendment made before any quadrature-leg comparison was computed.
2. **scipy nnls iteration cap.** The joint 116×400 system trips the default cap; raised to 200×n_cols with lsq_linear(trf, bounds≥0) fallback. Per-rung fits unaffected.
3. **SIGPIPE incident.** One compare script died mid-pipe before its JSON write; rerun with write-before-print, numbers identical. No contamination.

## 5. Cost ledger (depth D_d = ⌈4√(α/σ_d)⌉)

LastFM (α=271.32): D = {659, 209, 66, 21, 7, 3} for σ = 1e-2…1e3, ΣD_full = 965 per moment set. g-pruning drops σ=1e-2 on all 20 columns (empty decade below λ₂) and more on hub-localized ports (top-hub port runs on {10,100,1000}: ΣD = 31 — a 31× depth saving where structure permits). f-flag (<0.51) fires on the 2–4 smallest alive rungs per column → those rungs ledgered at ×100 shots per the inherited ε/10 repair; deep rungs (σ≥10, f≥0.6) stay at base shots. SBM: ΣD_full = 33,793, dominated by σ=1e-6 (23,104) — exactly the rungs a correct pruner must *keep* for inter-community ports, so the honest depth story on community graphs is "pay for the decades your question lives in," not "prune to 35."

## 6. What did we find, simply

Pointed at a real social network, the chip engine's measurement plan answered three classically expensive questions from one shopping list of numbers: the electrical distance between any two people (to ~0.001% noiseless, ~0.3–1% under realistic noise, including the exact s=0 endpoint the chip work never attempted), the network's total resistance (0.7%), and its number of spanning trees — about 10^4116 — to a tenth of a percent in the log. The one-big-fit reading of the same data is provably the right one: the measurement family is secretly an optimal rational dictionary for logs and inverses, so it computes those functionals at machine precision. Two pre-named risks fired and are now measured mechanisms with scoped fixes: decade-stitching double-counts at seams (use the joint fit), and the emptiness flag prunes exactly the low-mass, high-importance community modes that carry a graph's resistance (leverage-weighted pruning, frozen for next session).

## 7. Repro map

`registration_G.md` (frozen) · `registration_G2.md` (frozen, next) · code: `graphatlas.py`, `setup_testbed.py`, `stage2a_pipeline.py`, `stage2truth_solves.py`, `lanczos_truth.py`, `stage2c_compare.py`, `autopsy2.py`, `run_noise.py`, `run_sbm.py`, `run_control.py`, `make_figs.py` · results: `res_control.json`, `res_stage2c.json`, `res_autopsy.json`, `res_noise.json`, `res_sbm.json` · checkpoints: `stage2a.npz`, `stage2truth_solves.npz`, `lanczos_truth.npz`, `lastfm_W.npz`, `sbm_W.npz` · figures: `figs/fig1–4`. Seeds: ports 2026, probes 31337, noise 424242, control 7.


---
## Post-hoc amendments (2026-07-21, later session; labeled per protocol — no frozen number above is altered)

1. **EXP G2 executed.** The repair registered in `registration_G2.md` has been run (see `../expG2/results_G2.md`). Substance: the P-G6 mechanism (M-F) is repaired — inter-type ports 68–1183% -> 0.008–0.32% (full-ladder accuracy, ratio 1.0); the intra port is pruned harder than the g-rule (SumD 8 vs 35) at 4.6e-7% error; LastFM median improves 7,500x (8.3e-4% -> 1.1e-7%) including five latent sub-cut columns corrected. Three frozen G2 clauses failed for registration-design reasons (a set-stability bar inappropriate to a target-aware rule — kill fired at 20/20 columns; two unfloored error-ratio bars evaluated at numerical floor), reported in full in the G2 ledger with a corrected bar form proposed for future freezes.
2. **Environment-attribution correction.** The amendment log above attributed dead background reference jobs to "silent OOM". Subsequent evidence (EXP H session) shows background processes are reaped at bash-call boundaries in this sandbox; the OOM attribution is superseded. The amended reference plan itself and its 2.0e-9 cross-validation are unaffected.
