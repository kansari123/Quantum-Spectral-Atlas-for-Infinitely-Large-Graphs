# EXP I results — signed operators: the engine doesn't notice; the classical sampler dies on camera

Date: 2026-07-21 · Frozen registration: `registration_I.md` (first registration under the post-G2 floored-bar hygiene). Claim structure under test: (a) the moment engine's accuracy and cost are invariant under signs and phases, because it only ever touches the spectral measure, which stays positive; (b) the generic classical competitor of Prop. C3 (path-sampled return amplitudes) does not survive signs — measured, on the same instances.

## 1. Ledger

| ID | Frozen bar | Measured | Verdict |
|---|---|---|---|
| P-I1 engine invariance (torus, all six fluxes) | band ≤0.5%; endpoint ≤2%/p90 5%; noise ≤5% | band 0.000–0.117%; endpoint 0.000–0.324%/≤0.324%; noise 0.07–1.53% | **PASS** |
| P-I1 at T1b as registered | same | **VOID** — instance design error (see §2) | **VOID** |
| P-I1/I2 at T1b-R (declared repair) | same | λ_min=1.444; band 0.0011%; endpoint 0.0017%/0.0022%; lndet 2.9e-3; trinv 0.31%; noise 1.17%/0.0099/2.65% | **PASS** |
| P-I2 new functionals (all fluxes) | lndet ≤0.02/0.15 nats; trinv ≤2%/10% | lndet 3.0e-4–8.1e-3 / 0.008–0.039; trinv 0.09–1.12% / 1.2–7.6% | **PASS** |
| P-I3a sampler sign decay monotone | Spearman ≥0.9 | ρ = **0.900** (exactly at bar) | **PASS** (see §4) |
| P-I3b shot-multiplier ratio at t*=850 | ≥1e6 (kill <1e2) | **6.0×10^105** (fitted; direct sign death by t=28–121 at N=2e5) | **PASS** |
| P-I4 accuracy flat in flux (floored form) | ≤ max(2×p0-median, 0.01%) per class | band max 0.117%, endpoint max 0.324% (both p=2) | **FAIL** (see §5) |
| P-I5 implicit signed, ℓ=266 DOS arm | trinv ≤2%/10%; lndet ≤0.02/0.15 | **2.5e-10% / 2.9e-14 nats**; noisy 0.024% / 4.3e-5 | **PASS** (after 2 declared truth-construction repairs, §6) |
| X-I1 (descriptive) | — | LWP alive tracks the opening gap: {0.1,1,10}→{1,10} as λ_min crosses 0.37 | reported |

4 registered pass · 1 registered fail (bar design) · 1 registered instance void (design) with its declared repair passing everything · exploratory reported.

## 2. T1b void, owned

The registered signed SBM (intra +, inter −) is **balanced**: flipping one community's basis signs removes every negative edge (switching equivalence), so λ_min = 3.2e-15 — no frustration, a zero mode I had disabled deflation for, and endpoint/trace targets undefined as registered. Instance design error; the arm is void, not failed. Declared repair T1b-R (5% random sign disorder, seed 20261) is genuinely frustrated (λ_min = 1.444) and passes every P-I1/I2 bar with the best numbers of the whole T1 suite.

## 3. The headline, in numbers

**Engine invariance.** Across flux φ from 0 to π (frustration gap opening 0.038 → 1.17), and on the frustrated SBM: every accuracy class sits at or below EXP-G levels, using the identical fitter — the complex Hermitian operator's moments are real (max imaginary residue gated at 1e-10), the spectral measure stays positive, positivity keeps doing the regularizing, and NOTHING in the classical post-processing changed. The endpoint machinery runs with **no deflation and no zero mode** for the first time in the campaign — the frustration gap replaces the projector — and works out of the box.

**Sampler death.** The importance-sampled path estimator that *is* the Prop-C3 baseline (and provably recovers it at φ=0: average sign ≡ 1, measured) decays as ⟨s⟩ ~ e^(−Δ_s t) with Δ_s = 0.033–0.151 once flux turns on; the average sign is measured-dead (below 5/√N) by t = 28–121, versus the t* = 850 our σ=1e-2 rung requires. Fitted shot multipliers at t*: 10^24 (φ=π/16) to 10^111 (φ=π/2). Quantum ΣD at every flux: identical, by the same formula, with measured accuracy flat. **The quadratic-ceiling argument for sign-free graphs rests on a baseline that is now measured to be gone the moment signs appear.** Not claimed: instance hardness (dense diagonalization solved every explicit instance in seconds; the ℓ=266 family is free-fermion solvable — that is what made truth checkable), or an unconditional exponential speedup. What replaces the dead generic baseline is the conditional worst-case DQC1/BQP anchor, unchanged.

**Implicit scale, signed.** The π-flux chain-signed hypercube at n = 2^266 ≈ 1.2×10^80 (spectrum measured λ ∈ [96.66, 435.3]): per-node log-determinant — combinatorially, a cycle-rooted-spanning-forest free energy in the Forman/Kenyon sense, the signed generalization of EXP G's spanning-tree count — recovered to 2.9×10^-14 nats noiseless, 4.3×10^-5 under shot noise; tr(L^{-1})/n to 2.5×10^-10%. Single alive rung (concentration, again), ΣD = 10 versus naive 428.

## 4. A genuine physics finding inside P-I3

Monotonicity of the sign problem in flux is **not strict**: Δ_s(π/2) = 0.151 > Δ_s(π) = 0.143. Complex phases (φ=π/2) decorrelate the sampler faster than real signs (φ=π). Spearman lands at exactly the 0.9 bar — a pass, reported with its margin of zero. The finding is worth a sentence in any paper version: "hardest for the sampler" is not "maximally frustrated" but "maximally phase-incoherent."

## 5. P-I4's failure is the third bar-design lesson

All absolute errors across flux are ≤0.33% — comfortably inside every P-I1 bar — but the frozen P-I4 floor (0.01%) sits *below this estimator's natural cross-spectrum scale*: as λ_min sweeps through the ladder (0.038→1.17), the nearest-rung geometry shifts and medians move between 0.000% and 0.32%. Scored FAIL as frozen. Corrected floor for future registrations: class-bar/10 (here 0.05–0.2%), not an absolute 0.01%. Lesson series now: unfloored ratios (G2, twice) → floors below scale (here). The bar-hygiene rule is converging; none of it is retro-applied.

## 6. Two declared truth-construction repairs on T2, both caught by the pre-registered gates

R-Id fired twice, exactly as designed. (1) The registered "2ℓ×2ℓ Majorana quadratic" mechanism was wrong — X_iZ_{i+1} is fermion-parity-odd, not a JW quadratic; the pair search failed loudly. Correct route: frustration-graph fermionization (the terms' anticommutation graph is the cycle C_ℓ, a line graph), ℓ Majoranas on the root cycle, two boundary-condition sectors. (2) First sector construction failed the ℓ=8 gate; the diagnostic against exact truth showed values matching perfectly and weights off 2:1 — the sectors carry half the Hilbert space each and must be mixed 50/50 with per-sector normalization (periodic-ring zero modes contribute multiplicity, not values). The corrected construction gates on **values and weights** at ℓ=8 and ℓ=10 (both mod-4 classes... ℓ=8≡0, ℓ=10≡2; ℓ=266≡2 matches the gated class), and the ℓ=266 dual-generator gate (convolution vs 5×10^6-sample MC) agrees within standard errors. No hand-derived spectrum ever entered a truth number; every construction decision was arbitrated by an exact gate — which is the entire point of the design.

## 7. Plainly

We put signs and magnetic phases on the graphs — the thing that breaks every generic classical sampling method — and our machine did not notice: same accuracy, same circuit depths, no changes to a single line of the fitting code, from a 1,024-node magnetic lattice to a signed graph with more nodes than atoms in the universe. Meanwhile we ran the fair classical competitor on the same problems and watched its signal die: by the depth our circuits need, it would require 10^24 to 10^111 times more samples. Our own scorecard still has honest stains: one test instance I designed turned out to secretly have no sign problem at all (fixed with a disordered variant), one cross-check bar was set tighter than the method's own natural precision, and the exact-solution machinery for the giant signed graph took me two corrected attempts — each mistake caught by the checks we froze in advance for exactly that purpose. Net: the door we said was the only one still open is now propped open with measurements. What remains genuinely unclaimed, as always: nobody has proven these problems are hard for *every* classical algorithm — only that the standard one is dead.

## 8. Repro map

`registration_I.md` (frozen) · `expI_t1.py` (torus fluxes + T1b, dense truths, dual gates) · `expI_t1bR_sampler.py` (T1b-R repair + path-MC sign decay) · `expI_t2v3.py` (gated fermionization + ℓ=266; v2 preserved as the failed-round record) · results: `res_I_t1.json`. Seeds: ports 2026, probes 31337, noise 434343, sampler 555+p, MC truth 777, disorder 20261. t* = ⌈α/σ⌉ = 850 at σ=1e-2, α=8.5, N=2×10^5 walkers.
