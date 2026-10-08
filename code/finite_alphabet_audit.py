#!/usr/bin/env python3
"""Independent oriented checks for a binary source and finite other alphabets.

The quadratic value here is the full vector score sum_e p(e|S)^2.
These checks cover the optional finite-event, finite-other-signal extension;
they make no claim about garbling a source with more than two outcomes.
"""

from fractions import Fraction as F
from itertools import product
import random


def moments(table, event_size, other_size):
    mass = [[F(0) for _ in range(other_size)] for _ in range(2)]
    event_mass = [[[F(0) for _ in range(event_size)]
                   for _ in range(other_size)] for _ in range(2)]
    for (e,a,b),p in table.items():
        mass[a][b] += p
        event_mass[a][b][e] += p
    prior = [sum(row) for row in mass]
    if 0 in prior:
        return {"passes":True,"degenerate":True,"prior":prior}
    r = [[mass[a][b]/prior[a] for b in range(other_size)] for a in range(2)]
    mean = [[sum(event_mass[a][b][e] for b in range(other_size))/prior[a]
             for e in range(event_size)] for a in range(2)]
    delta_squared = sum((mean[1][e]-mean[0][e])**2 for e in range(event_size))
    overlap = [b for b in range(other_size) if mass[0][b] and mass[1][b]]
    distance_squared = {
        b:sum((event_mass[1][b][e]/mass[1][b]
               -event_mass[0][b][e]/mass[0][b])**2 for e in range(event_size))
        for b in overlap}
    margins = [delta_squared-sum(r[a][b]*distance_squared[b] for b in overlap)
               for a in range(2)]
    return {"passes":min(margins)>=0,"degenerate":False,"prior":prior,
            "r":r,"delta_squared":delta_squared,"overlap":overlap,
            "distance_squared":distance_squared,"margins":margins}


def raw_value(table, event_size, observation_positions, kernel):
    groups = {}
    for (e,a,b),p in table.items():
        for z,k in enumerate(kernel[a]):
            state = (e,a,b,z)
            key = tuple(state[i] for i in observation_positions)
            v = groups.setdefault(key,[F(0)]*event_size)
            v[e] += p*k
    return sum(sum(x*x for x in v)/sum(v) for v in groups.values() if sum(v))


def raw_gap(table,event_size,kernel):
    return (raw_value(table,event_size,(3,2),kernel)
            -raw_value(table,event_size,(3,),kernel)
            -raw_value(table,event_size,(1,2),kernel)
            +raw_value(table,event_size,(1,),kernel))


def identity_gap(data,kernel):
    if data["degenerate"]:
        return F(0)
    result = F(0)
    for z in range(len(kernel[0])):
        w = sum(data["prior"][a]*kernel[a][z] for a in range(2))
        if not w:
            continue
        q = data["prior"][1]*kernel[1][z]/w
        if q in (0,1):
            continue
        term = data["delta_squared"]-sum(
            data["r"][0][b]*data["r"][1][b]*data["distance_squared"][b]
            / ((1-q)*data["r"][0][b]+q*data["r"][1][b])
            for b in data["overlap"])
        result += w*q*(1-q)*term
    return result


def witness_kernel(data):
    if data["passes"]:
        return None
    prior, r, distances = data["prior"][1],data["r"],data["distance_squared"]
    if data["margins"][1]<0:
        epsilon = -data["margins"][1]
        slope = sum(r[1][b]*distances[b]*(r[1][b]-r[0][b])/r[0][b]
                    for b in data["overlap"] if r[1][b]>r[0][b])
        q = min(prior/2,epsilon/(2*slope)) if slope else prior/2
        k = q*(1-prior)/(prior*(1-q))
        return ((F(1),F(0)),(k,1-k))
    epsilon = -data["margins"][0]
    slope = sum(r[0][b]*distances[b]*(r[0][b]-r[1][b])/r[1][b]
                for b in data["overlap"] if r[0][b]>r[1][b])
    s = min((1-prior)/2,epsilon/(2*slope)) if slope else (1-prior)/2
    q = 1-s
    k = prior*(1-q)/((1-prior)*q)
    return ((k,1-k),(F(1),F(0)))


def run_checks(seed=20261008,random_cases=100):
    rng = random.Random(seed)
    cases = []
    for case in range(random_cases):
        event_size = 2+case%3
        other_size = 3+case%5
        weights = {}
        for a,b in product(range(2),range(other_size)):
            active = rng.randrange(5)!=0
            for e in range(event_size):
                weights[e,a,b] = rng.randrange(5) if active else 0
        if not sum(weights.values()):
            weights[0,0,0] = 1
        denominator = sum(weights.values())
        cases.append((event_size,other_size,{k:F(v,denominator) for k,v in weights.items()}))
    # Construct accepted instances with many outcomes of B, arbitrary
    # correlation between A and B, and posterior depending only on A.
    for other_size in range(3,8):
        weights = {(e,a,b):F(rng.randrange(1,6)*(3 if e!=a else 1))
                   for e,a,b in product(range(2),range(2),range(other_size))}
        # Fix the common within-cell odds exactly (the independent random
        # weights above merely provide positive base weights).
        for a,b in product(range(2),range(other_size)):
            base = weights[0,a,b]
            weights[0,a,b] = base*(3 if a==0 else 1)
            weights[1,a,b] = base*(1 if a==0 else 3)
        denominator = sum(weights.values())
        cases.append((2,other_size,{k:v/denominator for k,v in weights.items()}))
    kernels = tuple(((a,1-a),(b,1-b))
                    for a,b in product((F(0),F(1,3),F(2,3),F(1)),repeat=2))
    kernels += (((F(1,2),F(1,3),F(1,6)),(F(1,6),F(1,3),F(1,2))),)
    passes = failures = comparisons = witness_count = 0
    for event_size,other_size,table in cases:
        data = moments(table,event_size,other_size)
        passes += data["passes"]
        failures += not data["passes"]
        for kernel in kernels:
            observed = raw_gap(table,event_size,kernel)
            derived = identity_gap(data,kernel)
            if not (observed==derived):
                raise AssertionError((event_size,other_size,observed,derived))
            if data["passes"]:
                if not (observed>=0):
                    raise AssertionError('Exact audit condition failed')
            comparisons += 1
        if not data["passes"]:
            kernel = witness_kernel(data)
            if not (raw_gap(table,event_size,kernel)<0):
                raise AssertionError('Exact audit condition failed')
            witness_count += 1
    if not (passes>=5):
        raise AssertionError('Exact audit condition failed')
    return {"status":"PASS","seed":seed,"cases":len(cases),
            "random_cases":random_cases,"constructed_passing_cases":5,
            "event_sizes":[2,3,4],"other_signal_sizes":[3,4,5,6,7],
            "binary_source_outcomes":2,"passing_orientations":passes,
            "failing_orientations":failures,"raw_kernel_comparisons":comparisons,
            "constructed_negative_witnesses":witness_count,
            "score":"sum_e posterior(e)^2"}
