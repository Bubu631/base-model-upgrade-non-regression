#!/usr/bin/env python3
"""Create standalone v1.0.0 assets locally; does not publish or assign a license."""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKIP_PARTS={'.git','.venv','venv','__pycache__','.cache','.pytest_cache','dist','runs'}
SKIP_SUFFIXES={'.aux','.log','.out','.blg','.fls','.fdb_latexmk','.pyc'}

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def archive(path,entries):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zipped:
        for source,name in entries:zipped.write(source,str(name))
    with zipfile.ZipFile(path) as zipped:
        bad=zipped.testzip()
        if bad:raise RuntimeError('ZIP CRC failure: '+bad)

def included(path,output):
    relative=path.relative_to(ROOT)
    return (path.is_file() and not path.is_symlink() and output not in path.parents
        and not any(x in SKIP_PARTS or x.startswith(('.verification_tmp_','.qa-')) for x in relative.parts)
        and path.suffix not in SKIP_SUFFIXES and path.name!='.DS_Store' and not path.name.endswith('.synctex.gz'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'dist/v1.0.0');args=parser.parse_args()
    output=args.output.resolve()
    if output==ROOT:raise ValueError('Output cannot equal the source root')
    subprocess.run([sys.executable,str(ROOT/'experiments/verify_artifact_integrity.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    output.mkdir(parents=True,exist_ok=True);paper=ROOT/'papers/base_upgrade'
    shutil.copyfile(paper/'main.pdf',output/'paper.pdf')
    sources=sorted(p for p in paper.rglob('*') if p.is_file() and
        (p.suffix in {'.tex','.bib','.bbl','.sty','.bst'} or ('figures' in p.parts and p.suffix=='.pdf')))
    archive(output/'paper_source.zip',[(p,p.relative_to(paper)) for p in sources])
    files=sorted(p for p in ROOT.rglob('*') if included(p,output))
    archive(output/'repository_bundle.zip',[(p,Path('base-model-upgrade-non-regression')/p.relative_to(ROOT)) for p in files])
    names=['paper.pdf','paper_source.zip','repository_bundle.zip']
    assets={name:{'sha256':sha(output/name),'bytes':(output/name).stat().st_size} for name in names}
    (output/'SHA256SUMS.txt').write_text(''.join(record['sha256']+'  '+name+'\n' for name,record in assets.items()))
    print(json.dumps({'status':'local_assets_created','assets':assets,'repository_files':len(files),'publication_performed':False},indent=2))

if __name__=='__main__':main()
