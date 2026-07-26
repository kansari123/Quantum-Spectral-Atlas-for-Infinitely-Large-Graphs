# EXP I pre-registration — signed and magnetic Laplacians: the engine unchanged where the classical sampler dies

STATUS: FROZEN 2026-07-21, before any EXP I number has been computed. Inherited unchanged unless stated: K=24, per-rung NNLS positive quadrature (row-0 x100), joint fit as registered primary for global functionals, Gaussian eps-per-moment noise proxy (eps=3e-4, T=100, seed 434343), D_sigma = ceil(4*sqrt(alpha/sigma)), G_CUT=5e-3 reported as diagnostic, LWP (G2 rule, C_REL=1e-3, w=1/(lambda+s_t)) as the pruning rule. NEW BAR HYGIENE (first use, per G2 lesson): every accuracy-comparison clause is floored — err_A <= max(2*err_B, 0.01%). No unfloored ratios anywhere in this registration.

## Why signed operators

The moment protocol touches only the SPECTRAL MEASURE, which is a positive measure on the real line for any Hermitian operator — positivity (our regularizer) survives arbitrary signs and phases in the matrix elements, and all moments <b|T_k(y_sigma(L))|b> remain real. The generic classical competitor of Prop. C3 (path-sampled return amplitudes) does not survive: signed/complex path weights create a sign problem with exponentially decaying average sign. EXP I measures both halves of that sentence on the same instances.

## Instances

- T1a (magnetic torus, explicit): 32x32 periodic square lattice, Landau gauge, per-plaquette flux phi = 2*pi*p/32 for p in {0,1,2,4,8,16} (phi from 0 to pi). n=1024, unit weights, alpha = 8.5 (bound > lambda_max). Frustration gap lambda_min > 0 for p>0; NO deflation for p>0 (no zero mode).
- T1b (signed SBM, explicit): two communities of 512; intra edges weight +1 (Erdos-Renyi p_in=0.02), inter edges weight -1 (p_out=0.01), seed 2026. Classic frustrated two-community signed graph. alpha = 2*max weighted |degree| bound computed at build, frozen procedure not value.
- T2 (implicit signed, DOS arm only): pi-flux "chain-signed" hypercube on Z_2^l: L = sum_{i=1}^{l} w (I - X_i Z_{i+1 mod l}), w=1 — a genuine signed graph on 2^l vertices (edge (x, x xor e_i) has sign (-1)^{x_{i+1}}). Free-fermion reducible: many-body levels lambda = w*l - sum_k s_k eps_k with single-particle eps_k from the 2l x 2l Majorana quadratic form, computed NUMERICALLY at runtime (no hand-derived spectrum enters truth). l=10 (fermionization authenticity gate vs dense 2^10 eig), l=266 (implicit scale). Ports are NOT synthesized at implicit scale (port measures of Gaussian states are not poly-accessible to us); the T2 arm is DOS/global-functionals only, stated as a scope limit.

## Targets

Explicit (T1): R(s)-analogue curves <b|(L+s)^{-1}|b> over 25 log shifts in [1e-3, alpha]; the s->0 endpoint <b|L^{-1}|b> — for p>0 this is FINITE WITHOUT DEFLATION (new regime: no zero-mode projection anywhere); per-node ln det L via joint fit over 8 Rademacher probes (combinatorial meaning per Forman/Kenyon: log of the cycle-rooted-spanning-forest partition function — the signed generalization of EXP G's spanning-tree count); tr(L^{-1})/n. Ports: 6 node pairs (seed 2026: 3 random, 2 max-|deg|-anchored, 1 antipodal-in-lattice) + 8 probes (seed 31337).
Implicit (T2): tr(L^{-1})/n and ln det L / n vs dual-generator truth.

## Truth generators (dual, gated, per campaign law)

T1: (i) dense eigh of the exact Hermitian matrix; (ii) direct dense solves (lu_factor) for resolvent curves; gate <= 1e-9 relative between routes on every reported quantity class. T2: (i) fermionic level structure -> distribution of sum s_k eps_k via 2^20-bin convolution; (ii) independent Monte Carlo over s in {+-1}^l, N=1e7, seed 777; gate: |generator difference| <= 3 MC standard errors AND <= 1e-4 relative. l=10 fermionization gate: many-body spectrum from Majorana route matches dense eig of the actual 1024x1024 signed matrix to <= 1e-9 (KILL: mismatch voids the entire T2 arm — reported as void, not fail).

## Ladders

T1: sigma in {1e-3, 1e-2, 1e-1, 1, 10}, grid 400 log pts on [1e-4, 1.2*alpha]. T2: sigma in {1e-1, 1, 10, 100, 1000} (spectrum centered near w*l = 266), grid 400 log pts on [1e-2, 1.2*alpha_T2], alpha_T2 = 2*l*w.

## Frozen predictions

- P-I1 (engine invariance under signs, explicit): for EVERY flux p and for T1b — in-band curve error median <= 0.5%; endpoint median <= 2%, p90 <= 5%; noise eps=3e-4 trial-median median <= 5%. KILL: any noiseless median > 10%.
- P-I2 (new functionals, explicit): ln det L per node, joint fit: |Delta| <= 0.02 nats/node noiseless, <= 0.15 noisy; tr(L^{-1})/n <= 2% noiseless, <= 10% noisy. Applies at every flux and T1b.
- P-I3 (measured breakdown of the generic classical sampler): on T1a, path-MC estimation of <u|(I - L/alpha)^t|u> with |weight| importance sampling (the estimator that IS the Prop-C3 baseline at phi=0): (a) the average sign magnitude decays as exp(-Delta_s(phi) t) with fitted Delta_s monotone nondecreasing in phi (Spearman rho >= 0.9 over p in {1,2,4,8,16}); (b) the shot multiplier to reach fixed per-moment precision at depth t* = ceil(alpha/sigma) for sigma = 1e-2 satisfies multiplier(phi=pi) / multiplier(phi=0) >= 1e6. KILL: ratio < 1e2 (the generic sampler survives signs; the premise of EXP I is falsified — to be reported as the headline if so).
- P-I4 (accuracy flat in frustration): for each error class in P-I1/P-I2, max over p of the median <= max(2 x the p=0 median, 0.01%) (floored form).
- P-I5 (implicit signed, DOS arm): l=266 — tr(L^{-1})/n error <= 2% noiseless / <= 10% noisy; ln det L / n <= 0.02 nats noiseless / <= 0.15 noisy; LWP alive set and Sum D reported (no bar on the set: first signed instance, no prior). KILL: any noiseless > 10%.
- X-I1 (exploratory, kills nothing): LWP behavior across flux on T1a — whether alive sets shift as the frustration gap opens; descriptive.

## Named risks

- R-Ia: complex LU/solve conditioning at sigma near lambda_min when the frustration gap is small at low flux — report, never retune.
- R-Ib: DOS 2^20-bin discretization bias on 1/lambda near lambda_min at l=266 — the MC generator gate is the guard; if the gate fails, refine bins once (declared repair), rerun gate, report both.
- R-Ic: sampler-fairness objection — the classical estimator is the SAME importance-sampled path MC that reproduces the sign-free baseline at phi=0 by construction; smarter classical algorithms (dense solvers, fermionization, tensor networks) exist for these structured instances and are named in the honesty statement. The measured breakdown is of the generic sampler only.
- R-Id: fermionization mapping error — caught by the l=10 gate; voids T2, does not touch T1.

## Honesty statement (frozen wording)

Every instance here is classically structured by necessity (dense diagonalization at n=1024; free-fermion solvability at implicit scale): that is what makes truth checkable, and it is why EXP I validates (a) protocol accuracy and cost invariance under signs and (b) the measured death of the generic Prop-C3 sampler — never classical hardness of these instances, and never an unconditional exponential speedup. What EXP I is designed to establish: the quadratic-ceiling argument for sign-free graphs does not extend to signed operators, because the baseline it rests on is gone; what replaces it is the conditional, worst-case DQC1/BQP anchor, unchanged.

## Cost-ledger lines

Quantum: identical D_sigma formula at every flux (the block-encoding of a signed/phased LCU costs the same per step); report Sum D and LWP sets. Classical sampler: measured shot multipliers vs (phi, t). Classical exact: n^3 dense at T1 (seconds, reported); fermionic O(l^3) at T2 (reported).
