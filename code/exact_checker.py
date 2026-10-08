#!/usr/bin/env python3
"""Exact rational classifier and independent disclosure-witness verifier.

Probability entries are ordered (E,X,Y) lexicographically: 000,001,...,111.
The score normalisation is V(S)=E[P(E=1|S)^2].  Every conventional binary
quadratic score differs by a positive multiple and an affine term.

Classification uses the proved endpoint inequalities.  Witness verification
does NOT reuse their derived gap formula: it groups the joint probability
table after the stochastic kernel and computes four expected scores directly.
"""

from fractions import Fraction as F
from itertools import product
import argparse
import json
from pathlib import Path


STATES = tuple(product(range(2), repeat=3))


def rational(x):
    if isinstance(x, float):
        raise TypeError("Use integer counts or exact rational strings, not floats")
    return F(x)


def validate(entries):
    p = tuple(map(rational, entries))
    if len(p) != 8 or any(x < 0 for x in p) or sum(p) != 1:
        raise ValueError("Expected eight nonnegative exact entries summing to one")
    return p


def normalise(counts):
    counts = tuple(map(rational, counts))
    return validate([x / sum(counts) for x in counts])


def from_signal_weights_and_posteriors(weights, means):
    """Both arguments have four entries in XY order 00,01,10,11."""
    weights = tuple(map(rational, weights))
    means = tuple(map(rational, means))
    if len(weights) != 4 or len(means) != 4:
        raise ValueError("Expected four signal weights and four posteriors")
    if sum(weights) != 1 or any(x < 0 for x in weights):
        raise ValueError("Signal weights must be nonnegative and sum to one")
    if any(x < 0 or x > 1 for x in means):
        raise ValueError("Posteriors must lie in [0,1]")
    return validate([w * (1-m) for w, m in zip(weights, means)]
                    + [w * m for w, m in zip(weights, means)])


def orientation_data(entries, source):
    p = validate(entries)
    if source not in ("X", "Y"):
        raise ValueError("source must be X or Y")
    source_idx, other_idx = (1, 2) if source == "X" else (2, 1)
    masses = [[F(0), F(0)] for _ in range(2)]
    events = [[F(0), F(0)] for _ in range(2)]
    for state, mass in zip(STATES, p):
        i, b = state[source_idx], state[other_idx]
        masses[i][b] += mass
        if state[0] == 1:
            events[i][b] += mass
    priors = [sum(row) for row in masses]
    if 0 in priors:
        return {"source": source, "degenerate_source": True,
                "priors": priors, "passes": True, "margins": []}
    r = [[masses[i][b] / priors[i] for b in range(2)] for i in range(2)]
    means = [sum(events[i]) / priors[i] for i in range(2)]
    cell_means = [[events[i][b] / masses[i][b] if masses[i][b] else None
                   for b in range(2)] for i in range(2)]
    overlap = [b for b in range(2) if masses[0][b] and masses[1][b]]
    contrasts = {b: cell_means[1][b] - cell_means[0][b] for b in overlap}
    delta_squared = (means[1] - means[0]) ** 2
    # Row i is the weight row, not the posterior endpoint.  At q=0 the
    # limiting sum uses row 1; at q=1 it uses row 0.
    margins = [delta_squared - sum(r[i][b] * contrasts[b] ** 2
                                   for b in overlap) for i in range(2)]
    return {"source": source, "degenerate_source": False,
            "priors": priors, "r": r, "means": means,
            "cell_means": cell_means, "overlap": overlap,
            "contrasts": contrasts, "delta_squared": delta_squared,
            "margins": margins, "passes": min(margins) >= 0}


def classify(entries):
    directions = {source: orientation_data(entries, source) for source in ("X", "Y")}
    return {"strong_substitutes": all(d["passes"] for d in directions.values()),
            "directions": directions}


def direct_value(entries, observed, source=None, kernel=None):
    """Evaluate V from raw joint masses, optionally after an arbitrary kernel.

    observed is a tuple drawn from E-free names X,Y,Z.  Rows of kernel contain
    P(Z=z | source=i), with any finite output alphabet.  Z randomness is fresh
    and independent conditional on the source.  No classification identities
    or endpoint expressions occur in this evaluator.
    """
    p = validate(entries)
    if any(name not in ("X", "Y", "Z") for name in observed):
        raise ValueError("Only X, Y and Z may be observed")
    if kernel is None:
        if "Z" in observed:
            raise ValueError("A kernel is needed to observe Z")
        kernel = ((F(1),), (F(1),))
        source = "X"
    if source not in ("X", "Y"):
        raise ValueError("Kernel source must be X or Y")
    kernel = tuple(tuple(map(rational, row)) for row in kernel)
    if (len(kernel) != 2 or not kernel[0] or len(kernel[0]) != len(kernel[1])
            or any(sum(row) != 1 for row in kernel)
            or any(x < 0 for row in kernel for x in row)):
        raise ValueError("Invalid stochastic kernel")
    groups = {}
    for (e, x, y), mass in zip(STATES, p):
        i = x if source == "X" else y
        for z, probability in enumerate(kernel[i]):
            output_mass = mass * probability
            assignment = {"X": x, "Y": y, "Z": z}
            key = tuple(assignment[name] for name in observed)
            totals = groups.setdefault(key, [F(0), F(0)])
            totals[0] += output_mass
            if e:
                totals[1] += output_mass
    return sum(event_mass ** 2 / total_mass for total_mass, event_mass in groups.values()
               if total_mass)


def direct_gap(entries, source, kernel):
    other = "Y" if source == "X" else "X"
    values = {
        "V_Z_other": direct_value(entries, ("Z", other), source, kernel),
        "V_Z": direct_value(entries, ("Z",), source, kernel),
        "V_source_other": direct_value(entries, (source, other)),
        "V_source": direct_value(entries, (source,)),
    }
    gap = values["V_Z_other"] - values["V_Z"] - values["V_source_other"] + values["V_source"]
    return {"gap": gap, "values": values}


def whole_signal_gap(entries):
    return (direct_value(entries, ("X",)) + direct_value(entries, ("Y",))
            - direct_value(entries, ("X", "Y")) - direct_value(entries, ()))


def analytic_gap(entries, source, kernel):
    """Separately derived variance-loss identity, used only in sanity checks."""
    d = orientation_data(entries, source)
    if d["degenerate_source"]:
        return F(0)
    total = F(0)
    for z in range(len(kernel[0])):
        weight = sum(d["priors"][i] * kernel[i][z] for i in range(2))
        if not weight:
            continue
        q = d["priors"][1] * kernel[1][z] / weight
        if q in (0, 1):
            continue
        bracket = d["delta_squared"] - sum(
            d["r"][0][b] * d["r"][1][b] * d["contrasts"][b] ** 2
            / ((1-q) * d["r"][0][b] + q * d["r"][1][b])
            for b in d["overlap"])
        total += weight * q * (1-q) * bracket
    return total


def exact_failure_witness(entries, source):
    """Construct a two-output asymmetric disclosure if an endpoint fails.

    The one-sided slope bound gives a rational posterior without numerical
    optimisation or a search.  Direct recomputation must certify negativity.
    """
    d = orientation_data(entries, source)
    if d["passes"]:
        return None
    prior_one = d["priors"][1]
    r, contrasts = d["r"], d["contrasts"]
    if d["margins"][1] < 0:  # Posterior q -> 0.
        epsilon = -d["margins"][1]
        slope = sum(r[1][b] * contrasts[b] ** 2 * (r[1][b] - r[0][b]) / r[0][b]
                    for b in d["overlap"] if r[1][b] > r[0][b])
        q = prior_one / 2
        if slope:
            q = min(q, epsilon / (2 * slope))
        mixed_given_one = q * (1-prior_one) / (prior_one * (1-q))
        kernel = ((F(1), F(0)), (mixed_given_one, 1-mixed_given_one))
        endpoint = 0
    else:  # Posterior q -> 1.
        epsilon = -d["margins"][0]
        slope = sum(r[0][b] * contrasts[b] ** 2 * (r[0][b] - r[1][b]) / r[1][b]
                    for b in d["overlap"] if r[0][b] > r[1][b])
        distance = (1-prior_one) / 2
        if slope:
            distance = min(distance, epsilon / (2 * slope))
        q = 1-distance
        mixed_given_zero = prior_one * (1-q) / ((1-prior_one) * q)
        kernel = ((mixed_given_zero, 1-mixed_given_zero), (F(1), F(0)))
        endpoint = 1
    result = direct_gap(entries, source, kernel)
    if result["gap"] >= 0:
        raise ValueError("Witness must fail under direct score recomputation")
    return {"source": source, "failed_endpoint": endpoint,
            "posterior_of_mixed_report": q, "epsilon": epsilon,
            "one_sided_slope_bound": slope, "kernel": kernel, **result}


def serialise(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): serialise(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [serialise(v) for v in obj]
    return obj


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("probabilities", type=Path, help="JSON containing an eight-entry probabilities array")
    args = parser.parse_args()
    data = json.loads(args.probabilities.read_text())
    entries = validate(data["probabilities"])
    result = classify(entries)
    result["weak_substitutes_margin"] = whole_signal_gap(entries)
    result["witnesses"] = [w for source in ("X", "Y")
                           if (w := exact_failure_witness(entries, source)) is not None]
    print(json.dumps(serialise(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
