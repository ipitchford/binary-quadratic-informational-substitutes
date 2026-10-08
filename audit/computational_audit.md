# Independent mathematical and computational audit

## Target and definition

The target is the non-strict strong-substitutes definition in Chen and
Waggoner, *Informational substitutes*, arXiv:1703.08636, Definition 2.2.3
(2017 version). That definition fixes its two compared signals on the
subsets lattice and permits a randomised garbling of one of them. It does
not assert submodularity for arbitrary pairs of garbled signals; footnote 4
explicitly distinguishes the earlier, stronger definition.

For binary sources X and Y the only nontrivial comparisons are the two
orientations X garbled while Y remains available, and Y garbled while X
remains available. All comparable pairs in the subsets lattice give
identities. Fresh randomisation is independent of the event and the other
source conditional on the garbled source.

Primary source inspected: https://arxiv.org/pdf/1703.08636

## Independent derivation

Write Z for a garbling of binary A, B for the other source, and
q=P(A=1|Z). Set e_i=P(E=1|A=i), r_ib=P(B=b|A=i), and
m_ib=P(E=1|A=i,B=b) wherever that cell has positive probability.
Let O be the cells b with both r_0b and r_1b positive, and put
d_b=m_1b-m_0b. For the normalisation V(S)=E[P(E=1|S)^2], the conditional
variance identity gives

    [V(B,Z)-V(Z)]-[V(A,B)-V(A)]
      = E[q(1-q) H(q)],

    H(q) = (e_1-e_0)^2
      - sum_{b in O} r_0b r_1b d_b^2 / ((1-q)r_0b+q r_1b).

This identity follows by subtracting the value lost when A is garbled
before and after observing B. It does not require a finite output alphabet
for Z: conditional expectation of the indicator of A=1 supplies q.

Each reciprocal-affine summand is convex on [0,1], so H is concave. Its
endpoint limits are

    H(0)=(e_1-e_0)^2-sum_{b in O}r_1b d_b^2,
    H(1)=(e_1-e_0)^2-sum_{b in O}r_0b d_b^2.

Both nonnegative endpoints therefore suffice. Either negative endpoint
allows a two-output garbling with one mixed report and one report revealing
a value of A. The construction in exact_checker.py supplies a rational
mixed posterior by a one-sided slope bound and verifies its negative gap
directly from the raw joint distribution.

This gives two endpoint inequalities per orientation, hence four for two
binary signals. The derivation also gives an oriented test when B has any
finite alphabet. Replacing scalar posterior differences by Euclidean
posterior-vector differences gives the finite-event quadratic-score
extension.

## Support and degenerate cases

1. If A has only one positive-probability value, the orientation holds as an
   identity; conditioning on an independent randomisation cannot change the
   value of B.
2. If a B value occurs for only one A value, that B value identifies A. It
   contributes zero conditional loss and must be omitted from the overlap
   sum. An arbitrary posterior must not be assigned to the missing cell.
3. If both binary sources are nondegenerate and the joint signal support
   has two cells, those cells lie on opposite diagonals and the sources
   determine one another. The overlap is empty and both orientations pass.
   Three- and four-cell signal supports have no nonconstant common
   deterministic information. Thus the potential distinction between a
   meet in the labelled subsets lattice and common information on the
   support does not alter this binary classification.
4. Zero event probabilities require no special convention beyond the
   ordinary posterior formula on positive signal cells.

## Exact examples

All eight-entry distributions below use lexicographic (E,X,Y) order.

### Positive margins with full support

The table (21,5,3,3,3,3,5,21)/64 has signal weights
(3,1,1,3)/8 and posteriors (1,3,5,7)/8. The two X-oriented margins are
9/64; the two Y-oriented margins are 3/16. Its whole-signal substitutes
margin is 13/256.

### Whole-signal substitution with a strict failure under disclosure

The table (21,15,5,39,27,1,11,9)/128 has the same signal weights and
posteriors (9,1,11,3)/16. Its whole-signal margin is 1/1024. The X margins
are zero; the Y margins are both -15/256.

Use the Y-source kernel

    P(mixed|Y=0)=1,
    P(mixed|Y=1)=1/3,

with the second report revealing Y=1. Direct expected-score values are

    V(Z,X)=213/1280,
    V(Z)=337/2048,
    V(X,Y)=49/256,
    V(Y)=193/1024.

Their oriented difference is -11/10240.

### Conditionally independent reports

Take P(E=1)=1/5. Conditional on E, draw X and Y independently and let each
flip E with probability 1/3. The table is
(16,8,8,4,1,2,2,4)/45. The determinants of both event-conditioned 2x2
tables vanish exactly, verifying conditional independence.

The whole-signal substitutes margin is 2/11475>0. Each orientation has
weight-row margins 241/68850 and -989/585225. The simple kernel

    P(mixed|X=0)=1,
    P(mixed|X=1)=1/2

has directly evaluated oriented gap -16/883575.

## Strictness and scope safeguards

The requested property is non-strict strong substitution. A stronger
statement about strictness should say precisely whether the channel loses
information about the original source. Forgetting an irrelevant appended
random coin changes a continuous-lattice partition while preserving the
source and all expected scores; literal lattice inequality alone is not a
safe criterion for strictness.

The four inequalities also do not imply diminishing marginal value
between every pair of nested partial disclosures. For the positive-margin
example above, the function f(q) giving the marginal value of Y under an
X-mixture has f''(0)=37/96>0. It is therefore not concave, despite satisfying
the requested strong-substitutes definition. This is a definition-boundary
check, not an objection to the theorem.

## Computational audit

Run from this directory:

    python audit_checks.py
    python audit_exhaustive.py

The first command checks eight named examples, all 255 nonempty uniform
joint supports, 12,750 exact binary-kernel comparisons, 212 directly
verified negative witnesses and 48 multi-output comparisons.

The second command checks all 6,560 nonzero eight-entry count tables in
{0,1,2}^8, after normalisation. These are count tables, not necessarily
distinct probability distributions. It checks all 13,120 orientations:

- 3,884 accepted orientations, each checked against 16 exact binary
  stochastic kernels, giving 62,144 direct score comparisons;
- 9,236 rejected orientations, each supplied with a strictly negative
  rational witness recomputed from the joint distribution;
- 1,870 count tables classified as strong substitutes;
- all 255 nonempty supports, including 320 degenerate-source orientations.

The finite-alphabet extension checks 105 cases: 100 generated from the
fixed seed 20261008 and five constructed passing cases. Event alphabets
range from two to four values, and the other signal from three to seven
values; the garbled source remains binary. The checks include 1,785 direct
score comparisons and 90 directly verified negative witnesses.

The exhaustive run passed in 26.129 seconds using CPython 3.12.14.
exhaustive_audit_results.json records the exact command, environment,
counts, timestamps and hashes. exhaustive_witnesses.jsonl contains every
rejected count table's exact witness. The direct score evaluator does not
use the classification formula, although all computations use Python's
Fraction class. These finite checks support the algebraic audit and do
not constitute a formal proof of the universal result.

## Remaining assurance boundary

The mathematical proof is an ordinary analytic proof, not a proof object
checked by a theorem prover. This was an independent derivation and raw
probability calculation within the same research session; it is not a
claim of external human peer review. No numerical search or finite-grid
test supplies the universal quantifier in the theorem. Public novelty
assessment remains the separate literature-review task.
