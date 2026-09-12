#!/usr/bin/env python3
"""Read-only integrity verification for the standalone model-upgrade project."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();checks=[]
    def check(path,expected):
        if not path.is_file():raise FileNotFoundError(path)
        if sha(path)!=expected:raise AssertionError('Hash mismatch: '+str(path))
        checks.append(str(path.relative_to(ROOT)))
    mapping=json.loads((ROOT/'provenance/split_mapping.json').read_text())
    for item in mapping['copied']:
        check(ROOT/item.get('preserved_original_copy',item['standalone_path']),item['sha256'])
    results=ROOT/'papers/base_upgrade/results'
    manifest=json.loads((results/'manifest.json').read_text())
    check(ROOT/'experiments/base_upgrade.py',manifest['script_sha256'])
    for name,expected in manifest['outputs'].items():check(results/name,expected)
    balanced=results/'digits_balanced';bm=json.loads((balanced/'digits_manifest.json').read_text())
    if not bm['status'].startswith('completed_'):raise AssertionError('Incomplete balanced experiment')
    for name,expected in bm['output_sha256'].items():check(balanced/name,expected)
    comparison=json.loads((results/'digits_path_comparison_manifest.json').read_text())
    check(ROOT/'experiments/summarize_digits_paths.py',comparison['script_sha256'])
    for name,expected in comparison['input_manifest_sha256'].items():check(ROOT/name,expected)
    for name,expected in comparison['output_sha256'].items():check(results/name,expected)
    result=dict(status='passed',hash_checks=len(checks),unique_files=len(set(checks)),verified=checks,
        scope='All copied scientific artifacts and the original manifests relevant to this project; no sibling repository or downloads required.')
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
