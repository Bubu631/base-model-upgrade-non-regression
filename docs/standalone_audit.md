# Standalone repository preparation and validation

This repository was split from the earlier `research_release` collection. The standalone path `papers/base_upgrade` was deliberately retained, so the five scientific scripts, manuscript, figures, tables, checkpoint arrays, experiment protocols, and result manifests remain byte-for-byte unchanged. The unrelated edit-localization paper and experimental code are absent. The current Makefile, validators, profiles, and packager operate only on this project.

The mapping and SHA-256 values for 82 copied files are in `provenance/split_mapping.json`. A paper-specific reader guide was adapted; its original bytes are retained under `provenance/original_collection/base_upgrade_README.original.txt`. Earlier collection-level utilities and guides use archival text filenames and are not runnable dependencies. The original author-confirmation record is preserved, while the current `paper_authorship.json` lists only Shengwei Zhang, Tao Wu, and Fei Qian, in that order, with their confirmed affiliations.

New convenience files are the English root/paper guides, `CITATION.cff`, `citations.bib`, `.gitignore`, `.gitattributes`, standalone Makefile, seven JSON command profiles, the standard-library profile runner, a project-specific integrity checker, a temporary-copy digits validator, and a local release packager. These additions did not configure the historical experiments. Trial count, seed, and output-location arguments map only to flags that already exist in the scientific scripts; no new algorithmic tuning controls were invented.

Validation performed:

- 121 integrity assertions passed over 82 distinct copied artifacts, including all relevant historical manifest checks. Original experimental bytes remain intact.
- All nine original unit tests passed: paired testing, candidate correction, fixed-sequence stopping, scalar/block identity, bounded scores, disjoint partitions, gate direction, finite-difference gradients, and exact incumbent identity.
- Both completed digits paths were independently recalculated from saved checkpoints in an isolated temporary copy. All ten seed/path runs passed; regenerated comparison tables were byte-identical, and delivered records were unchanged.
- All seven profiles passed `--dry-run`. Both scratch digits profiles were also executed: every generated CSV matched the recorded CSV byte-for-byte and every NPZ array matched the corresponding original checkpoint artifact. Those replay outputs are under ignored `runs/`; they are validation of the new launch interface, not replacement historical results or new independent evidence.
- Active README links resolve locally, and all current Python files parse. No active experiment/test/runner depends on an edit-localization path.
- The `paper_source.zip` was extracted into an empty directory and compiled successfully with `latexmk`; it produced 21 pages, no LaTeX warnings, and text exactly identical to the delivered PDF. The delivered PDF itself was not replaced.
- A credential-pattern scan found no matching keys or tokens. Private interview materials, raw user attachments, downloaded model/corpus caches, and the other paper's code are absent.

Machine-readable records are under `checks/`. The preserved PDF SHA-256 is `4abb50f8b167b5ebb887a1fecdc6f880a557af46c10e021e2b1db538e6349bf1`. Exact floating-point replay was checked in the available recorded-compatible local environment; cross-platform execution is not promised to produce identical training arrays.

The packager creates `dist/v1.0.0/paper.pdf`, `paper_source.zip`, `repository_bundle.zip`, and `SHA256SUMS.txt`. The source ZIP is directly compilable; the repository ZIP has the prefix `base-model-upgrade-non-regression/` and excludes caches, temporary verification directories, replay outputs, and its own release-output directory. The standalone preparation and local packaging operations perform no GitHub commit or upload.
