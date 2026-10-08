"""Compare the supplied release implementations with independent mass scoring.

Scripts were inspected before copying under reproduction/. The reference
variance parameters and direct score evaluator are independently implemented in
independent_checks.py. This is a finite cross-check, not a formal proof.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys
import time

from independent_checks import distribution, row_parameters, direct_gap, score, complements as reference_complements

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'reproduction'))
import exact_checker as submitted
import complements as submitted_complements


def main():
    start=time.perf_counter()
    stats=Counter()
    for counts in product(range(3),repeat=8):
        if not any(counts):
            continue
        p=distribution(counts)
        entries=tuple(F(c,sum(counts)) for c in counts)
        strong_results=[]
        comp_results=[]
        for orientation,source in enumerate(('X','Y')):
            ref=row_parameters(p,orientation)
            sub=(ref is None or ref['H0']>=0 and ref['H1']>=0)
            comp=(ref is None or reference_complements(ref))
            strong_results.append(sub)
            comp_results.append(comp)
            decision=submitted.orientation_data(entries,source)
            certificate=submitted_complements.orientation_certificate(entries,source)
            assert decision['passes']==sub
            assert certificate['passes']==comp
            if ref is not None:
                assert decision['margins']==[ref['H1'],ref['H0']]
                assert certificate['K0']==ref['K0']
                assert certificate['K1']==ref['K1']
            failure=submitted.exact_failure_witness(entries,source)
            assert (failure is None)==sub
            if failure is not None:
                gap=direct_gap(p,orientation,failure['kernel'])
                assert gap==failure['gap']<0
                stats['substitute_witnesses_checked_by_independent_score']+=1
            failure=submitted_complements.exact_failure_witness(entries,source)
            assert (failure is None)==comp
            if failure is not None:
                gap=direct_gap(p,orientation,failure['kernel'])
                assert gap==failure['gap']>0
                stats['complement_witnesses_checked_by_independent_score']+=1
            stats['orientation_decisions_checked']+=1
        assert submitted.classify(entries)['strong_substitutes']==all(strong_results)
        assert submitted_complements.classify(entries)['strong_complements']==all(comp_results)
        stats['tables_checked']+=1

    # Manuscript's conditional-independence example, via independent moments.
    p=distribution((16,8,8,4,1,2,2,4))
    weak=score(p,lambda v:v[1])+score(p,lambda v:v[2])-score(p,lambda v:())-score(p,lambda v:(v[1],v[2]))
    assert weak==F(2,11475)
    for orientation in (0,1):
        ref=row_parameters(p,orientation)
        assert (ref['H1'],ref['H0'])==(F(241,68850),F(-989,585225))
    special={'conditional_independence_example_weak_gap':str(weak)}
    # Manuscript's short manual disclosure, independently computed.
    p=distribution((21,15,5,39,27,1,11,9))
    kernel=((F(1),F(0)),(F(1,3),F(2,3)))
    manual=direct_gap(p,1,kernel)
    assert manual==F(-11,10240)
    special['manual_separation_witness_gap']=str(manual)
    # Strong/weak numerical XOR margins require fair bits; countercheck the
    # broader, earlier manuscript wording using an independent biased pair.
    a,b=F(1,4),F(1,3)
    p={(0,0,0):(1-a)*(1-b),(1,0,1):(1-a)*b,
       (1,1,0):a*(1-b),(0,1,1):a*b}
    refA,refB=(row_parameters(p,i) for i in (0,1))
    weak=score(p,lambda v:v[1])+score(p,lambda v:v[2])-score(p,lambda v:())-score(p,lambda v:(v[1],v[2]))
    assert refA['H0']==refA['H1']==F(-8,9)
    assert refB['H0']==refB['H1']==F(-3,4)
    assert weak==F(-1,6)
    special['biased_XOR_correction_check']={'a':str(a),'b':str(b),'A_margins':str(refA['H0']),'B_margins':str(refB['H0']),'weak_margin':str(weak)}

    # Compare supplied replay outputs, including counts and exact example files.
    reproducibility=[]
    runs=json.loads((HERE/'reproduction/reproduction_results.json').read_text())
    for record in runs:
        name=record['script']
        expected_name={'audit_checks.py':'audit_results.json',
                       'complements_checks.py':'complements_check_results.json',
                       'polynomial_certificate.py':'polynomial_certificate_result.json'}[name]
        expected=json.loads((HERE/'inspected'/expected_name).read_text())
        observed=dict(record['output'])
        expected.pop('elapsed_seconds',None)
        observed.pop('elapsed_seconds',None)
        assert observed==expected
        reproducibility.append({'script':name,'matching_non_timing_fields':True,'exit_status':record['exit_status']})
    for filename in ('examples.json','complements_examples.json'):
        expected=(HERE/'inspected'/filename).read_bytes()
        actual=(HERE/'reproduction'/filename).read_bytes()
        assert actual==expected
        reproducibility.append({'file':filename,'byte_identical':True,'sha256':hashlib.sha256(actual).hexdigest()})

    out={'status':'passed','statistics':dict(stats),'special_checks':special,
         'submitted_replay_reproduction':reproducibility,
         'elapsed_seconds':round(time.perf_counter()-start,6),'python':sys.version,
         'arithmetic':'fractions.Fraction; no floating point decisions',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Finite cross-check of preserved submitted implementation copies, including all 255 support masks. Independent direct score arithmetic checks every returned failure witness.'}
    (HERE/'release_check_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
