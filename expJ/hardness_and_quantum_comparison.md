# Hardness of the task class, and where quantum competitors win and lose

Companion to EXP I/J. Status of every statement is labeled: [PROVEN] mathematics with proof below or citation; [MEASURED] numbers from frozen-registration runs; [FORMULA] arithmetic from measured constants; [CONJECTURAL] stated as such. Date 2026-07-21.

## 1. What "hard for every classical method" can and cannot mean

Unconditional instance hardness would separate BPP from BQP; nobody has that. Three honest layers exist and we now hold all three:
(a) [PROVEN] worst-case hardness of the exact task class the protocol outputs (Theorem 1);
(b) [MEASURED] death of the generic sampler and closure of every known structural route on a concrete instance family (EXP I, EXP J);
(c) [CONJECTURAL] average-case hardness of natural signed families — evidence, never proof, and labeled so everywhere.
The instances we validated remain classically easy by construction; that is the price of checkable truth and is stated in every registration.

## 2. Theorem 1 — the protocol's first output is already worst-case hard

**Task RT.** Given a succinct Hermitian 0 ⪯ L ⪯ αI (poly-size LCU of Pauli strings/unitaries or a block-encoding — exactly our access model), and a shift σ ≤ poly(n)·α, estimate the rung-1 moment μ₁(σ) = (2σ/2ⁿ)·tr((L+σ)⁻¹) − 1 to additive ±1/poly(n).

**Theorem 1.** RT is DQC1-hard. The port variant — estimate ⟨b|2σ(L+σ)⁻¹|b⟩ − 1 for b = |0ⁿ⟩ — is BQP-hard. Hence a polynomial-time classical algorithm for the protocol's probe-arm (resp. port-arm) single-moment output on all succinct signed operators would classically solve every DQC1-complete (resp. BQP-complete) estimation problem — e.g., additive Jones-polynomial evaluation at a fifth root of unity (Shor–Jordan, QIC 8:681, 2008).

**Proof.** Normalized-trace estimation — given a poly-size circuit U on n qubits, estimate Re tr(U)/2ⁿ to ±1/poly — is the canonical DQC1-complete problem (Knill–Laflamme, PRL 81:5672, 1998; Shepherd, quant-ph/0608132; Shor–Jordan 2008). Let H = (U+U†)/2: Hermitian, ‖H‖ ≤ 1, an LCU of two poly-size unitaries, so L := I + H is succinct with 0 ⪯ L ⪯ 2I (α = 2), and tr H/2ⁿ = Re tr U/2ⁿ =: m₁. Write eigenvalues λ = 1 + h, h ∈ [−1,1], m_j := tr(Hʲ)/2ⁿ, |m_j| ≤ 1. For σ ≥ 2, the geometric expansion of σ/(σ+1+h) gives

  G(σ) := (σ/2ⁿ)tr((L+σ)⁻¹) = [σ/(σ+1)]·(1 − m₁/(σ+1) + R),  |R| ≤ Σ_{j≥2}(σ+1)⁻ʲ = 1/[σ(σ+1)].

Rearranging: m₁ = (σ+1)[1 − ((σ+1)/σ)G(σ)] + (σ+1)R with |(σ+1)R| ≤ 1/σ. An estimate of G to ±ε therefore yields m₁ to ±[((σ+1)²/σ)ε + 1/σ]. Given any target δ = 1/poly: set σ = 2/δ and ε = δ²/16. Then 1/σ = δ/2, and since σ ≥ 2 implies (σ+1)²/σ ≤ 9σ/4, the first term is ≤ (9/(2δ))·(δ²/16) = 9δ/32; total error ≤ 25δ/32 < δ. Both σ and 1/ε are poly(n), and μ₁(σ) = 2G(σ) − 1, so additive estimation of μ₁ to ±2ε suffices. The port variant is verbatim with m_j → ⟨0ⁿ|Hʲ|0ⁿ⟩, |·| ≤ 1, recovering Re⟨0ⁿ|U|0ⁿ⟩ to ±1/poly, whose estimation is BQP-complete (Hadamard-test acceptance amplitudes). ∎

**Prior art and placement.** The umbrella phenomenon — DQC1-completeness of normalized traces of *functions* of Hamiltonians, with approximate degree as the governing parameter and block-encoding access, via Chebyshev machinery — is established in arXiv:2604.01519 (2026), which should be cited as the general result; our Theorem 1 is a minimal special case (a single resolvent point), included because (i) it is self-contained and elementary, and (ii) it pins hardness to the *literal first number our acquisition emits*, at exactly the additive-normalized 1/poly precision the protocol targets (ε = 3×10⁻⁴): no precision bait-and-switch. Consequences of a hypothetical classical solver are stated via Shor–Jordan; on classical-simulation collapse results for DQC1-type sampling see Morimae–Fujii–Fitzsimons, PRL 112:130502 (2014) — related but distinct (sampling vs estimation), cited conservatively.

**What Theorem 1 does not say.** Nothing about any instance we ran; nothing average-case; the σ in the reduction is instance-chosen (one free knob of the interface), while our registered ladders freeze σ — the theorem is about the interface class, and every rung output belongs to it.

## 3. No generic escape hatch from signs [PROVEN, cited]

Deciding whether single-qubit transformations (Clifford or orthogonal) can cure a Hamiltonian's sign problem is NP-complete (Marvian–Lidar–Hen, Nat. Commun. 10:1571, 2019); for 2-local Hamiltonians with one-local terms, curing by single-qubit unitaries is NP-hard, with an efficient decision algorithm existing only in the strictly 2-local case (Klassen, Marvian, Piddock, Ioannou, Hen, Terhal, SIAM J. Comput. 49(6):1332, 2020). So "just rotate the basis" is not a method — even *finding* the rotation is intractable in general. Cited as method-level evidence; proves nothing about a specific instance.

## 4. EXP J v0 [MEASURED, frozen registration_J.md] — the all-known-routes-closed instance

L_J = Σᵢ(I − XᵢZᵢ₊₁) + Σ_{i∈4ℤ}(I − XᵢXᵢ₊₂). Ledger, all four clauses PASS as frozen:
- J1: frustration graph contains the induced claw (C1; C0, C2, E0) — certificate printed. Claw-freeness is necessary for line graphs, so the Chapman–Flammia line-graph fermionization that solved EXP I's T2 is closed. Non-claim kept: "free fermions in disguise" (Fendley-type) and unknown structures are not exhausted.
- J2: non-commuting term pairs exist — simultaneous stabilizer diagonalization closed.
- J3: engine on the hard family at checkable size (ℓ=12, n=4096, λ_min = 4.925, no deflation): band and endpoint medians 0.0000%, lndet 2.8×10⁻³ nats, trinv 0.36%, noise 0.18%/0.0028/1.18%, truth gate 7.9×10⁻¹¹ — every J3 bar met with headroom.
- J4: the generic sampler dies fastest yet on this instance: Δ_s = 0.356, average sign measured-dead by t = 12 (N = 2×10⁵), t* = 3000 at σ = 10⁻²; fitted multiplier 10^926 (extrapolated exponential; the direct measurement is the t=12 death).
- The point, stated as registered: at ℓ = 266 we possess NO method to produce this operator's moments — not fermionization (claw), not stabilizer, not the sampler (measured dead), not dense algebra (n ≈ 10⁸⁰), and no basis cure is generically findable (Sec. 3). That absence is simultaneously the strongest evidence available short of proof and the reason no accuracy number can ever be claimed there classically. On hardware, only the protocol's internal diagnostics (rung cross-consistency, f/g flags, K-tail decay, noise stability) would be reportable — consistency, never truth. [CONJECTURAL] that this family is classically hard on average; named as the campaign's standing conjecture, not a result.

## 5. Against quantum competitors: a regime map, not a victory lap

| Competitor | Their cost | Ours | Verdict |
|---|---|---|---|
| Time-evolution/QPE-style spectral estimation at resolution σ | depth ~ α/σ per feature | D_σ = ⌈4√(α/σ)⌉ | [FORMULA+MEASURED] quadratic win in resolution, prefactor 4 — real only for σ ≪ α/16. Measured instances: EXP J ℓ=12 (α=30, σ=10⁻²): 3000 vs 220 = 13.6×; SBM community regime (σ=10⁻⁶): ~1.6×10³×; T2's alive rung (σ=100, α=532): 5.3 vs 10 — we LOSE at shallow rungs. |
| Modern per-query coherent QSVT + amplitude estimation (same √-filters as ours) | per functional: ~K·D·(1/ε) coherent depth | one acquisition ΣD·c/ε² shots, then every rational-span functional free | [FORMULA, measured constants; corrected — see appendix] this is the FT-AE tier: crossover **≈ 2.4×10⁴ queries**; the same-hardware sampling tier breaks even at **Q*_samp = 276|alive|/K = 11.5–34.5**, which the campaign's own workloads (26–364 functionals/acquisition) exceeded 2–30× in every frozen run. |
| Same, single-query precision race (fault-tolerant, unlimited depth) | ε⁻¹ coherent | ε⁻² shots | **We lose ≈ 2.4×10⁴× in total steps at ε = 3×10⁻⁴ (corrected — see appendix).** Stated plainly; no framing rescues it. |
| Any coherent method under a depth budget D_max | needs unbroken depth ~D/ε (ℓ=266: ~3.3×10⁴ walk steps ≈ 8.8×10⁶ gates) | per-shot depth D (= 10 walk steps ≈ 2.7×10³ gates at ℓ=266) | [FORMULA] whenever D_max < D/ε, coherent AE is unavailable and the shots-heavy/short-depth atlas wins by default — the near-term hardware column. |
| Threat, named | coherent multi-observable amortization (gradient/QSVT batching) could erode Q* | — | open; if realized, our amortization column shrinks. Flagged, not hidden. |

The licensed sentence: "The task class is worst-case DQC1/BQP-hard [Theorem 1, and generally arXiv:2604.01519]; on it, the atlas beats time-evolution-style quantum spectral estimation quadratically in resolution where resolution is deep, beats same-hardware per-query pipelines beyond 12–35 queries per operator (its own workloads ran 26–364) and by a 5.5×10³ per-circuit coherence margin whenever depth is budget-limited, and loses ≈2.4×10⁴× to amplitude estimation in the single-query fault-tolerant limit (corrected — see appendix)." Anything stronger is unsupported.

## 6. What would settle more

Proof targets: average-case hardness for random signed Pauli families (out of reach; anticoncentration-style routes per the DQC1-sampling literature); tightening Theorem 1 to the frozen-ladder σ set (remove the free knob). Deployment: run L_J at ℓ ≥ 100 on hardware under the diagnostics-only protocol of Sec. 4 — the first campaign instance where the quantum device would be producing numbers nobody can check, which is precisely the regime the whole apparatus of flags, gates, and pre-registration was built for.


---
## Correction (2026-07-21, later in session; labeled per protocol)
The regime-map constants above conflated two competitor classes. Corrected model (three competitors, l=266 measured constants, eps=3e-4): atlas T=3.07e10 walk steps once (shots <=230 deep); per-query SAMPLING QSVT 2.67e9/query (same hardware class) -> Q*_samp = 276|alive|/K = 11.5-34.5 measured (~12-100 with degree/flag effects); per-query QSVT+AE 1.26e6/query coherent (1.26e6-deep unbroken circuits, FT only) -> single-query loss and atlas crossover both 2.4e4 (NOT 71); per-circuit coherence ratio 5.5e3. Campaign's own workloads issued Q=26-364 functionals per acquisition — past the sampling break-even by 2-30x in every frozen run. The "Q*~71" and "lose ~71x" figures earlier in this document and in paper v0.5/v1.0 are superseded; frozen experimental numbers are untouched. Full development: paper v1.1 Sec. "The advantage over quantum competitors" (fig_qcomp).
