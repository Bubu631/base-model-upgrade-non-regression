PYTHON ?= python

.PHONY: verify test reproduce-core reproduce-digits digits-balanced figures paper papers clean release

verify:
	$(PYTHON) scripts/run_profile.py --config configs/verify.json

test:
	$(PYTHON) -m unittest discover -s tests -v

reproduce-core:
	$(PYTHON) scripts/run_profile.py --config configs/core.json

reproduce-digits:
	$(PYTHON) scripts/run_profile.py --config configs/digits.json

digits-balanced:
	$(PYTHON) experiments/digits_balanced.py
	$(PYTHON) experiments/summarize_digits_paths.py

figures:
	$(PYTHON) experiments/plot_digits.py

paper papers:
	cd papers/base_upgrade && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	cd papers/base_upgrade && latexmk -c

release:
	$(PYTHON) experiments/package_release.py --output dist/v1.0.0
