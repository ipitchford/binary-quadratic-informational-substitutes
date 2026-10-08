#!/usr/bin/env python3
"""Replay the declared exact audits in an isolated directory, comparing records.

Only Python's standard library is required. Original evidence files are never
overwritten. Result paths and scripts are fixed by this audited package.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
SCRIPTS = ('exact_checker.py','finite_alphabet_audit.py','audit_checks.py',
           'audit_exhaustive.py','independent_checks.py','polynomial_certificate.py',
           'complements.py','complements_checks.py')
JOBS = ('polynomial_certificate.py','audit_checks.py','audit_exhaustive.py',
        'independent_checks.py','complements_checks.py')
IGNORED_FIELDS = {'elapsed_seconds','runtime_seconds','started_utc','finished_utc',
                  'python','python_version','platform','script_sha256','sha256',
                  'command','implementation'}


def stable(value):
    if isinstance(value,dict):
        return {k:stable(v) for k,v in value.items() if k not in IGNORED_FIELDS}
    if isinstance(value,list):
        return [stable(x) for x in value]
    return value


def compare_json(fresh,recorded):
    a=json.loads(fresh.read_text());b=json.loads(recorded.read_text())
    if stable(a)!=stable(b):
        raise AssertionError('Stable replay result mismatch: '+recorded.name)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=PACKAGE/'replay')
    args=p.parse_args(); destination=args.out.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit('Replay output directory must be empty or absent: '+str(destination))
    destination.mkdir(parents=True,exist_ok=True)
    clock=time.perf_counter();records=[]
    with tempfile.TemporaryDirectory(prefix='binary-quadratic-replay-') as temp:
        work=Path(temp)
        for filename in SCRIPTS:shutil.copy2(HERE/filename,work/filename)
        for script in JOBS:
            started=time.perf_counter()
            flags = ['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else []
            result=subprocess.run([sys.executable,*flags,script],cwd=work,capture_output=True,text=True)
            (destination/(script+'.stdout.log')).write_text(result.stdout)
            (destination/(script+'.stderr.log')).write_text(result.stderr)
            if result.returncode:
                raise RuntimeError(script+' failed; inspect the captured log')
            records.append({'script':script,'exit_code':result.returncode,
                            'elapsed_seconds':round(time.perf_counter()-started,3)})
            print(script+': passed',flush=True)
            if script=='polynomial_certificate.py':
                (work/'polynomial_certificate_result.json').write_text(result.stdout)
        comparisons=[
            ('polynomial_certificate_result.json','polynomial_certificate_result.json'),
            ('audit_results.json','initial_audit_results.json'),
            ('examples.json','named_examples_results.json'),
            ('exhaustive_audit_results.json','exhaustive_audit_results.json'),
            ('independent_results.json','independent_results.json'),
            ('complements_check_results.json','complements_check_results.json'),
            ('complements_examples.json','complements_examples_results.json'),
        ]
        for fresh,recorded in comparisons:
            compare_json(work/fresh,PACKAGE/'results'/recorded)
        witness=work/'exhaustive_witnesses.jsonl'
        expected=PACKAGE/'results/exhaustive_witnesses.jsonl'
        if hashlib.sha256(witness.read_bytes()).digest()!=hashlib.sha256(expected.read_bytes()).digest():
            raise AssertionError('The complete exact witness corpus changed')
        for path in work.iterdir():
            if path.is_file() and path.suffix in ('.json','.jsonl'):
                shutil.copy2(path,destination/path.name)
    report={'status':'PASS','jobs':records,
            'stable_record_comparisons':len(comparisons),
            'exact_witness_corpus_byte_match':True,
            'elapsed_seconds':round(time.perf_counter()-clock,3),
            'python':sys.version,
            'optimization_level':sys.flags.optimize,
            'universal_proof_machine_formalised':False,
            'scope':'Replay of declared exact algebra and finite checks; analytic proof is in the manuscript'}
    (destination/'replay_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
