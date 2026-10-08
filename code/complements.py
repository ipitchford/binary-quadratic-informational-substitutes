#!/usr/bin/env python3
"""Exact strong-complements classifier for a binary event and two binary signals.

Input is a JSON object containing an eight-entry ``probabilities`` array in
lexicographic (E,X,Y) order. Entries must be integers or rational strings.
The score is V(S)=E[P(E=1|S)^2]. A complement comparison requires gap <= 0.

For each orientation, the complete test is nonpositivity on [0,1] of
Q(q)=K0+T*q-R*q^2, where R >= 0. Thus endpoints and an interior maximum suffice.
A failure returns an exact disclosure kernel with a directly recomputed positive
gap. The direct evaluator comes from exact_checker and does not use this Q.

This file may sit beside exact_checker.py in a release package. In the research
workspace it also finds the unchanged checker in the sibling adversarial folder.
"""

from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import sys


try:
    from exact_checker import validate, orientation_data, direct_gap, serialise
except ModuleNotFoundError as exc:
    if exc.name != "exact_checker":
        raise
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "adversarial"))
    from exact_checker import validate, orientation_data, direct_gap, serialise


def polynomial_value(data, q):
    """Evaluate the exact quadratic certificate at a rational mixture weight."""
    q = F(q)
    return data["K0"] + data["T"] * q - data["R"] * q * q


def orientation_certificate(entries, source):
    """Return the necessary and sufficient endpoint/vertex conditions."""
    d = orientation_data(entries, source)
    if d["degenerate_source"]:
        return {
            "source": source,
            "degenerate_source": True,
            "priors": d["priors"],
            "passes": True,
            "reason": "A constant source has no information to withhold.",
        }

    b = [d["r"][i][1] for i in range(2)]
    variance = [x * (1 - x) for x in b]
    covariance = []
    for i in range(2):
        event_and_other = b[i] * d["cell_means"][i][1] if b[i] else F(0)
        covariance.append(event_and_other - d["means"][i] * b[i])
    conditional_gain = [covariance[i] ** 2 / variance[i] if variance[i] else F(0)
                        for i in range(2)]

    delta_b = b[1] - b[0]
    delta_e = d["means"][1] - d["means"][0]
    w = delta_b * delta_e
    c0, c1 = covariance
    v0, v1 = variance
    h0, h1 = conditional_gain
    k0 = 2 * c0 * c1 + 2 * c0 * w - v0 * h1 - (v1 + delta_b ** 2) * h0
    # Both cross terms have a PLUS sign. Under row exchange, delta_b and
    # delta_e both change sign, so their product w does not change sign.
    k1 = 2 * c0 * c1 + 2 * c1 * w - v1 * h0 - (v0 + delta_b ** 2) * h1
    r = w * w
    t = k1 - k0 + r
    interior = r > 0 and 0 < t < 2 * r
    vertex = t / (2 * r) if interior else None
    numerator = 4 * r * k0 + t * t if interior else None
    endpoint_passes = k0 <= 0 and k1 <= 0
    vertex_passes = not interior or numerator <= 0

    return {
        "source": source,
        "degenerate_source": False,
        "degenerate_other": b[0] == b[1] and b[0] in (0, 1),
        "priors": d["priors"],
        "conditional_other_probabilities": b,
        "conditional_event_means": d["means"],
        "conditional_covariances": covariance,
        "conditional_other_variances": variance,
        "conditional_gains": conditional_gain,
        "delta_other": delta_b,
        "delta_event": delta_e,
        "w": w,
        "K0": k0,
        "K1": k1,
        "R": r,
        "T": t,
        "endpoint_conditions": [k0 <= 0, k1 <= 0],
        "interior_vertex": interior,
        "vertex_q": vertex,
        "vertex_numerator_4R_Q": numerator,
        "vertex_condition": vertex_passes,
        "passes": endpoint_passes and vertex_passes,
    }


def classify(entries):
    entries = validate(entries)
    directions = {source: orientation_certificate(entries, source)
                  for source in ("X", "Y")}
    return {
        "strong_complements": all(d["passes"] for d in directions.values()),
        "directions": directions,
    }


def balanced_kernel(prior_one, q):
    """Realise q and one pure posterior with the prescribed prior mean.

    When q equals the prior, a constant disclosure already witnesses failure;
    the second output is then a null column. In all cases there are <=2 outputs.
    """
    a, q = F(prior_one), F(q)
    if not 0 < a < 1 or not 0 < q < 1:
        raise ValueError("Both prior and mixed posterior must be interior")
    if q < a:
        mix_given_one = (1 - a) * q / (a * (1 - q))
        return ((F(1), F(0)), (mix_given_one, 1 - mix_given_one))
    if q > a:
        mix_given_zero = a * (1 - q) / ((1 - a) * q)
        return ((mix_given_zero, 1 - mix_given_zero), (F(1), F(0)))
    return ((F(1), F(0)), (F(1), F(0)))


def exact_failure_witness(entries, source):
    """Produce <=2 disclosure outputs and certify a positive raw-score gap."""
    entries = validate(entries)
    d = orientation_certificate(entries, source)
    if d["passes"]:
        return None
    prior_one = d["priors"][1]
    slope_bound = abs(d["T"]) + 2 * d["R"]

    if d["interior_vertex"] and d["vertex_numerator_4R_Q"] > 0:
        q = d["vertex_q"]
        location = "positive interior quadratic maximum"
    elif d["K0"] > 0:
        q = prior_one / 2
        if slope_bound:
            q = min(q, d["K0"] / (2 * slope_bound))
        location = "positive left endpoint, moved inside using coefficient bound"
    elif d["K1"] > 0:
        distance = (1 - prior_one) / 2
        if slope_bound:
            distance = min(distance, d["K1"] / (2 * slope_bound))
        q = 1 - distance
        location = "positive right endpoint, moved inside using coefficient bound"
    else:
        raise AssertionError("A failed quadratic certificate must have a positive maximum")

    if not 0 < q < 1:
        raise ValueError("Witness posterior must be interior")
    q_value = polynomial_value(d, q)
    if q_value <= 0:
        raise ValueError("Witness polynomial must be positive")
    kernel = balanced_kernel(prior_one, q)
    direct = direct_gap(entries, source, kernel)
    if direct["gap"] <= 0:
        raise ValueError("Disclosure must violate complements under direct score computation")

    b0, b1 = d["conditional_other_probabilities"]
    b_q = (1 - q) * b0 + q * b1
    if not 0 < b_q < 1:
        raise ValueError("Second-source mixture must be nonconstant")
    weight = sum(d["priors"][i] * kernel[i][0] for i in range(2))
    predicted_gap = weight * q * (1 - q) * q_value / (b_q * (1 - b_q))
    if predicted_gap != direct["gap"]:
        raise ValueError("Quadratic and raw-score paths must agree exactly")
    return {
        "source": source,
        "construction": location,
        "posterior_of_mixed_report": q,
        "quadratic_at_mixed_posterior": q_value,
        "coefficient_slope_bound": slope_bound,
        "mixed_report_probability": weight,
        "kernel": kernel,
        **direct,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("probabilities", type=Path,
                        help="JSON object with an exact eight-entry probabilities array")
    args = parser.parse_args()
    data = json.loads(args.probabilities.read_text())
    entries = validate(data["probabilities"])
    result = classify(entries)
    result["witnesses"] = [w for source in ("X", "Y")
                           if (w := exact_failure_witness(entries, source)) is not None]
    print(json.dumps(serialise(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
