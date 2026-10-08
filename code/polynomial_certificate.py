"""Dependency-free exact checks of the two symbolic identities in the proof.

This script expands polynomials over Z. It does not sample parameter values.
The quartic identity is reduced by the exact row identities c_i^2=v_i h_i.
"""

from collections import defaultdict
import json


NAMES = ("q", "r0", "r1", "c0", "c1", "v0", "v1", "h0", "h1", "d", "w")
SIZE = len(NAMES)
ZERO_EXP = (0,) * SIZE


class Polynomial:
    def __init__(self, terms=None):
        self.terms = {e: c for e, c in (terms or {}).items() if c}

    @classmethod
    def constant(cls, value):
        return cls({ZERO_EXP: value})

    @classmethod
    def variable(cls, name):
        exponent = [0] * SIZE
        exponent[NAMES.index(name)] = 1
        return cls({tuple(exponent): 1})

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Polynomial) else Polynomial.constant(value)

    def __add__(self, other):
        result = defaultdict(int, self.terms)
        for exponent, coefficient in self.coerce(other).terms.items():
            result[exponent] += coefficient
        return Polynomial(result)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        result = defaultdict(int)
        for left_e, left_c in self.terms.items():
            for right_e, right_c in self.coerce(other).terms.items():
                exponent = tuple(a + b for a, b in zip(left_e, right_e))
                result[exponent] += left_c * right_c
        return Polynomial(result)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not (isinstance(power, int) and power >= 0):
            raise AssertionError('Exact audit condition failed')
        result = self.constant(1)
        for _ in range(power):
            result = result * self
        return result

    def reduce_row_identities(self):
        result = defaultdict(int)
        for exponent, coefficient in self.terms.items():
            exponent = list(exponent)
            for c_name, v_name, h_name in (("c0", "v0", "h0"), ("c1", "v1", "h1")):
                c_index = NAMES.index(c_name)
                pairs, exponent[c_index] = divmod(exponent[c_index], 2)
                exponent[NAMES.index(v_name)] += pairs
                exponent[NAMES.index(h_name)] += pairs
            result[tuple(exponent)] += coefficient
        return Polynomial(result)


def main():
    q, r0, r1, c0, c1, v0, v1, h0, h1, d, w = [Polynomial.variable(n) for n in NAMES]
    mixture = (1 - q) * r0 + q * r1
    reciprocal_identity = ((1 - q) * r1 + q * r0) * mixture - r0 * r1 - q * (1 - q) * (r1 - r0) ** 2
    if not (not reciprocal_identity.terms):
        raise AssertionError('Exact audit condition failed')

    covariance = (1 - q) * c0 + q * c1 + q * (1 - q) * w
    variance = (1 - q) * v0 + q * v1 + q * (1 - q) * d ** 2
    chord = (1 - q) * h0 + q * h1
    k0 = 2 * c0 * c1 + 2 * c0 * w - v0 * h1 - (v1 + d ** 2) * h0
    k1 = 2 * c0 * c1 + 2 * c1 * w - v1 * h0 - (v0 + d ** 2) * h1
    residual = covariance ** 2 - variance * chord - q * (1 - q) * ((1 - q) * k0 + q * k1 + w ** 2 * q * (1 - q))
    raw_terms = len(residual.terms)
    reduced = residual.reduce_row_identities()
    if not (not reduced.terms):
        raise AssertionError('Exact audit condition failed')
    print(json.dumps({
        "arithmetic": "exact integer coefficients in an 11-variable polynomial ring",
        "reciprocal_chord_identity_residual_terms": len(reciprocal_identity.terms),
        "quartic_identity_before_row_reduction_terms": raw_terms,
        "quartic_identity_after_row_reduction_terms": len(reduced.terms),
        "row_relations": ["c0^2=v0*h0", "c1^2=v1*h1"],
        "passed": True,
    }, indent=2))


if __name__ == "__main__":
    main()
