#!/usr/bin/env python3
"""Reproducible exact sanity checks; these do not replace the analytic proof."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import time

from exact_checker import (
    normalise, from_signal_weights_and_posteriors, classify,
    orientation_data, direct_gap, analytic_gap, whole_signal_gap,
    exact_failure_witness, serialise,
)


def main():
    start = time.perf_counter()
    weights = (F(3,8), F(1,8), F(1,8), F(3,8))
    examples = {
        "strict_full_support": from_signal_weights_and_posteriors(
            weights, (F(1,8), F(3,8), F(5,8), F(7,8))),
        "weak_positive_strong_fail": from_signal_weights_and_posteriors(
            weights, (F(9,16), F(1,16), F(11,16), F(3,16))),
        "conditional_independence_weak_positive_strong_fail": normalise(
            (16,8,8,4,1,2,2,4)),
        "identical_signals_sparse_support": from_signal_weights_and_posteriors(
            (F(1,2),0,0,F(1,2)), (F(1,4),0,0,F(3,4))),
        "independent_signals_additive_posterior": from_signal_weights_and_posteriors(
            (F(1,4),)*4, (F(1,8),F(3,8),F(5,8),F(7,8))),
        "independent_signals_XOR": normalise((1,0,0,1,0,1,1,0)),
        "constant_source": normalise((1,2,0,0,3,4,0,0)),
        "constant_event": normalise((1,2,3,4,0,0,0,0)),
    }
    expected_strong = {
        "strict_full_support": True,
        "weak_positive_strong_fail": False,
        "conditional_independence_weak_positive_strong_fail": False,
        "identical_signals_sparse_support": True,
        "independent_signals_additive_posterior": True,
        "independent_signals_XOR": False,
        "constant_source": True,
        "constant_event": True,
    }
    records = {}
    for name, p in examples.items():
        c = classify(p)
        if not (c["strong_substitutes"] == expected_strong[name]):
            raise AssertionError('Exact audit condition failed')
        records[name] = {
            "probabilities": p, "classification": c,
            "weak_substitutes_margin": whole_signal_gap(p),
            "failure_witnesses": [w for source in ("X","Y")
                                  if (w := exact_failure_witness(p,source)) is not None],
        }
    p = examples["weak_positive_strong_fail"]
    kernel = ((F(1), F(0)), (F(1,3), F(2,3)))
    manual = direct_gap(p, "Y", kernel)
    if not (whole_signal_gap(p) == F(1,1024)):
        raise AssertionError('Exact audit condition failed')
    if not (manual["gap"] == F(-11,10240)):
        raise AssertionError('Exact audit condition failed')
    if not (manual["values"] == {
        "V_Z_other": F(213,1280), "V_Z": F(337,2048),
        "V_source_other": F(49,256), "V_source": F(193,1024)}):
        raise AssertionError('Exact audit condition failed')
    records["weak_positive_strong_fail"]["manual_witness"] = {
        "source": "Y", "kernel": kernel, **manual}
    p = examples["strict_full_support"]
    if not (whole_signal_gap(p) == F(13,256)):
        raise AssertionError('Exact audit condition failed')
    if not (orientation_data(p,"X")["margins"] == [F(9,64)]*2):
        raise AssertionError('Exact audit condition failed')
    if not (orientation_data(p,"Y")["margins"] == [F(3,16)]*2):
        raise AssertionError('Exact audit condition failed')
    p = examples["conditional_independence_weak_positive_strong_fail"]
    # Conditional independence follows from both 2x2 event-table determinants.
    if not (p[0]*p[3] == p[1]*p[2]):
        raise AssertionError('Exact audit condition failed')
    if not (p[4]*p[7] == p[5]*p[6]):
        raise AssertionError('Exact audit condition failed')
    if not (sum(p[4:]) == F(1,5)):
        raise AssertionError('Exact audit condition failed')
    if not (whole_signal_gap(p) == F(2,11475)):
        raise AssertionError('Exact audit condition failed')
    for source in ("X","Y"):
        if not (orientation_data(p,source)["margins"] == [F(241,68850),F(-989,585225)]):
            raise AssertionError('Exact audit condition failed')

    # Every nonempty joint support is represented, including event/signal
    # constants, deterministic signals, triangular and full signal support.
    # Direct raw-score checks cover a grid of exact binary disclosure kernels.
    grid = tuple(F(i,4) for i in range(5))
    kernels = tuple(((a,1-a),(b,1-b)) for a,b in product(grid,repeat=2))
    support_count = 0
    orientation_count = 0
    kernel_comparisons = 0
    constructed_negative_witnesses = 0
    strong_support_count = 0
    for mask in range(1,256):
        p = normalise([(mask >> i) & 1 for i in range(8)])
        c = classify(p)
        support_count += 1
        strong_support_count += c["strong_substitutes"]
        for source in ("X","Y"):
            d = c["directions"][source]
            orientation_count += 1
            for kernel in kernels:
                direct = direct_gap(p,source,kernel)["gap"]
                analytic = analytic_gap(p,source,kernel)
                if not (direct == analytic):
                    raise AssertionError((mask,source,kernel,direct,analytic))
                if d["passes"]:
                    if not (direct >= 0):
                        raise AssertionError((mask,source,kernel,direct))
                kernel_comparisons += 1
            if not d["passes"]:
                witness = exact_failure_witness(p,source)
                if not (witness["gap"] < 0):
                    raise AssertionError('Exact audit condition failed')
                constructed_negative_witnesses += 1

    # Multi-output kernels check aggregation across more than one posterior.
    multiple_kernels = (
        ((F(1,2),F(1,3),F(1,6)),(F(1,6),F(1,3),F(1,2))),
        ((F(0),F(1,3),F(2,3)),(F(1,2),F(1,2),F(0))),
        ((F(1,4),)*4,(F(1,10),F(1,5),F(3,10),F(2,5))),
    )
    multiple_comparisons = 0
    for p in examples.values():
        for source in ("X","Y"):
            for kernel in multiple_kernels:
                direct = direct_gap(p,source,kernel)["gap"]
                if not (direct == analytic_gap(p,source,kernel)):
                    raise AssertionError('Exact audit condition failed')
                if orientation_data(p,source)["passes"]:
                    if not (direct >= 0):
                        raise AssertionError('Exact audit condition failed')
                multiple_comparisons += 1

    root = Path(__file__).resolve().parent
    example_path = root / "examples.json"
    example_path.write_text(json.dumps(serialise(records),indent=2,sort_keys=True)+"\n")
    report = {
        "status":"PASS",
        "arithmetic":"Python fractions.Fraction only; no floating-point decisions",
        "full_proof_claim":False,
        "scope":"Independent exact raw-score checks against the proved classifier",
        "nonempty_joint_supports_checked":support_count,
        "strong_substitute_uniform_supports":strong_support_count,
        "orientations_checked":orientation_count,
        "binary_kernel_comparisons":kernel_comparisons,
        "constructed_exact_negative_witnesses":constructed_negative_witnesses,
        "multi_output_kernel_comparisons":multiple_comparisons,
        "named_examples_checked":len(examples),
        "elapsed_seconds":round(time.perf_counter()-start,3),
    }
    (root / "audit_results.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
