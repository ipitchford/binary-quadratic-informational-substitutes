# Proof outline: binary-source quadratic substitutes

## Statement

For a binary source $A$, finite secondary signal $B$, and a binary event $E$, consider $V(X)=E[P(E=1\mid X)^2]$. If both values of $A$ have positive probability, write $r_{ib}=P(B=b\mid A=i)$, $e_i=E[E\mid A=i]$, $D=e_1-e_0$, and $d_b=E[E\mid A=1,B=b]-E[E\mid A=0,B=b]$ only for outcomes in the common conditional support $O$. Then

\[
V(B,T)-V(T)\ge V(A,B)-V(A)
\quad\text{for every disclosure }T\perp(E,B)\mid A
\]

if and only if

\[
D^2\ge\sum_{b\in O}r_{0b}d_b^2,
\qquad D^2\ge\sum_{b\in O}r_{1b}d_b^2.
\]

The disclosure may have an arbitrary measurable output space. Applying this oriented result in both directions gives a complete classification for two binary sources. If either source is constant, the full substitutes comparisons are automatic. The arbitrary-finite-$B$ version remains an oriented statement.

## Idea

Garbling the source loses some quadratic value before observing the other source and some after observing it. Both losses are conditional variances of two possible posterior means. Their difference reduces to (q(1-q)H(q)), where $q$ is the posterior probability of the binary source and $H$ is a concave sum of reciprocal affine terms. Nonnegative endpoint values force a nonnegative gap for every disclosure. A negative endpoint creates a nearby interior posterior with a negative gap, and mixing that posterior with a fully revealing outcome gives a two-output counterexample with the required original prior.

## Outline

1. **Identify the two oriented comparisons.** Chen–Waggoner Definition 2.2.3 fixes the comparison elements in the subsets lattice, so only the incomparable singleton pair matters for two sources. *Notes Section 1; standard definition unpacking.*
2. **Replace a disclosure by its posterior source probability.** Let $Q=E[1_{A=1}\mid\sigma(T)]$, with $E[Q]=P(A=1)$; the conditional law of the finite pair ((E,B)) is a mixture of two fixed rows. *Section 3; standard conditional expectation.*
3. **Compute the two value losses.** The squared-score difference is (E[Q(1-Q)H(Q)]). Outcomes of $B$ outside the overlap identify the source and contribute zero to the second loss. *Sections 2–3; the point.*
4. **Reduce a continuum of inequalities to two endpoints.** The reciprocal-affine identity writes $H$ as its endpoint chord plus a nonnegative correction. Thus the two margins imply the comparison for every measurable disclosure without approximation. *Section 3; the point.*
5. **Construct a failure disclosure.** If an endpoint is negative, a nearby interior posterior and a pure posterior have a Bayes-plausible two-point mixture; only the interior outcome contributes a negative gap. A Lipschitz bound gives rational parameters for rational input. *Sections 3–4; the point, followed by routine arithmetic.*
6. **Apply both orientations and handle constants.** The theorem for binary $A$ can also be applied with binary $B$ as source; constant sources are handled before forming conditionals. *Sections 2 and 5; routine.*

## New components in the inspected submission

The oriented overlap formula is a reusable statement about a binary source and squared-error value. Its proof also supports a square-integrable real target or a finite event vector, since the variance identity becomes the square or squared Euclidean norm of a difference of conditional means. The endpoint certificate removes optimization over disclosure alphabets. The explicit rational channel turns a negative decision into an auditable operational failure. These descriptions identify the submission's components; they do not establish that the statements or techniques first appeared here.

The optional binary-secondary-signal covariance formula is a second representation of the same gap, with a concave quadratic numerator after factoring (q(1-q)). Its endpoints and possible interior maximum produce the complement criterion. It is not used to justify the main overlap formula.

## Prior work

The definition is from [Chen and Waggoner (2017), *Informational Substitutes*](https://arxiv.org/pdf/1703.08636), especially Definition 2.2.3 and the continuous-lattice discussion. Conditional variance, posterior martingales, Jensen's inequality, and splitting a binary prior into two posterior values are standard ingredients. This review inspected the foundational source and the supplied target, not the full related-literature corpus. A separate recorded novelty search is needed for any contribution-priority language; failure to find an earlier statement would not prove historical priority.

## Verification status

No proof assistant was used. The referee reconstructed the two variance calculations, the endpoint sufficiency/necessity proof, the rational witness bound, the support cases, the structural corollaries, and the corrected covariance factorization. An independently written exact-arithmetic program tested all 6,560 nonzero count vectors in $\{0,1,2\}^8$, both orientations, covering all 255 nonempty event-table support masks, with 65,600 direct disclosure comparisons and 9,236 rational failure witnesses. The finite checks do not establish the unrestricted statement; they are adversarial evidence alongside the mathematical derivation. Final manuscript and submitted-code reproduction are outside this phase's inspection boundary.
