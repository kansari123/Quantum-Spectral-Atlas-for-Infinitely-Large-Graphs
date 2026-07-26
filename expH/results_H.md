# EXP H results — the engine at n = 2^1000: implicit graphs, where cost follows the description

Date: 2026-07-21 · Frozen registration: `registration_H.md` · Claim under test: "quantum cost grows with the description, not the node count." Instance family: two-scale weighted hypercube Q_ℓ (Cayley graph of Z₂^ℓ; ℓ−r bulk dimensions at weight 1, r weak at 1e-3; λ₂ = 2e-3 at every ℓ). Scales: ℓ = 10, 14 (checkable), 266 (n ≈ 1.2×10^80 — more nodes than atoms in the observable universe), 1000 (n ≈ 1.1×10^301), 2000 (n ≈ 10^602, exploratory).

## 1. Prediction ledger

| ID | Quantity | Frozen bar | Measured | Verdict |
|---|---|---|---|---|
| P-H1 | Synthesizer faithfulness: character moments vs real-matrix moments, ℓ=10/14 | ≤1e-10 (kill 1e-6) | 1.9e-13 / 3.1e-12 | **PASS** |
| P-H2 | ℓ=14 in-band R(s), truth-blind, median | ≤0.5% | 0.00024% | **PASS** |
| P-H2 | ℓ=14 s→0 R_eff, registered "non-canary" set | med ≤2% | **median 109%** (d1: 0.0009%; mid: 109%; anti: 156%) | **FAIL — M-F** (see §2) |
| P-H3 | ℓ=266 & 1000 noiseless: R_eff (all non-canary), tr(L⁺)/n, ln τ/n | ≤2% / ≤2% / ≤0.02 nats | ≤1e-5% / ≤1.2e-7% / ≤5.9e-10 nats | **PASS** |
| P-H3 | same, noisy ε=3e-4 medians | ≤5% / ≤10% / ≤0.15 | 0.07–0.35% / 0.12–0.19% / ≤2e-4 | **PASS** |
| P-H4 | Concentration detection: g prunes all σ≤10 at ℓ≥266; alive ⊆ {1e2,1e3}; no accuracy loss | — | alive = {1e2,1e3} every port & probe, both ℓ; answers unchanged | **PASS** |
| P-H5 | n-independence between ℓ=266 and ℓ=1000 (×2^734 nodes) | Δerr ≤1 pt; ΣD formula exact | Δ ≈ 0 on every target; formula exact | **PASS** |
| P-H6 | Naive/pruned depth ratio at ℓ=1000 | ≥50× | **344×** (325× at 266) | **PASS** |
| P-H7 | Canary arc: (0,r) port fails pruned at ℓ=14 (ratio >10) AND heals at ℓ≥266 | — | ratio **1263×** at ℓ=14 (full ladder: 0.12%); 0.0000% + 0.15% noisy at ℓ≥266 | **PASS**, corroborated beyond registration (§2) |
| X-H1 | ℓ=2000 spot: alive set exactly {1e3}; P-H3 bars | exploratory | alive = {1e3} exactly; 3.1e-5% / 1.9e-6 nats | PASS |

7 registered pass, 1 registered fail with confirmed mechanism and an owned registration-design error, exploratory pass.

## 2. The one failure, and why it is the most informative number in the ledger

P-H2's s→0 clause failed because the registration misclassified the ports. I pre-computed leverage mass only for the (0,r) pure-weak "canary" and labeled (mid) and (anti) as safe — but any port with d_w > 0 has odd-weak-overlap levels at λ = 2ε_b·b, and at ℓ=14 those carry mass ~3.7e-4–1e-3 (below G_CUT = 5e-3) while contributing ~60% of R_eff. The g-flag pruned σ=1e-3 for every port; mid/anti/canary all collapsed to 109–156% error, while the full ladder gets 0.12% — the SBM's M-F mechanism, quantitatively reproduced on a third graph family. The registered "non-canary median" therefore fails at 109%. Owned as a design error in port classification; the mechanism itself was pre-named and the truly bulk-pure port (d1) passes at 0.0009%.

The arc this creates is the experiment's main scientific finding: **the identical ports that fail by ×1263 at ℓ=14 are exact (≤1e-5%, 0.07–0.35% under noise) at ℓ=266 and ℓ=1000.** Measure concentration is the mechanism — weak-sector level mass scales like 2^{−(ℓ−r)} × poly, so the low-mass/high-leverage pathology that defines M-F is a *finite-size and community-structure phenomenon*, and it vanishes identically at product-structure implicit scale. The M-F blind spot lives exactly where graphs are small or community-modular (SBM, small hypercubes); it cannot occur where concentration governs. Suggested (not frozen — G2 is already locked): add the ℓ=14 hypercube as a second LWP testbed in the G2 run, since the repair must rescue mid/anti/canary there.

## 3. What the implicit-scale numbers established

- **Accuracy is n-blind.** Identical frozen config, identical bars, from n = 1.6×10⁴ to n = 10^602: every implicit-scale target within 3.5e-5% noiseless. Pipeline error is a function of spectral geometry (decades, K, rung placement), with node count appearing nowhere — P-H5 measured, not assumed.
- **The two-flag protocol is the enabler, not a liability, at implicit scale.** The naive ladder must budget for λ₂ = 2e-3 (D(1e-3) = 5,640 at ℓ=1000); the g-flag correctly detects that concentration empties every decade except the bulk band and collapses ΣD by 344× (1460× at ℓ=2000) with zero accuracy cost. The same flag that is the villain of EXP G's P-G6 is the hero here — pruning is right precisely when concentration holds and wrong precisely when community leverage does. One diagnostic, two regimes, both now measured.
- **Global invariants come essentially for free.** A Hutchinson probe's level measure at ℓ=1000 equals the density of states to O(2^{−500}): probe variance is annihilated by concentration, single-probe suffices, and ln τ/n = 6.9012394697 nats/node of a 10^301-node graph is recovered to 5.9e-10 nats (tr(L⁺)/n to 1.2e-7%). Under ε=3e-4 noise: 4.3e-5 nats. The spanning-tree count being estimated is a number with ~10^303 digits.

## 4. Honesty statements (frozen wording upheld)

The implicit-scale "measurement record" is classically synthesized from the same character structure that yields analytic truth; the fitter is truth-blind (K noisy moments + nb² only), and P-H1 pins the synthesizer to real matrix dynamics at checkable sizes to 3e-12. This family is classically easy BY CONSTRUCTION — that is what makes truth checkable, and it is why this experiment validates the *cost-scaling and accuracy claims of the protocol*, not classical hardness of the instance. The verifiability trilemma stands: any instance you can check is not the hard instance. The advantage claim rides on the cost model — one walk step = O(ℓ) gates (LCU over ℓ weighted involutions) versus one classical matvec = ℓ·2^ℓ flops — reported as a model:

| ℓ | n | classical flops per single matvec | pruned quantum depth ΣD (walk steps) |
|---|---|---|---|
| 266 | 1.2e80 | 3.2e82 | 13 |
| 1000 | 1.1e301 | 1.1e304 | 24 |
| 2000 | 1.1e602 | 2.3e605 | 8 |

Classical structure-exploiting cost for THIS family: O(ℓ²) big-integer work (seconds) — stated so no reader mistakes the family for hard.

**Post-hoc amendment (2026-07-21, discussion only; no frozen number touched): the explicit-matvec column above is NOT the fair generic classical competitor at implicit scale.** For any sign-free (nonnegative-weight) Laplacian given as a rule, a classical lazy random walker also pays only poly(l) per step: return probabilities <u|P^t|u> are estimable by direct sampling, they are exactly monomial moments of the same local spectral measure, and they can feed the identical NNLS post-processing. The generic classical-vs-quantum gap on sign-free implicit graphs is therefore POLYNOMIAL, not exponential: resolvent-grade resolution at scale sigma costs classical walk length ~alpha/sigma versus quantum depth ~sqrt(alpha/sigma) (the polynomial-method square root), compounded with the usual 1/eps^2 vs 1/eps amplitude-estimation factor. Exponential-advantage territory requires leaving stochasticity (magnetic/signed/complex-weighted operators, generic sparse Hamiltonians, where the sign problem blocks MCMC and the DQC1/BQP hardness anchors actually apply) or changing task type (welded-trees traversal has a proven oracle-model separation; spectral-functional estimation does not). The table stands as a statement about explicit linear algebra; it must not be read as a classical lower bound. The candidate hard instances are the same access model without closed-form structure: Cayley graphs of nonabelian groups, configuration/state-space graphs — where the classical column collapses to "infeasible" and the quantum column is unchanged, provided λ₂ is not exponentially small and targets are normalized-additive (the DQC1-class regime).

## 5. Bugs and environment findings owned this session

1. **nb² normalization interface bug (real, caught by design).** I fed raw moments (μ₀ = nb²) to `nnls_rung`/`flags`, which expect the normalized convention (μ₀ ≡ 1) of `moments_block`. Result: all port answers ×2, all probe answers ×1 — the nb²=1 DOS column being clean while nb²=2 ports failed at exactly 100% error was the differential diagnostic; P-H1 (moments faithful) and the two-generator truth gates (3.1e-6 agreement) had already fenced the bug into the fit interface. Fixed; flags re-derived (alive sets changed); all reported numbers post-fix. **EXP G is unaffected** (it consumed `moments_block` output directly).
2. **Hypercube splu fill.** First arm A attempt used sparse LU on Q_14 — hypercubes have near-worst-case separators; foreground timeout. Same mechanism class I'd already hit this session; should have anticipated. Replaced with matrix-free XOR matvec + CG (16 s total).
3. **Environment correction to the results_G amendments log.** Background processes are reaped at bash-call boundaries in this sandbox. The earlier "silent OOM" attribution for the dense-eig reference jobs was wrong — they were reaped. The reference-generator amendment itself remains valid and cross-validated (2.0e-9); only the death-mechanism claim is corrected here. Matrix-tree gate bug (double-subtracted ln n in a comparison line, signature exactly ℓ·ln2/2^ℓ) found and fixed before scoring; float overflow of 2^ℓ at ℓ=2000 replaced with clean-underflow exp form.

## 6. What did we find, brutally simply

We ran the same measurement plan on a graph with more nodes than there are atoms in the universe — then one with 10^301 nodes, then 10^602 — and it did not care. Same accuracy, same tiny circuit depths, because the cost depends on the graph's *description* (a thousand numbers) and its spectral shape, never on its node count. On these giants, the machine counted spanning trees — numbers with hundreds of digits of digits — to nine decimal places in the log, and the emptiness detector that failed us on community graphs became the whole reason the run is cheap: at astronomical size, randomness concentrates, almost every energy decade really is empty, and detecting that cuts the circuit bill by 300–1500×. The one failure was ours, not the machine's: at small sizes, the community-mode blind spot from last experiment bit again on ports we had mislabeled as safe — and then provably vanished at large size, which tells us exactly where the blind spot lives and where it can't. The honest boundary of the whole claim is unchanged: this family is easy to check *because* it's structured; the speedup money is on rule-defined graphs with no such structure, where a classical computer can't take a single step and — as now measured — this protocol's costs wouldn't change.

## 7. Repro map

`registration_H.md` (frozen) · `hypercube.py` (exact big-int level measures, synthesis, analytic truths) · `armA_v2.py` (ℓ=10/14: matrix-free CG moments, CG/slogdet truths, P-H1/H2/H7, noise) · `armB.py` (ℓ=266/1000/2000: synthesis, flags, joint fit, noise, depth ledger) · results: `res_armA.json`, `res_armB.json` · figure: `figs/fig5_implicit_arc.png`. Seeds: noise 434343. Ports: (d_b,d_w) ∈ {(1,0),(⌊(ℓ−r)/2⌋,⌊r/2⌋),(ℓ−r,r),(0,r)} + DOS probe.


---
## Post-hoc amendments (2026-07-21, later session; labeled per protocol — no frozen number above is altered)

1. **G2 addendum approved and executed.** The suggested l=14 hypercube LWP testbed was authorized by Kamran, frozen as `../expG2/registration_G2_addendum.md` BEFORE any addendum number existed, and run: the P-H2 s->0 failure is repaired — mid/anti/canary ports 109–156% -> 0.059–0.123% (ratio 1.0 vs full ladder), and the l=266 concentration dividend is preserved and slightly improved (SumD 13 -> 10, LWP also drops sigma=1e3 as irrelevant to 1/lambda). One addendum clause (A2) failed as an unfloored-ratio-at-machine-floor artifact (9.7e8 with absolute errors 9e-13% vs 8.7e-4%); see `../expG2/results_G2.md` §3–4.
