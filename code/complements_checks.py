#!/usr/bin/env python3
"""Exact boundary and disclosure sanity checks for complements.py.

These finite checks do not replace the analytic theorem. They audit support
branches, coefficient orientation, witness construction, and the independent
raw joint-mass evaluator.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import json
import random

import complements
from exact_checker import (
    classify as classify_substitutes,
    direct_gap,
    from_signal_weights_and_posteriors,
    normalise,
    serialise,
)


def fixed_examples():
    return {
        "independent_xor": (from_signal_weights_and_posteriors(
            [F(1, 4)] * 4, [0, 1, 1, 0]), True),
        "independent_additive": (from_signal_weights_and_posteriors(
            [F(1, 4)] * 4, [0, F(1, 2), F(1, 2), 1]), True),
        "positive_substitute_margins": (from_signal_weights_and_posteriors(
            [F(5, 16), F(3, 16), F(3, 16), F(5, 16)],
            [F(1, 10), F(1, 2), F(1, 2), F(9, 10)]), False),
        "weak_substitutes_only": (from_signal_weights_and_posteriors(
            [F(3, 8), F(1, 8), F(1, 8), F(3, 8)],
            [F(9, 16), F(1, 16), F(11, 16), F(3, 16)]), False),
        "perfect_copies": (from_signal_weights_and_posteriors(
            [F(1, 2), 0, 0, F(1, 2)], [0, 0, 0, 1]), False),
        "irrelevant_signals": (from_signal_weights_and_posteriors(
            [F(3, 8), F(1, 8), F(1, 8), F(3, 8)], [F(1, 2)] * 4), True),
    }


def main():
    kernel_grid = [F(i, 4) for i in range(5)]
    kernels = [((x, 1-x), (y, 1-y)) for x, y in product(kernel_grid, repeat=2)]
    tables = [normalise([int(mask & (1 << i) != 0) for i in range(8)])
              for mask in range(1, 256)]
    rng = random.Random(20261008)
    for _ in range(50):
        counts = [rng.randrange(10) for _ in range(8)]
        if not (sum(counts)):
            raise AssertionError('Exact audit condition failed')
        tables.append(normalise(counts))

    category_counts = Counter()
    witness_constructions = Counter()
    witnesses = 0
    direct_checks = 0
    for table in tables:
        result = complements.classify(table)
        sub = classify_substitutes(table)["strong_substitutes"]
        category_counts[f"substitutes={sub},complements={result['strong_complements']}"] += 1
        for source in ("X", "Y"):
            certificate = result["directions"][source]
            witness = complements.exact_failure_witness(table, source)
            if not ((witness is None) == certificate["passes"]):
                raise AssertionError('Exact audit condition failed')
            if witness is not None:
                witnesses += 1
                witness_constructions[witness["construction"]] += 1
                if not (direct_gap(table, source, witness["kernel"])["gap"] > 0):
                    raise AssertionError('Exact audit condition failed')
            for kernel in kernels:
                gap = direct_gap(table, source, kernel)["gap"]
                direct_checks += 1
                if certificate["passes"]:
                    if not (gap <= 0):
                        raise AssertionError('Exact audit condition failed')

                # Independent raw score compared against Q at every mixed
                # output. This checks the optional polynomial formula itself,
                # including zero-support/zero-variance branches.
                if certificate["degenerate_source"] or certificate["degenerate_other"]:
                    if not (gap == 0):
                        raise AssertionError('Exact audit condition failed')
                    continue
                predicted = F(0)
                for z in range(2):
                    weight = sum(certificate["priors"][i] * kernel[i][z] for i in range(2))
                    if not weight:
                        continue
                    q = certificate["priors"][1] * kernel[1][z] / weight
                    if q in (0, 1):
                        continue
                    b0, b1 = certificate["conditional_other_probabilities"]
                    b_q = (1-q) * b0 + q * b1
                    predicted += (weight * q * (1-q) * complements.polynomial_value(certificate, q)
                                  / (b_q * (1-b_q)))
                if not (predicted == gap):
                    raise AssertionError('Exact audit condition failed')

    examples = {}
    for name, (table, expected) in fixed_examples().items():
        result = complements.classify(table)
        if not (result["strong_complements"] == expected):
            raise AssertionError('Exact audit condition failed')
        result["probabilities"] = table
        result["witnesses"] = [w for source in ("X", "Y")
                               if (w := complements.exact_failure_witness(table, source)) is not None]
        examples[name] = result

    # A substantive vertex check: both endpoints in one direction are strictly
    # negative, but its interior maximum is positive. Endpoints alone cannot
    # classify complements.
    vertex_example = examples["weak_substitutes_only"]["directions"]["Y"]
    if not (vertex_example["K0"] < 0 and vertex_example["K1"] < 0):
        raise AssertionError('Exact audit condition failed')
    if not (vertex_example["vertex_numerator_4R_Q"] > 0):
        raise AssertionError('Exact audit condition failed')

    output = {
        "passed": True,
        "arithmetic": "Python fractions.Fraction, no numerical tolerances",
        "all_nonempty_joint_support_patterns": 255,
        "random_weighted_tables": 50,
        "random_seed": 20261008,
        "binary_kernels_per_orientation": len(kernels),
        "raw_score_and_quadratic_identity_checks": direct_checks,
        "strict_positive_gap_witnesses": witnesses,
        "witness_construction_counts": dict(witness_constructions),
        "classification_counts": dict(category_counts),
        "fixed_example_count": len(examples),
        "vertex_needed_example_verified": True,
        "scope": "Finite sanity checks; the universal guarantee comes from the analytic polynomial theorem.",
    }
    destination = Path(__file__).resolve().parent
    (destination / "complements_check_results.json").write_text(
        json.dumps(serialise(output), indent=2, sort_keys=True) + "\n")
    (destination / "complements_examples.json").write_text(
        json.dumps(serialise(examples), indent=2, sort_keys=True) + "\n")
    print(json.dumps(serialise(output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
