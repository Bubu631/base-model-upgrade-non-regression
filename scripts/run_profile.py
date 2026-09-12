#!/usr/bin/env python3
"""Run explicit command profiles; these did not configure the historical runs."""
from __future__ import annotations
import argparse,json,os,shlex,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',required=True,type=Path)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    path=args.config if args.config.is_absolute() else ROOT/args.config
    config=json.loads(path.read_text())
    if config.get('schema_version')!=1:raise ValueError('Unsupported profile schema')
    commands=config.get('commands')
    if not isinstance(commands,list) or not commands:raise ValueError('commands must be a nonempty array')
    print(config['name']+': '+config['description'],flush=True)
    for command in commands:
        if not isinstance(command,list) or not command or not all(isinstance(x,str) and x for x in command):
            raise ValueError('Each command must be a nonempty string-argument array')
        argv=[sys.executable if x=='{python}' else str(ROOT) if x=='{root}' else x for x in command]
        if any('{' in x or '}' in x for x in argv):raise ValueError('Unknown placeholder')
        print('$ '+shlex.join(argv),flush=True)
        if not args.dry_run:
            subprocess.run(argv,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)

if __name__=='__main__':main()
