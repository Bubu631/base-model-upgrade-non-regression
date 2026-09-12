# Certifying Model Upgrades with Slice-Wise Non-Regression and Incumbent Fallback

**Shengwei Zhang** — University of Pennsylvania  
**Tao Wu, Fei Qian** — Alibaba International Digital Commerce

[Paper (PDF)](papers/base_upgrade/main.pdf) · [LaTeX source](papers/base_upgrade/main.tex) · [Results](papers/base_upgrade/results/) · [Run profiles](configs/) · [Citation](CITATION.cff)

An updated model can improve an aggregate score while degrading an important slice. This project separates candidate development from independent, paired non-inferiority certification and retains the **exact incumbent** when the evidence cannot certify an update. It applies established intersection–union testing and Learn-then-Test principles to an auditable release procedure; it does not claim a new general testing principle or merging operator.

This is a complete, independent repository. Its code, tests, manuscript, tables, figures, checkpoint arrays, protocols, and historical manifests are included. It needs no sibling project or pretrained-model download.

## What the evidence shows

| Study | Executed scope | Finding and limitation |
|---|---|---|
| Bounded-score simulations | Paired gates, slice counts, sample sizes, correlated slices, adaptive candidate selection, and scalar versus two-block search | Failing to detect harm is different from certifying non-inferiority. In one 32-slice setting, the former releases a harmful candidate in 99.7% of trials versus 2.6% for the exact non-inferiority gate at a 5% target. [Recorded manifest](papers/base_upgrade/results/manifest.json). |
| Public digits: selective continuation | Five fixed seeds; 1,797 examples; a NumPy 64–48–10 classifier; 121 candidates for each search family | Every selected proposal fails certification and returns the incumbent. Small per-class certification samples limit power. [Protocol](docs/digits_protocol.md), [manifest](papers/base_upgrade/results/digits_manifest.json). |
| Subsequent balanced continuation | The same five seeds and holdouts, with continuation on all training classes | Mean reporting accuracy of the continued checkpoint rises from 94.78% to 95.94%, but every release still falls back. This later path is descriptive, reuses holdouts, and has more minibatch updates. [Protocol](docs/digits_balanced_protocol.md), [all seeds](papers/base_upgrade/results/digits_path_all_seeds.csv), [comparison](papers/base_upgrade/results/digits_path_comparison.csv). |

A joint release decision for one frozen candidate needs no Bonferroni penalty over slices, but its power can still decrease as the number of slices increases. The guarantees require the stated sampling, development/certification separation, tolerances, and candidate-testing rule. The public experiment is scikit-learn digits—not MNIST, multilingual translation, or a foundation-model benchmark. Seed variability is descriptive rather than an independent deployment confidence interval.

## Install and verify

Use Python 3.13 for the recorded dependency set. The core requirements include NumPy, SciPy, matplotlib, scikit-learn, and pypdf; no Torch or model weights are required.

```bash
git clone https://github.com/Bubu631/base-model-upgrade-non-regression.git
cd base-model-upgrade-non-regression
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-core.txt
make verify
```

`make verify` checks preserved scientific file hashes, runs the unit tests, and independently recalculates both digits paths from the saved checkpoints and bundled scikit-learn dataset. The checkpoint validation runs in a temporary copy and leaves the delivered result files unchanged. It performs no training or network download.

Equivalent commands:

```bash
python experiments/verify_artifact_integrity.py
python -m unittest discover -s tests -v
python experiments/verify_digits_saved.py
```

The original shared execution environment is retained in [requirements-recorded.txt](requirements-recorded.txt) for provenance; install the smaller `requirements-core.txt` for this project. Package versions, seeds, and dataset hashes in each original manifest remain the record of the actual run.

## Configuration profiles and reproduction

[configs/](configs/) contains usable command profiles, interpreted by the standard-library runner [scripts/run_profile.py](scripts/run_profile.py). They were added for this standalone repository; the historical experiments did **not** use these new JSON files. Each command is an argument array executed without a shell, from the repository root, with `{python}` replaced by the active Python executable.

```bash
python scripts/run_profile.py --config configs/verify.json --dry-run
python scripts/run_profile.py --config configs/verify.json
python scripts/run_profile.py --config configs/core.json --dry-run
```

The synthetic profile exposes the script's existing `--calibration-trials`, `--search-trials`, and `--seed` arguments. The digits profiles use the existing `--output` argument when targeting scratch directories; their recorded training settings remain in `digits_upgrade.py` and the archived manifest. Profiles do not introduce unsupported algorithmic tuning knobs.

```bash
# Reproduce the recorded synthetic trial sizes; writes existing result paths.
make reproduce-core

# Retrain selective first, then balanced; writes existing digits result paths.
make reproduce-digits

# Alternatively, write a fixed selective run to runs/digits_selective.
python scripts/run_profile.py --config configs/digits_selective_scratch.json

# Balanced scratch run checks incumbents against the included selective checkpoints.
python scripts/run_profile.py --config configs/digits_balanced_scratch.json
```

Use a separate clone for full reproduction if you want to preserve the delivered records. `digits_balanced.py` verifies its retrained incumbent and split indices against the selective path's saved checkpoints. The `digits.json` profile runs the two paths and reports in that required order. See the [profile guide](configs/README.md) for the complete command mapping.

## Paper, formats, and release assets

The manuscript builds directly from its saved tables and figures; no experiments need to rerun. Install a TeX distribution providing `latexmk`, `pdflatex`, and BibTeX, then:

```bash
make paper
```

The PDF remains at [papers/base_upgrade/main.pdf](papers/base_upgrade/main.pdf). The [ICLR 2027 formatting files](submission/iclr2027/) retain their official source record; they are optional formatting references, not an assertion of submission or compliance with a venue's current requirements. [ArXiv metadata](submission/base_upgrade_arxiv_metadata.txt) is a prepared submission aid, not an arXiv identifier.

The v1.0.0 release uses these standard assets:

- [paper.pdf](https://github.com/Bubu631/base-model-upgrade-non-regression/releases/download/v1.0.0/paper.pdf)
- [paper_source.zip](https://github.com/Bubu631/base-model-upgrade-non-regression/releases/download/v1.0.0/paper_source.zip): standalone LaTeX source with bibliography output, figure PDFs, and tables.
- [repository_bundle.zip](https://github.com/Bubu631/base-model-upgrade-non-regression/releases/download/v1.0.0/repository_bundle.zip): complete standalone project, including results and checkpoints.
- [SHA256SUMS.txt](https://github.com/Bubu631/base-model-upgrade-non-regression/releases/download/v1.0.0/SHA256SUMS.txt)

`make release` creates these files under `dist/v1.0.0/`; it does not commit, upload, or publish. The packager validates the preserved evidence first and has no dependency on another paper.

## Repository map and provenance

- [experiments/](experiments/): five unchanged scientific scripts plus standalone validation and packaging utilities.
- [tests/](tests/): paired-testing, search, gradient, split, and fallback checks.
- [papers/base_upgrade/](papers/base_upgrade/): manuscript, bibliography, figures, all saved experiment results, and ten small classifier checkpoint archives.
- [docs/](docs/): original experiment protocols and the standalone preparation audit.
- [provenance/split_mapping.json](provenance/split_mapping.json): original-to-standalone file mapping and hashes.
- [provenance/original_collection/](provenance/original_collection/): historical collection-level metadata and utilities, retained as records and excluded from the current command flow.

The `papers/base_upgrade` path is retained to preserve the original scripts and manifest paths. There is no runtime dependency on the earlier collection. `.gitattributes` disables line-ending conversion so recorded CSV, JSON, LaTeX, and source hashes survive checkout unchanged. Original timestamps, scientific results, author order, and affiliations are preserved.

## Citation and research status

Use [CITATION.cff](CITATION.cff) or [citations.bib](citations.bib). The manuscript bibliography is separately available as [references.bib](papers/base_upgrade/references.bib). No DOI, arXiv identifier, conference acceptance, production deployment benefit, or new blanket license is inferred from these artifacts. The paper includes its AI-assistance disclosure and detailed evidence limitations; third-party datasets and formatting files retain their applicable terms.
