"""Independent finite adversarial checks of binary quadratic substitutes.

This file does not import the submitted implementation. Direct score differences
are computed by summing joint event masses after disclosures. Fraction arithmetic
is exact. The finite checks support, but do not prove, the unrestricted theorem.
"""

from collections import defaultdict, Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys
import time


HERE = Path(__file__).resolve().parent
INDEX = tuple(product(range(2), repeat=3))  # E, A, B
ZERO = F(0)
ONE = F(1)


def distribution(counts):
    total = sum(counts)
    return {index: F(n, total) for index, n in zip(INDEX, counts) if n}


def score(atoms, key):
    """E[P(E=1|signal)^2] from raw event masses and a signal projection."""
    masses = defaultdict(lambda: [ZERO, ZERO])
    for atom, p in atoms.items():
        masses[key(atom)][atom[0]] += p
    return sum((p1 * p1 / (p0 + p1) for p0, p1 in masses.values()), ZERO)


def direct_gap(p, orientation, channel):
    """Four independent score evaluations; no contrast-criterion calls."""
    x, z = (1, 2) if orientation == 0 else (2, 1)
    extended = {}
    for atom, mass in p.items():
        for t, chance in enumerate(channel[atom[x]]):
            if chance:
                extended[atom + (t,)] = mass * chance
    return (score(extended, lambda v: (v[z], v[3]))
            - score(extended, lambda v: v[3])
            - score(p, lambda v: (v[x], v[z]))
            + score(p, lambda v: v[x]))


def row_parameters(p, orientation):
    x, z = (1, 2) if orientation == 0 else (2, 1)
    joint = [[ZERO, ZERO], [ZERO, ZERO]]
    one = [[ZERO, ZERO], [ZERO, ZERO]]
    for atom, mass in p.items():
        joint[atom[x]][atom[z]] += mass
        if atom[0]:
            one[atom[x]][atom[z]] += mass
    weights = [sum(row) for row in joint]
    if not all(weights):
        return None
    r = [[v / weights[i] for v in row] for i, row in enumerate(joint)]
    e = [sum(row) / weights[i] for i, row in enumerate(one)]
    overlap = [j for j in range(2) if joint[0][j] and joint[1][j]]
    differences = {j: one[1][j] / joint[1][j] - one[0][j] / joint[0][j]
                   for j in overlap}
    D = e[1] - e[0]
    H0 = D * D - sum((r[1][j] * differences[j] ** 2 for j in overlap), ZERO)
    H1 = D * D - sum((r[0][j] * differences[j] ** 2 for j in overlap), ZERO)
    # Direct conditional moments obtain covariance independently of differences.
    b = [r[i][1] for i in range(2)]
    c = [one[i][1] / weights[i] - e[i] * b[i] for i in range(2)]
    v = [bi * (1 - bi) for bi in b]
    h = [ci * ci / vi if vi else ZERO for ci, vi in zip(c, v)]
    w = (b[1] - b[0]) * D
    d2 = (b[1] - b[0]) ** 2
    K0 = 2*c[0]*c[1] + 2*c[0]*w - v[0]*h[1] - (v[1]+d2)*h[0]
    K1 = 2*c[0]*c[1] + 2*c[1]*w - v[1]*h[0] - (v[0]+d2)*h[1]
    return dict(a=weights[1], r=r, e=e, overlap=overlap, differences=differences,
                D=D, H0=H0, H1=H1, b=b, c=c, v=v, h=h, w=w, K0=K0, K1=K1)


def H(par, q):
    r, ds = par['r'], par['differences']
    return par['D']**2 - sum((r[0][j]*r[1][j]*ds[j]**2 /
                             ((1-q)*r[0][j]+q*r[1][j])
                             for j in par['overlap']), ZERO)


def decomposition(par, q):
    r, ds = par['r'], par['differences']
    return ((1-q)*par['H0'] + q*par['H1'] + q*(1-q) *
            sum((ds[j]**2*(r[1][j]-r[0][j])**2 /
                 ((1-q)*r[0][j]+q*r[1][j]) for j in par['overlap']), ZERO))


def expected_gap(par, channel):
    a = par['a']
    answer = ZERO
    for u, v in zip(*channel):
        mass = (1-a)*u + a*v
        if mass:
            q = a*v/mass
            answer += mass*q*(1-q)*H(par, q)
    return answer


def witness(par):
    a, r, ds = par['a'], par['r'], par['differences']
    L = sum((r[0][j]*r[1][j]*ds[j]**2*abs(r[1][j]-r[0][j]) /
             min(r[0][j],r[1][j])**2 for j in par['overlap']), ZERO)
    if par['H0'] < 0:
        q = min(a/2, -par['H0']/(2*L)) if L else a/2
        k = (1-a)*q/(a*(1-q))
        channel = ((ONE, ZERO), (k, 1-k))
        predicted = (1-a)*q*H(par,q)
    else:
        if not (par['H1'] < 0):
            raise AssertionError('Exact audit condition failed')
        q = 1-min((1-a)/2, -par['H1']/(2*L)) if L else (1+a)/2
        k = a*(1-q)/((1-a)*q)
        channel = ((k, 1-k), (ONE, ZERO))
        predicted = a*(1-q)*H(par,q)
    if not (0 < q < 1 and H(par,q) < 0):
        raise AssertionError('Exact audit condition failed')
    if not (all(sum(row)==1 and all(0<=v<=1 for v in row) for row in channel)):
        raise AssertionError('Exact audit condition failed')
    return channel, predicted, q


def check_polynomial(par, q):
    b = (1-q)*par['b'][0]+q*par['b'][1]
    c = (1-q)*par['c'][0]+q*par['c'][1]+q*(1-q)*par['w']
    h = (1-q)*par['h'][0]+q*par['h'][1]
    bracket = (1-q)*par['K0']+q*par['K1']+par['w']**2*q*(1-q)
    if not (c*c-b*(1-b)*h == q*(1-q)*bracket):
        raise AssertionError('Exact audit condition failed')
    if 0 < b < 1 and 0 < q < 1:
        if not (bracket == b*(1-b)*H(par,q)):
            raise AssertionError('Exact audit condition failed')
    for i in range(2):
        if not (par['c'][i]**2 == par['v'][i]*par['h'][i]):
            raise AssertionError('Exact audit condition failed')
        if par['v'][i]:
            if not (par[f'K{i}'] == par['v'][i]*par[f'H{i}']):
                raise AssertionError('Exact audit condition failed')
    return bracket


def complements(par):
    k0, k1, R = par['K0'], par['K1'], par['w']**2
    T = k1-k0+R
    ans = k0 <= 0 and k1 <= 0
    if R and 0 < T < 2*R:
        ans = ans and 4*R*k0+T*T <= 0
    return ans


def independent_complement_max(par):
    """Evaluate covariance bracket at endpoints and its rational vertex."""
    k0, k1, R = par['K0'], par['K1'], par['w']**2
    points = [ZERO,ONE]
    if R:
        vertex = (k1-k0+R)/(2*R)
        if 0 < vertex < 1:
            points.append(vertex)
    vals = [check_polynomial(par,q) for q in points]
    return max(vals) <= 0


def make_table(signal_weights, posterior):
    return {(e,a,b): signal_weights[2*a+b] *
            (posterior[2*a+b] if e else 1-posterior[2*a+b])
            for e,a,b in INDEX
            if signal_weights[2*a+b] *
            (posterior[2*a+b] if e else 1-posterior[2*a+b])}


def special_cases():
    checks = {}
    p = make_table([F(5,16),F(3,16),F(3,16),F(5,16)],
                   [F(1,10),F(1,2),F(1,2),F(9,10)])
    par = row_parameters(p,0)
    if not ([par['H0'],par['H1']] == [F(9,100),F(9,100)]):
        raise AssertionError('Exact audit condition failed')
    if not (par['K0'] == par['K1'] == F(27,1280)):
        raise AssertionError('Exact audit condition failed')
    old_k1 = par['K1']-4*par['c'][1]*par['w']
    if not (old_k1 == F(-33,1280)):
        raise AssertionError('Exact audit condition failed')
    checks['resolved_sign_error'] = {'correct_K1':str(par['K1']),'old_K1':str(old_k1)}
    weights=[F(3,8),F(1,8),F(1,8),F(3,8)]
    p=make_table(weights,[F(9,16),F(1,16),F(11,16),F(3,16)])
    par0,par1=(row_parameters(p,i) for i in range(2))
    prior=score(p,lambda v: ())
    weak=score(p,lambda v:v[1])+score(p,lambda v:v[2])-prior-score(p,lambda v:(v[1],v[2]))
    if not (weak==F(1,1024)):
        raise AssertionError('Exact audit condition failed')
    if not ((par0['H0'],par0['H1'],par1['H0'],par1['H1']) == (0,0,F(-15,256),F(-15,256))):
        raise AssertionError('Exact audit condition failed')
    channel,predicted,q=witness(par1)
    observed=direct_gap(p,1,channel)
    if not (observed==predicted and observed < 0):
        raise AssertionError('Exact audit condition failed')
    checks['weak_not_strong']={'weak_margin':str(weak),'posterior_q':str(q),'gap':str(observed),
                             'channel':[[str(x) for x in row] for row in channel]}
    # Full-support additive corollary over a distinct grid.
    additive_count=0
    for counts in product(range(1,4),repeat=4):
        weights=[F(c,sum(counts)) for c in counts]
        a=weights[2]+weights[3]; b=weights[1]+weights[3]
        covariance=weights[3]-a*b
        for u,v in product([F(i,8) for i in range(-2,3)],repeat=2):
            posterior=[F(1,2)+u*x+v*z for x,z in product(range(2),repeat=2)]
            if not all(0<=m<=1 for m in posterior):
                continue
            p=make_table(weights,posterior)
            pars=[row_parameters(p,i) for i in range(2)]
            verdict=all(par['H0']>=0 and par['H1']>=0 for par in pars)
            if not (verdict == (u*v*covariance>=0)):
                raise AssertionError('Exact audit condition failed')
            additive_count += 1
    checks['additive_grid_cases']=additive_count
    # Independent weights, all posterior grids in {0,1/3,2/3,1}^4.
    independent_count=0
    for a,b in product([F(1,4),F(1,2),F(3,4)],repeat=2):
        weights=[(1-a)*(1-b),(1-a)*b,a*(1-b),a*b]
        for posterior in product([F(i,3) for i in range(4)],repeat=4):
            p=make_table(weights,posterior)
            pars=[row_parameters(p,i) for i in range(2)]
            verdict=all(par['H0']>=0 and par['H1']>=0 for par in pars)
            zero_interaction=posterior[0]+posterior[3]==posterior[1]+posterior[2]
            weak=score(p,lambda v:v[1])+score(p,lambda v:v[2])-score(p,lambda v:())-score(p,lambda v:(v[1],v[2]))
            if not (verdict==zero_interaction==(weak>=0)):
                raise AssertionError('Exact audit condition failed')
            if not (all(complements(par) for par in pars)):
                raise AssertionError('Exact audit condition failed')
            independent_count += 1
    checks['independent_grid_cases']=independent_count
    return checks


def main():
    started=time.perf_counter()
    stats=Counter()
    support_masks=set()
    channel_list=[((ONE,ZERO),(ZERO,ONE)),
                  ((ONE,ZERO),(ONE,ZERO)),
                  ((ONE,ZERO),(F(1,3),F(2,3))),
                  ((F(2,3),F(1,3)),(F(1,4),F(3,4))),
                  ((F(1,2),F(1,3),F(1,6)),(F(1,7),F(2,7),F(4,7)))]
    q_grid=[ZERO,F(1,7),F(1,2),F(6,7),ONE]
    for counts in product(range(3),repeat=8):
        if not any(counts):
            continue
        p=distribution(counts)
        stats['input_count_vectors']+=1
        support_masks.add(tuple(bool(c) for c in counts))
        for orientation in range(2):
            par=row_parameters(p,orientation)
            if par is None:
                stats['constant_source_orientations']+=1
                for channel in channel_list:
                    if not (direct_gap(p,orientation,channel)==0):
                        raise AssertionError('Exact audit condition failed')
                    stats['direct_channel_checks']+=1
                continue
            stats['nonconstant_source_orientations']+=1
            stats[f'overlap_size_{len(par["overlap"])}']+=1
            ss=par['H0']>=0 and par['H1']>=0
            # This is the corrected polynomial certificate, including zero rows.
            if not (ss == (par['K0']>=0 and par['K1']>=0)):
                raise AssertionError('Exact audit condition failed')
            stats['substitute_polynomial_decisions']+=1
            if not (complements(par)==independent_complement_max(par)):
                raise AssertionError('Exact audit condition failed')
            stats['complement_maximum_checks']+=1
            for q in q_grid:
                if not (H(par,q)==decomposition(par,q)):
                    raise AssertionError('Exact audit condition failed')
                check_polynomial(par,q)
                if ss:
                    if not (H(par,q)>=0):
                        raise AssertionError('Exact audit condition failed')
                stats['posterior_identity_checks']+=1
            for channel in channel_list:
                observed=direct_gap(p,orientation,channel)
                predicted=expected_gap(par,channel)
                if not (observed==predicted):
                    raise AssertionError('Exact audit condition failed')
                if ss:
                    if not (observed>=0):
                        raise AssertionError('Exact audit condition failed')
                if complements(par):
                    if not (observed<=0):
                        raise AssertionError('Exact audit condition failed')
                stats['direct_channel_checks']+=1
            if not ss:
                channel,predicted,q=witness(par)
                if not (direct_gap(p,orientation,channel)==predicted<0):
                    raise AssertionError('Exact audit condition failed')
                stats['negative_rational_witnesses']+=1
            else:
                stats['passing_orientations']+=1
                identically_zero = (par['H0']==par['H1']==0 and
                     all(par['differences'][j]*(par['r'][1][j]-par['r'][0][j])==0
                         for j in par['overlap']))
                if not ((H(par,F(1,2))==0)==identically_zero):
                    raise AssertionError('Exact audit condition failed')
                stats['strictness_checks']+=1
    result={'status':'passed','scope':'All nonzero unnormalised count vectors in {0,1,2}^8, both orientations; duplicate normalized tables retained.',
            'stats':dict(stats),'distinct_support_masks':len(support_masks),
            'channel_count_per_orientation':len(channel_list),
            'posterior_q_grid':[str(q) for q in q_grid],
            'special_cases':special_cases(),
            'arithmetic':'fractions.Fraction; no floating point comparisons',
            'python':sys.version,'platform':platform.platform(),
            'elapsed_seconds':round(time.perf_counter()-started,6),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'unrestricted_claim':'Not established by finite enumeration; independent informal derivation is in the review.'}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
