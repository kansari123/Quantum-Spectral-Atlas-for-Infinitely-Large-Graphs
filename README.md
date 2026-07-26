# Quantum Spectral Atlases for Exponentially Large Graphs

**Quadratic Speedup, Query Amortization, and Shallow Circuits**

Kamran Ansari · Stanford University · ansarik@stanford.edu

This repository is the public mirror of the ancillary materials (`anc/`) accompanying the arXiv submission: all experiment code, exact instance generators with seeds, per-run result files, protocols with accuracy criteria fixed prior to data collection, figures, and the IBM hardware acquisition and analysis notebook.

**Paper:** arXiv link pending — this line will be updated when the preprint is live.
**Landing page:** https://kansari123.github.io/Quantum-Spectral-Atlas-for-Infinitely-Large-Graphs/

## Layout

| Path | Contents |
|---|---|
| `expG/` | Explicit-graph experiments: the LastFM social network (7,624 nodes) and a designed stochastic block model. Code and archived datasets in `expG_code_checkpoints.tar.gz`; per-run results, protocol files, figures. |
| `expG2/` | Leverage-weighted port-selection follow-up on the same instances. |
| `expH/` | Implicitly specified product graphs with up to 2^2000 vertices. |
| `expI/` | Signed and magnetic operators (flux-threaded tori; a signed operator on ≈10^80 vertices), with path-sampler baselines. |
| `expJ/` | Hardness construction and quantum-comparison worked constants and cost tables. |
| `qpvl_ibm_hardware_validation.ipynb` | IBM hardware acquisition and analysis notebook (two-processor characterization on IBM Heron devices). |
| `qpvl_run2_reanalysis_cell.py` | Self-contained zero-QPU reanalysis of the cached hardware run. |
| `figs/` | The seven figures as they appear in the paper. |
| `docs/` | Source of the landing page. |
| `README.txt` | The original ancillary README shipped with the arXiv package. |

File conventions inside each experiment directory: `registration_*.md` — protocol and quantitative accuracy criteria, fixed prior to data collection; `results_*.md` — outcome ledgers; `res_*.json` — machine-readable results.

Ground truth is dual-generator with cross-checks at or below 1e-9 throughout; seeds are listed in the paper's Data and code availability section.

## Reproducing

Requires Python 3 with `numpy` and `scipy`. The archived datasets (`.npz`) ship inside `expG/expG_code_checkpoints.tar.gz`, so no external downloads are needed. Scripts expect their inputs in the working directory; the pattern below is verified end-to-end:

```bash
mkdir work && cd work
tar -xzf ../expG/expG_code_checkpoints.tar.gz   # code + archived datasets
cp ../expG2/g2_main.py ../expG/res_sbm.json .
python3 g2_main.py                               # ~3 s; prints MAIN G2 DONE on success
```

The other experiment scripts follow the same working-directory pattern. The hardware notebook's acquisition cells require IBM Quantum access; the reanalysis script reproduces the run-2 analysis from cached results without QPU access.

## Citation

Until the arXiv identifier is live:

```bibtex
@misc{ansari2026spectralatlases,
  title  = {Quantum Spectral Atlases for Exponentially Large Graphs:
            Quadratic Speedup, Query Amortization, and Shallow Circuits},
  author = {Ansari, Kamran},
  year   = {2026},
  note   = {arXiv preprint; identifier to be added}
}
```
