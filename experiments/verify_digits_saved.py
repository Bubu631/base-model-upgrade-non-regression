#!/usr/bin/env python3
"""Recalculate saved digits predictions/gates in an isolated temporary copy."""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'papers/base_upgrade/results'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);args=parser.parse_args()
    original={str(p.relative_to(RESULTS)):sha(p) for p in RESULTS.rglob('*') if p.is_file()}
    with tempfile.TemporaryDirectory(prefix='.verification_tmp_',dir=ROOT) as directory:
        work=Path(directory);(work/'experiments').mkdir()
        for name in ['digits_upgrade.py','summarize_digits_paths.py']:
            shutil.copy2(ROOT/'experiments'/name,work/'experiments'/name)
        shutil.copytree(RESULTS,work/'papers/base_upgrade/results')
        run=subprocess.run([sys.executable,'experiments/summarize_digits_paths.py'],cwd=work,
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stderr or run.stdout)
        generated=work/'papers/base_upgrade/results'
        report=json.loads((generated/'digits_path_comparison_manifest.json').read_text())
        if report['prediction_and_gate_recalculation']!='passed_all_10_seed_path_runs':raise AssertionError(report)
        for name,expected in report['output_sha256'].items():
            if sha(RESULTS/name)!=expected:raise AssertionError('Regenerated comparison differs: '+name)
    if original!={str(p.relative_to(RESULTS)):sha(p) for p in RESULTS.rglob('*') if p.is_file()}:
        raise AssertionError('Delivered result changed during validation')
    result=dict(status='passed',seed_path_runs=10,predictions_and_gates='recalculated from saved checkpoints and sklearn digits',
        comparison_artifacts_byte_identical=True,delivered_files_unchanged=True,
        scope='No fitting, network downloads, or mutation of the recorded experiment files.')
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
