"""Exact finite checks of revision identities and semantic rejection controls.

These computations support, but do not replace, the manuscript proofs.
"""
from fractions import Fraction as F
from itertools import product
import json
import exact_checker as ec
import complements as co

def require(ok, message):
    if not ok:
        raise ValueError(message)

def check_identities(p):
    checked = 0
    for source in ('X', 'Y'):
        d = ec.orientation_data(p, source)
        if d['degenerate_source']:
            continue
        c = co.orientation_certificate(p, source)
        r, margins = d['r'], d['margins']
        v = [r[i][1] * r[i][0] for i in (0, 1)]
        require(c['K0'] == v[0]*margins[1], 'Reversed left endpoint')
        require(c['K1'] == v[1]*margins[0], 'Reversed right endpoint')
        for q in (F(1,4), F(1,2), F(3,4)):
            h = d['delta_squared'] - sum(r[0][b]*r[1][b]*d['contrasts'][b]**2 /
                ((1-q)*r[0][b]+q*r[1][b]) for b in d['overlap'])
            bq = (1-q)*r[0][1]+q*r[1][1]
            require(co.polynomial_value(c,q) == bq*(1-bq)*h, 'Residual identity')
        a=d['priors'][1]; x=r[0][0]; y=r[1][0]; s=(1-a)*x+a*y
        if s not in (0,1):
            direct = a*(1-a)*sum(r[0][b]*r[1][b]*(d['delta_squared']-d['contrasts'][b]**2) /
                ((1-a)*r[0][b]+a*r[1][b]) for b in d['overlap'])
            weighted = a*(1-a)/(s*(1-s))*(a*y*(1-y)*margins[0]+(1-a)*x*(1-x)*margins[1])
            require(direct == weighted, 'Projective identity')
        checked += 1
    return checked

def main():
    n=0
    for counts in product(range(3), repeat=8):
        if sum(counts):
            n += check_identities(ec.normalise(counts))
    p=ec.from_signal_weights_and_posteriors([F(3,8),F(1,8),F(1,8),F(3,8)],
                                         [F(1,8),F(1,8),F(3,8),F(5,8)])
    require(not ec.classify(p)['strong_substitutes'], 'Separator must fail strong condition')
    # Direct Definition 2.8 check, independently expressed here from the
    # reviewer-supplied separator: every pair of subsets and added source.
    atoms=list(product(range(2),repeat=2))
    weights=[F(3,8),F(1,8),F(1,8),F(3,8)]
    means=[F(1,8),F(1,8),F(3,8),F(5,8)]
    def project(values, mask):
        out=[]
        for atom in atoms:
            indexes=[j for j,b in enumerate(atoms) if all(not (mask>>k&1) or atom[k]==b[k] for k in (0,1))]
            out.append(sum(weights[j]*values[j] for j in indexes)/sum(weights[j] for j in indexes))
        return out
    def normdiff(a,b): return sum(w*(x-y)**2 for w,x,y in zip(weights,a,b))
    projections=[project(means,m) for m in range(4)]
    for a,b,k in product(range(4),range(4),range(2)):
        require(normdiff(projections[b],project(projections[b],a)) >=
                normdiff(projections[b|1<<k],project(projections[b|1<<k],a|1<<k)),
                'Projective separator comparison')
    require(ec.direct_gap(p,'X',((F(1),F(0)),(F(1,39),F(38,39))))['gap'] == -F(323,8458240),
            'Separator raw-score witness')
    rejected=0
    for bad in ([F(-1)]+[F(2,7)]*7, [F(1,8)]*7, [0.125]*8):
        try: ec.validate(bad)
        except (ValueError, TypeError): rejected += 1
        else: raise ValueError('Invalid probability input accepted')
    try: ec.direct_gap(p,'X',((F(1),F(1)),(F(0),F(1))))
    except ValueError: rejected += 1
    else: raise ValueError('Invalid stochastic kernel accepted')
    original=ec.direct_gap
    try:
        ec.direct_gap=lambda *args: {'gap': F(0), 'values': {}}
        try: ec.exact_failure_witness(p,'X')
        except ValueError: rejected += 1
        else: raise ValueError('Forged zero-gap witness accepted')
    finally: ec.direct_gap=original
    print(json.dumps({'status':'PASS','nonconstant_orientations':n,
                      'projective_separator_comparisons':32,
                      'negative_controls_rejected':rejected,
                      'scope':'Finite identity coverage and semantic controls; not universal proof'},indent=2))

if __name__ == '__main__': main()
