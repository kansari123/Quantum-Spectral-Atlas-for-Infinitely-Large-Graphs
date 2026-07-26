# EXP J v0 pre-registration — a signed operator with every known classical route closed

STATUS: FROZEN 2026-07-21, before any EXP J number exists. Companion to the analysis document (Theorem + quantum-competitor map), which is mathematics and citation, not experiment; this registration covers only the empirical claims. Bar hygiene: floored forms throughout; comparison floors at class-bar/10 per the P-I4 lesson.

## Purpose

EXP I killed the generic sampler on instances that remained classically solvable by construction (that is what made truth checkable). EXP J v0 constructs an instance family designed so that every classical route WE know is closed, verifies the engine on it at the largest size where dense truth exists, and then states plainly that its implicit-scale moments cannot be produced by us at all — which is simultaneously the evidence of interest and the reason no accuracy claim can exist there.

## Instance

L_J = sum_{i=0}^{l-1} (I - X_i Z_{i+1 mod l}) + sum_{i in {0,4,8,...} (step 4)} (I - X_i X_{i+2}), unit weights. Sizes: l=12 (n=4096, dense truth) for engine verification and sampler measurement; l=266 named as the deployment target with NO numbers to be produced.

## Frozen predictions

- J1 (structure): the frustration graph (vertices = Pauli terms, edges = anticommuting pairs) contains an induced claw K_{1,3}, certified by an explicit vertex list printed by the script. A claw obstructs line-graph-ness (necessary condition), closing the Chapman-Flammia line-graph free-fermion route that solved EXP I's T2. KILL: no claw found -> the design fails; reported as the headline.
- J2 (structure): at least one non-commuting term pair exists (closes simultaneous stabilizer diagonalization). Trivial, frozen anyway.
- J3 (engine on the hard-family member at checkable size, l=12, no deflation): band median <= 0.5%; endpoint median <= 2%, p90 <= 5%; lndet <= 0.02 nats noiseless / 0.15 noisy; trinv <= 2% / 10%; noise endpoint median <= 5%. KILL: any noiseless median > 10%.
- J4 (generic sampler death on the same instance): fitted average-sign decay Delta_s > 0 and shot multiplier at t* = ceil(alpha/sigma), sigma = 1e-2, of at least 1e6 relative to the sign-free baseline. KILL: multiplier < 1e2.

## Frozen non-claims (the teeth)

1. The claw closes the line-graph route ONLY. "Free fermions in disguise" (Fendley-type) and undiscovered solvable structures are NOT exhausted by any certificate we can produce; we check what is checkable and name what is not.
2. NP-hardness of curing the sign problem by single-qubit transformations (Marvian-Lidar-Hen 2019; Klassen et al. 2020) is cited as evidence that no generic efficient escape exists as a method; it proves nothing about this specific instance.
3. No average-case or instance hardness is claimed, at any size. Worst-case hardness of the TASK CLASS is a theorem (analysis doc) about the class, not about L_J.
4. l=266 moments are deliberately NOT synthesized: we possess no method, and that absence is the point. Consequently no accuracy statement exists or will be made at implicit scale for L_J; on hardware, only the protocol's internal diagnostics (rung cross-consistency, f/g flags, K-tail decay, noise stability) would be available there, and they verify consistency, not truth.

## Procedure notes

Dense truths at l=12 by eigendecomposition + direct-solve gate <= 1e-9 (as EXP I). alpha = 2 x max weighted row-|sum| bound, frozen as procedure. Ladder {1e-3,1e-2,1e-1,1,10}, grid 400 log pts [1e-4, 1.2 alpha]. Ports/probes seeds 2026/31337; noise 434343; sampler seed 606, N = 2e5 walkers, measure to t = 150, exponential fit on the measurable window (s > 5/sqrt(N)), extrapolate to t*; report the fitted character of the multiplier explicitly.
