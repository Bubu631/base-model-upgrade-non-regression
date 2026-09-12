# Runnable command profiles

These JSON files are a new convenience layer for the standalone repository. Original experiments used the unchanged scripts and recorded protocols/manifests; these files are not retrospectively described as their configuration mechanism.

```bash
python scripts/run_profile.py --config configs/verify.json --dry-run
python scripts/run_profile.py --config configs/verify.json
```

| Profile | Existing command(s) | Writes |
|---|---|---|
| `verify.json` | Integrity check, unit tests, isolated checkpoint/gate audit | Temporary validation copy only |
| `core.json` | `base_upgrade.py --calibration-trials 20000 --search-trials 4000 --seed 20260911` | Synthetic result and figure paths |
| `digits.json` | Selective training → figure → balanced training → comparison | Recorded digits output paths |
| `digits_selective_scratch.json` | `digits_upgrade.py --output runs/digits_selective` | Scratch directory |
| `digits_balanced_scratch.json` | `digits_balanced.py --output runs/digits_balanced` | Scratch directory; reads included selective checkpoints |
| `paper.json` | `latexmk -cd ... papers/base_upgrade/main.tex` | Paper PDF and TeX build files |
| `release.json` | Standalone local packager | `dist/v1.0.0` |

Each profile has `schema_version: 1`, a readable name/description, a historical-status note, and `commands`, an array of nonempty string-argument arrays. `{python}` and `{root}` are the only supported placeholders and must each occupy a complete argument. The runner uses `subprocess.run(argv, check=True)` with the repository root as its working directory. It stops after any failed command; it never evaluates shell syntax.

Only existing CLI arguments are represented. The synthetic script supports three options shown above. The digits scripts expose output location, while their seeds, architecture, optimizer, slice tolerance, and search grids remain the fixed scientific choices in `experiments/digits_upgrade.py` and the archived manifests. Editing a profile does not add new optimizer controls. Reproduction runs can overwrite recorded outputs; use scratch profiles or a separate clone as indicated.
