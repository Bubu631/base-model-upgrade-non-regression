# Certifying Model Upgrades with Slice-Wise Non-Regression and Incumbent Fallback

**Shengwei Zhang** — University of Pennsylvania  
**Tao Wu, Fei Qian** — Alibaba International Digital Commerce

[PDF](main.pdf) · [LaTeX](main.tex) · [References](references.bib) · [Results](results/) · [Standalone project guide](../../README.md)

This directory retains the original manuscript, figures, tables, manifests, and checkpoint evidence. Its path is preserved so the unchanged experiment scripts and original recorded hashes remain usable in the independent repository.

From the repository root, install `requirements-core.txt` and run `make verify` for bounded offline checks, `make reproduce-core` for synthetic trials, `make reproduce-digits` for both public classifier paths, or `make paper` to compile the supplied manuscript. Full reproduction writes existing result paths; use a separate clone to preserve the included runs. [Command profiles](../../configs/) provide dry-run previews and optional scratch destinations.

The paper distinguishes non-inferiority certification from failure to detect harm. Every public digits release returns the exact incumbent; the later balanced continuation is descriptive because it reuses holdouts. The results do not establish foundation-model, multilingual, or production-upgrade benefits. Full evidence and limitations appear in the manuscript and [root README](../../README.md).

The earlier collection-level version of this guide is preserved in [provenance](../../provenance/original_collection/base_upgrade_README.original.txt).
