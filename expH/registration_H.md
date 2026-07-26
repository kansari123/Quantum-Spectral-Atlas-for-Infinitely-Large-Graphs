# EXP H pre-registration — the claim under test: "quantum cost grows with the description, not the node count"

STATUS: FROZEN 2026-07-21, before any EXP H number has been computed. Inherited unchanged: K=24, NNLS positive quadrature (row-0 ×100), two-flag protocol (G_CUT=5e-3; f<0.51 → ε/10), Gaussian ε-per-moment noise model, D_d=⌈4√(α/σ_d)⌉, joint fit is the REGISTERED PRIMARY for global functionals (per EXP G promotion; stitched reported as diagnostic only). LWP (registration_G2) is OUT OF SCOPE here and is not run.

## Instance family (succinctly specified graphs)

Two-scale weighted Boolean hypercube Q_ℓ = Cayley graph of Z₂^ℓ: dimensions 1..ℓ−r have edge weight 1 ("bulk"), the last r=3 (ℓ=14) or r=6 (ℓ≥266) have weight ε_b=1e-3 ("weak"). n = 2^ℓ nodes, described by ℓ+1 numbers. Spectrum: λ_S = 2|S∩bulk| + 2ε_b|S∩weak|, S ⊆ [ℓ]; a node-pair port differing on (d_b, d_w) dimensions has spectral mass only on odd-overlap characters — (ℓ−r+1)(r+1) distinct levels total, with exact big-integer level masses. λ₂ = 2ε_b at every ℓ.

Scales: ℓ=10, 14 (classically checkable), ℓ=266 (n ≈ 1.2e80 — more nodes than atoms in the observable universe), ℓ=1000 (n ≈ 1.07e301), exploratory ℓ=2000.

## Data-generation honesty statement (frozen wording)

At implicit scale, the "quantum measurement record" (per-rung Chebyshev moments) is synthesized classically from the character-domain level measure — the same structure that yields analytic truth. This is the standard and only possible validation design: any instance with checkable truth is by definition classically structured. What is therefore being tested is NOT classical hardness of this family (it is easy by construction) but: (1) faithfulness of the synthesizer to real matrix dynamics at checkable sizes; (2) invariance of pipeline accuracy in n at fixed spectral parameters; (3) the measured cost ledger's dependence on (α, σ, flags) only. The fitting pipeline is truth-blind: it receives K noisy moments per rung and nb², nothing else. The advantage claim rides on the cost model (one walk step = O(ℓ) gates via LCU of ℓ local terms vs one classical matvec = ℓ·2^ℓ flops), stated as a model, not a benchmark.

## Ports (frozen)

Per ℓ: (d_b,d_w) ∈ {(1,0), (⌊(ℓ−r)/2⌋,⌊r/2⌋), (ℓ−r, r) antipodal, (0, r) pure-weak "canary"} + one DOS probe (density-of-states measure = exact ℓ→∞ Hutchinson limit; finite-probe fluctuation O(2^{−ℓ/2}) noted analytically).

Ladders: ℓ=14: σ∈{1e-3,1e-2,1e-1,1,10,100}, grid 400 log pts [1e-4, 1.2α]. ℓ≥266: σ∈{1e-3..1e3} (7 rungs), grid 400 log pts [1e-4, 1.2α]. R(s): ℓ=14, 25 log s in [1e-3, α]; ℓ≥266, 5 log s in [1, 100] + s→0 endpoint. Noise: ε=3e-4, T=100, seed 434343; noiseless flags fix alive sets and ε/10 rungs.

## Frozen predictions

- **P-H1 (synthesizer faithfulness):** at ℓ=10 and ℓ=14, character-synthesized moments equal matrix-route moments (sparse LU on the real 2^ℓ Laplacian) to ≤1e-10 max abs, all rungs × ports. KILL: >1e-6.
- **P-H2 (checkable-scale accuracy, truth-blind, non-canary ports):** ℓ=14 vs independent solve/logdet truth: in-band R(s) median ≤0.5%; s→0 R_eff median ≤2%, p90 ≤5%; ε=3e-4 trial-median median ≤5%. Same bars as EXP G.
- **P-H3 (implicit-scale accuracy):** ℓ=266 and ℓ=1000 vs analytic truth: noiseless R_eff error ≤2% on every non-canary port; per-node Kirchhoff tr(L⁺)/n ≤2%; ln τ/n ≤0.02 nats/node (joint fit). Noisy ε=3e-4 medians: R_eff ≤5%, tr(L⁺)/n ≤10%, ln τ/n ≤0.15. KILL: any noiseless target >10%.
- **P-H4 (concentration detection):** at ℓ≥266, g prunes every rung σ≤10 for every port and probe (measure concentration renders those decades empty), alive ⊆ {1e2,1e3}; pruned answers still meet P-H3. KILL: pruning-induced degradation >10%.
- **P-H5 (n-independence):** identical frozen config passes P-H3 at both ℓ=266 and ℓ=1000 (2^734 ≈ 10^221 × more nodes); |err(1000) − err(266)| ≤ 1 percentage point on every noiseless target; ΣD matches ⌈4√(α/σ)⌉ exactly with α = 2Σw_i.
- **P-H6 (two-flag protocol as the implicit-scale enabler):** naive full-ladder ΣD (which must cover λ₂=2e-3) vs flag-pruned ΣD ratio ≥ 50× at ℓ=1000.
- **P-H7 (M-F canary arc):** the (0,r) pure-weak port REPRODUCES the EXP G pruning pathology at ℓ=14 — its small-λ mass (~1e-3, below G_CUT) carries ~half its R_eff, g prunes the σ=1e-3 rung, pruned-vs-full error ratio >10 — AND the same port HEALS at ℓ≥266 (weak-sector mass ~2^{−(ℓ−r)}: concentration erases the leverage pathology), meeting P-H3 bars. Prediction: the M-F blind spot is a finite-size/community phenomenon, absent at product-structure implicit scale.
- **X-H1 (exploratory):** ℓ=2000 spot check (n ≈ 1e602), predicted alive set exactly {1e3}, same bars as P-H3 noiseless. Not running or failing bars here kills nothing.

## Named risks

- R-Ha: concentrated band (relative width ~ℓ^{−1/2}) may stress the 400-pt log grid / NNLS conditioning → mechanism if P-H3 fails with mass placed off-band.
- R-Hb: warp saturation at the alive rungs (checked pre-run: y ∈ [−0.82, 0.01] at ℓ=1000 — inside safe range; recorded).
- R-Hc: circularity objection to synthesis — mitigated solely by P-H1 + noise injection + fitter blindness; if P-H1 fails, ALL implicit-scale results are void.
- R-Hd: big-integer → float mass conversion precision at ℓ=1000 (exact Fraction rounding; Σmass gate 1±1e-12 enforced per port).

## Cost-ledger lines to report (measured or formula-exact, no hand-waving)

Per-walk-step gate count O(ℓ) (LCU over ℓ weighted involutions); pruned ΣD and shot multipliers (f-flag) per ℓ; classical exact per-matvec ℓ·2^ℓ flops at each ℓ (10^304 at ℓ=1000); classical structure-exploiting cost O(ℓ²) with the explicit statement that the latter exists BECAUSE the instance is a validation instance.
