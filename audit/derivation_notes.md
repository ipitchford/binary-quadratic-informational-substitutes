# Binary-source quadratic substitutes: complete classification

Independent mathematical notes, 8 October 2026. Source definition: Chen and Waggoner (2017), Definition 2.2.3, https://arxiv.org/html/1703.08636v1. These notes do not claim historical priority. Parent prior-art agent has been sent all structural simplifications for formula-level collision checks.

## 1. Exact scope and score normalisation

The state is a binary random variable `E`. The two base signals `A,B` are binary. All joint probability tables are permitted, including zeros. Use the quadratic score `S(q,e)=2qe-q²`, whose expected truthful score is `q²`. Thus `V(X)=E[(E[E|X])²]`. The usual negative Brier loss gives `V(X)-P(E=1)`; the doubled categorical quadratic score differs by positive scale and an affine term. Every substitute comparison is therefore unchanged.

Chen–Waggoner Definition 2.2.3 fixes its two comparison elements in the **subsets lattice** and permits only its intermediate element to range over randomized partial disclosures. For two base signals, the only nontrivial comparisons are

`V(B,T)-V(T) >= V(A,B)-V(A)` for every garbling `T` of `A`,

and the same comparison with `A,B` exchanged. Arbitrary simultaneous garblings of both signals are not required by this definition. The definition is also not submodularity of the value function on the whole continuous lattice; the paper's footnote 4 expressly distinguishes that older, stronger definition.

For two binary base signals, weak and moderate substitutes coincide, because every deterministic coarsening of a binary signal is either the signal or a constant, up to relabelling and null atoms. The same holds for weak and moderate complements. Randomized disclosures introduce the genuinely additional test in the strong notion.

## 2. One oriented theorem, allowing arbitrary finite B

Assume `P(A=0),P(A=1)>0`. For `i=0,1` put

`r_ib=P(B=b|A=i)` and `e_i=E[E|A=i]`.

Let `O={b:r_0b r_1b>0}` be the overlap of the two conditional supports. For `b in O`, put

`m_ib=E[E|A=i,B=b]`, `d_b=m_1b-m_0b`, and `D=e_1-e_0`.

Then the following are equivalent:

1. The oriented substitute comparison above holds for every randomized garbling of A, with finite or arbitrary measurable output alphabet.
2. The two inequalities

   `D² >= sum_{b in O} r_0b d_b²`

   and

   `D² >= sum_{b in O} r_1b d_b²`

   hold.

For binary `B`, this takes two sums with at most two terms. Applying the theorem in both orientations gives four scalar inequalities for the entire arbitrary `2×2×2` table. Only positive-probability cell posteriors are evaluated.

The same proof works for any square-integrable real target `Y`, with `E[E|...]` replaced by `E[Y|...]`, and squared-error utility. It also works for a finite event vector under the usual multicategory quadratic score by replacing scalar squares with squared Euclidean norms.

## 3. Proof

Let `a=P(A=1)`, let `T` be any garbling of `A`, and define `Q=P(A=1|T)`. Conditional on `T`, the law of `(E,B)` is the mixture of the two conditional rows with mixture weight `Q`; the Markov condition is `T ⟂ (E,B) | A`. Bayes plausibility gives `E[Q]=a`.

Rewrite the oriented substitute gap as

`[V(A)-V(T)] - [V(A,B)-V(T,B)]`.

The conditional-variance identity gives, for a posterior mixture weight `q`,

`V(A)-V(T)` contribution `q(1-q) D²`,

while the corresponding second loss is

`q(1-q) sum_{b in O} r_0b r_1b d_b² / [(1-q)r_0b+q r_1b]`.

For a `b` supported in only one row, observing `b` already identifies `A`, so its contribution to the second loss is zero. This explains the overlap restriction without assigning arbitrary posteriors to null cells.

Define the continuous function on `[0,1]`

`H(q)=D²-sum_{b in O} r_0b r_1b d_b² / [(1-q)r_0b+q r_1b]`.

All denominators here are strictly positive on the closed interval. The full expected substitute gap is

`E[Q(1-Q)H(Q)]`.

Each reciprocal-affine summand is convex; consequently `H` is concave. Its endpoint values are

`H(0)=D²-sum_O r_1b d_b²`,

`H(1)=D²-sum_O r_0b d_b²`.

If both endpoint values are nonnegative, concavity gives `H(q)>=0` everywhere. This proves the comparison for every garbling, including arbitrary measurable outputs; conditional expectation alone was used.

There is also an explicit nonnegative certificate, avoiding any appeal to differential calculus. For `s_b(q)=(1-q)r_0b+q r_1b`, direct multiplication gives

`r_0b r_1b/s_b(q)=(1-q)r_1b+q r_0b-q(1-q)(r_1b-r_0b)²/s_b(q)`.

Consequently

`H(q)=(1-q)H(0)+qH(1)+q(1-q)sum_O d_b²(r_1b-r_0b)²/s_b(q)`.

Under the endpoint conditions every term on the right is nonnegative. This identity supplies a rational certificate for every posterior mixture simultaneously.

Conversely, if an endpoint value is negative, continuity supplies an interior `q` on the same side of `a` with `H(q)<0`. A binary-output garbling can have posterior support `{q,1}` when `q<a`, or `{0,q}` when `q>a`, with posterior mean `a`. The pure posterior contributes zero and the interior one contributes strictly negatively. This violates the oriented substitute inequality. Thus the two inequalities are necessary.

## 4. Explicit rational counterexample garbling

No limiting channel is needed to witness failure. Write

`h_b=r_0b r_1b d_b²`,

`L=sum_O h_b |r_1b-r_0b| / min(r_0b,r_1b)²`.

Then `|H'(q)|<=L` on `[0,1]`.

If `H(0)<0`, choose

`q=min(a/2,-H(0)/(2L))` when `L>0`, or `q=a/2` when `L=0`.

This gives `0<q<a` and `H(q)<0`. Use

`P(T=mix|A=0)=1`,

`P(T=mix|A=1)=(1-a)q/[a(1-q)]`.

The other output reveals `A=1`. Its mixture-output probability is `(1-a)/(1-q)` and the exact gap is

`(1-a)q H(q)<0`.

If `H(1)<0`, choose

`q=1-min((1-a)/2,-H(1)/(2L))` when `L>0`, or `q=(1+a)/2` when `L=0`.

Use

`P(T=mix|A=1)=1`,

`P(T=mix|A=0)=a(1-q)/[(1-a)q]`.

The other output reveals `A=0`, and the exact gap is `a(1-q)H(q)<0`.

All quantities are rational when the input table is rational. For the fixed binary table, the decision and this witness use a bounded number of rational arithmetic operations and comparisons.

## 5. Degenerate cases

If either base signal is almost surely constant, the entire information structure is strongly substitutable: adding that signal yields zero value, and garbling it reveals only independent randomness. No undefined conditional row should be evaluated.

If `A,B` determine each other on their support, the overlap set is empty in each orientation, and both conditions are automatically true.

If exactly one joint `(A,B)` cell has zero probability, only one term remains in each oriented endpoint sum. If the event is deterministic, every contrast and every gain is zero, and the classification returns true.

## 6. Alternative quartic certificate, binary B

This offers an independent algebraic check of the variance proof. Let

`b_i=P(B=1|A=i)`, `c_i=Cov(E,B|A=i)`, `v_i=b_i(1-b_i)`,

`h_i=c_i²/v_i` if `v_i>0`, and `h_i=0` if `v_i=0`.

Put `d=b_1-b_0`, `w=d(e_1-e_0)`, `b(q)=b_0+dq`,

`c(q)=(1-q)c_0+q c_1+q(1-q)w`, `l(q)=(1-q)h_0+qh_1`.

The chord-gap numerator has the exact identity

`c(q)²-b(q)(1-b(q))l(q)`

`=q(1-q){(1-q)K_0+qK_1+w²q(1-q)}`,

where

`K_0=2c_0c_1+2c_0w-v_0h_1-(v_1+d²)h_0`,

`K_1=2c_0c_1+2c_1w-v_1h_0-(v_0+d²)h_1`.

The bracket is concave; its nonnegativity is equivalent to `K_0,K_1>=0`, unless `B` is constant, which is trivial. With both row B-variances positive, `K_i=v_i H(i)`. Boundary cases need this product relation interpreted carefully: when `v_i=0`, `K_i=0` regardless of `H(i)`, but the other endpoint and the curvature preserve the exact condition. The direct variance criterion in Section 2 is the preferred statement because it does not obscure support changes.

## 7. Three exact examples

### Positive strong-substitutes margins, nontrivial joint uncertainty

`P(A,B)=(5,3,3,5)/16` in row-major order, and

`P(E=1|A,B)=(1/10,1/2,1/2,9/10)`.

Both orientations have conditional row probabilities `(5/8,3/8)` and `(3/8,5/8)`, row means `1/4,3/4`, and cell mean contrasts `2/5,2/5`. Thus the squared marginal contrast is `1/4`, each conditional contrast sum is `4/25`, and all four margins are `9/100`.

These are conditionally independent signals given a fair event, each with error probability `1/4`.

### Useful independent signals with equality

`P(A,B)=(1/4,1/4,1/4,1/4)` and cell means `(0,1/2,1/2,1)`.

Both marginal contrasts equal `1/2`, and both cell contrasts equal `1/2`. All four endpoint margins are zero. Every garbling comparison has zero gap. The signals are both substitutes and complements in this score sense.

### Weak substitutes that fail the strong condition

`P(A,B)=(3,1,1,3)/8`, cell means `(9/16,1/16,11/16,3/16)`.

Equivalently the event-one joint masses are `(27,1,11,9)/128` and event-zero masses `(21,15,5,39)/128`. All eight masses are strictly positive.

The posterior mean is additive: `9/16+(1/8)A-(1/2)B`. In the `A` orientation, row means are `7/16,5/16` and cell contrasts both `1/8`, giving two zero margins. In the `B` orientation, row means are `19/32,5/32` and cell contrasts both `-1/2`; the squared marginal contrast is `49/256`, while each contrast sum is `1/4`. Both endpoint margins equal `-15/256`.

Nonetheless, the whole-signal substitute margin is `1/1024>0` for `V=E[posterior²]`. This illustrates why the four whole-signal values cannot settle the requested problem.

## 8. Structural corollaries

### Independent signals

Suppose both binary signals are nondegenerate and independent. In the `A` orientation the two row weights coincide, and the marginal contrast equals the weighted mean of the two conditional contrasts. Jensen's inequality gives the reverse of the required inequality, with equality only when the two cell contrasts coincide. Therefore strong substitutes hold if and only if

`m_00+m_11=m_01+m_10`.

This is precisely absence of an interaction term in the posterior mean. For independent binary signals, weak substitutes imply the same condition: the weak margin is the negative variance contribution of the posterior interaction.

More explicitly, with `W=m_11-m_10-m_01+m_00`, the weak margin is `-W² Var(A)Var(B)`.

### Additive posterior under associated signals

Suppose the joint `(A,B)` support is full and

`E[E|A,B]=kappa+u A+v B`.

Then strong substitutes hold if and only if `u v Cov(A,B)>=0`.

Proof: write `delta_B=P(B=1|A=1)-P(B=1|A=0)` and `delta_A=P(A=1|B=1)-P(A=1|B=0)`. The two oriented conditions become

`(u+v delta_B)²>=u²`, ` (v+u delta_A)²>=v²`.

If `uv Cov(A,B)>=0`, expansion proves both. Otherwise `u,v,delta_A,delta_B` are nonzero and both ratios `t=v delta_B/u`, `s=u delta_A/v` are negative. The two inequalities require `t<=-2` and `s<=-2`; but `ts=delta_A delta_B=Corr(A,B)²<1`, a contradiction. The full support assumption ensures nondegeneracy and correlation magnitude strictly below one.

For comparison, write `C=Cov(A,B)`, `s_A²=Var(A)`, `s_B²=Var(B)`. The weak margin for this additive posterior is `2uvC+v²C²/s_A²+u²C²/s_B²`. It can be positive when `uvC<0`, as the full-support example demonstrates.

### One signal is sufficient for the other about the event

If `E ⟂ A | B`, adding `A` after full `B` has zero gain, so the orientation garbling `B` is immediate; in the other orientation all overlap contrasts `d_b` are zero. Thus both strong substitute comparisons hold. The symmetric sufficiency statement also holds.

## 9. Equality and strict inequalities for nonrevealing garblings

Assume the two endpoint margins `H(0),H(1)` are nonnegative. A nonnegative concave function on `[0,1]` that vanishes at an interior point must vanish identically. Consequently either `H` is identically zero, or `H(q)>0` for every `0<q<1`.

An exact criterion for the first case is

`H(0)=H(1)=0` and `d_b(r_1b-r_0b)=0` for every `b in O`.

Indeed,

`H''(q)=-2 sum_O h_b(r_1b-r_0b)²/[(1-q)r_0b+q r_1b]³`.

Every term has one sign, so vanishing curvature is equivalent to the stated per-cell conditions. Together with the zero endpoint values it gives `H≡0`.

If `H≡0`, every oriented garbling comparison is an equality. Otherwise a comparison is an equality precisely when `Q in {0,1}` almost surely, that is, when the disclosure still determines `A`. Every disclosure with `P(0<Q<1)>0` then gives a strictly positive gap.

This is an operational strictness statement about disclosures of the base signal. Do not identify it automatically with the paper's syntactic strict-lattice definition: the continuous-lattice construction adjoins independent randomness, and forgetting irrelevant random bits can change a partition without changing any posterior. The main non-strict classification has no such ambiguity.

## 10. Quantitative lower bounds

Let `epsilon=min(H(0),H(1))>=0`. Then

`gap >= epsilon E[Q(1-Q)] = epsilon E[Var(A|T)]`.

Thus the endpoint margin controls the gain in proportion to the uncertainty about the first signal retained by its disclosure. If `D != 0`, the loss from garbling `A` is `D²E[Q(1-Q)]`, so this also gives a relative guarantee `gap >= (epsilon/D²)[V(A)-V(T)]`.

For a stronger bound, define

`C=sum_O d_b²(r_1b-r_0b)²/max(r_0b,r_1b)`.

The exact nonnegative identity in Section 3 gives

`H(q)>=(1-q)H(0)+qH(1)+Cq(1-q)`,

and

`gap >= H(0)E[Q(1-Q)²] + H(1)E[Q²(1-Q)] + C E[Q²(1-Q)²]`.

This lower bound can establish strict inequality even when both endpoint margins are zero.

## 11. Prior reweighting and sensitivity

For a fixed pair of conditional laws `Law(E,B|A=0)` and `Law(E,B|A=1)`, the one-oriented classification is independent of `a=P(A=1)`, as long as `0<a<1`. Changing the prior mass of the two rows changes the mixture weights of a witnessing garbling, but not whether such a witness exists. This statement concerns one orientation: reweighting the `A` rows generally changes the conditional laws used in the reverse orientation.

At a full-support table the four endpoint margins are continuous functions of the eight joint probabilities. Therefore strict positivity of all four margins gives an open neighbourhood of strong-substitutes tables. Near zero support, conditionals may change sharply; support terms must be handled by the overlap rule rather than by an arbitrary pseudo-count.

## 12. Optional complete binary complements certificate

The same chord identity in Section 6 also certifies strong complements. Assume neither base signal is constant. In one orientation put

`R=w²`, `T=K_1-K_0+R`.

The sign of the oriented gap at every interior mixture weight is the sign of

`Q(q)=K_0+Tq-Rq²`.

The comparison is complementary for every garbling if and only if `Q(q)<=0` on `[0,1]`. This is equivalent to

`K_0<=0`, `K_1<=0`,

and, when `R>0` and `0<T<2R`, the additional rational inequality

`4R K_0+T²<=0`.

The latter tests the concave quadratic at its interior maximum `q=T/(2R)`. If `R=0` or the vertex is outside the interval, the endpoint tests suffice. Apply both orientations. The zero-variance convention in Section 6 handles boundary tables; a constant signal is again trivial.

Failure also has an explicit rational disclosure certificate. If the interior vertex is positive, choose its rational mixture weight. Otherwise a positive endpoint remains. The coefficient bound `L_Q=|T|+2R` gives `|Q'(q)|<=L_Q`. For `K_0>0`, choose `q=min(a/2,K_0/(2L_Q))`, with `q=a/2` when `L_Q=0`; for `K_1>0`, choose `q=1-min((1-a)/2,K_1/(2L_Q))`, with the analogous midpoint convention. The chosen `q` is interior and has `Q(q)>0`. Balance this posterior against a pure posterior as in Section 4. If `q=a`, the constant disclosure already witnesses failure and the second output can have probability zero. Since `b(q)(1-b(q))>0` at every interior mixture whenever the other signal is nonconstant, the resulting substitute gap is strictly positive, as required to disprove complements.

The optional `complements.py` implements this criterion and directly recomputes every failing disclosure from the original eight joint masses through the independent `exact_checker.py` evaluator. `complements_checks.py` checked all 255 nonempty joint support patterns with equal supported-atom masses and 50 further weighted tables. Across 25 binary kernels per orientation, 15,250 exact raw-score/identity comparisons passed; 174 failing-oriented certificates produced strictly positive direct gaps. These finite checks audit implementation and boundary handling; the theorem supplies the universal conclusion.

This ancillary criterion does not imply that substitutability and complementarity exhaust information structures. The full-support weak/strong example in Section 7 lies in neither strong class: its first orientation has strictly positive gaps for all nonrevealing disclosures and its second has negative gaps near full revelation.

