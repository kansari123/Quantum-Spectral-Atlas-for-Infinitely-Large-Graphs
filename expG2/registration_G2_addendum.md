# EXP G2 addendum pre-registration — hypercube as second LWP testbed

STATUS: FROZEN 2026-07-21 18:3x, before any addendum number has been computed. Authorized by Kamran this session ("do the next experiment needed like G2 or any others"); registered separately because registration_G2.md's frozen scope excluded new testbeds. The main G2 predictions (P-G2R1/R2/R3) are scored strictly against their own frozen text; this addendum adds bars, changes nothing.

Rule under test: identical LWP rule as registration_G2.md (band-restricted own-model contribution, C_REL=1e-3, w(lambda)=1/(lambda+s_t), s_t=0), applied to the EXP H hypercube configurations via the P-H1-validated character-domain synthesis (fidelity 3e-12; zero new shots).

## Frozen addendum predictions

- **A1 (repairs the EXP H P-H2 failure):** at l=14 (r=3, eb=1e-3, ladder {1e-3..1e2}, grid 400 log pts on [1e-4, 1.2*22.006]), LWP retains sigma=1e-3 for ALL three weak-support ports (mid, anti, canary), and each port's s->0 R_eff error under LWP-alive evaluation is within 2x its full-ladder error. KILL: any port ratio > 10.
- **A2 (savings preserved where structure is absent):** the bulk-pure port d1 prunes >= 2 of 6 rungs including sigma=1e-3, with error ratio <= 2.
- **A3 (repair must not undo the concentration dividend):** at l=266 (7-rung ladder {1e-3..1e3}, 4 ports + DOS probe), LWP alive is a subset of {1e2, 1e3} on every column, leaving EXP H's pruned depth (Sum D = 13) unchanged. KILL: LWP retains any rung sigma <= 10 at l=266.

## Declared risks

Inherited R-G2b (band-edge leakage) and R-G2c (w=1/lambda scope only). Addendum-specific: the l=14 truth is the analytic level-sum formula (validated against numeric CG truth at 3.1e-6 in EXP H); a truth-generator discrepancy would void A1/A2, not fail them.
