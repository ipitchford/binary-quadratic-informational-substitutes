# Independent informal mathematical audit

Date: 8 October 2026. Track: **I — Informal**. Target: the binary-event, two-binary-signal, quadratic-score classification in `classification_notes.md`, using Chen–Waggoner (2017), Definition 2.2.3.

## 1. Bounded conclusion

**No counterexample or unresolved load-bearing gap was found in the corrected core classification inspected here.** The two oriented endpoint conditions follow from an exact conditional-variance identity, and they are necessary as well as sufficient for all measurable disclosures generated from the source alone. The proof handles every binary support pattern without defining posteriors on null cells. The rational witness, the independent-signal and additive-posterior corollaries, the operational equality classification, and the corrected ancillary complement certificate withstand this review.

This is an independent mathematical reading and independently written finite check program. It is not proof-assistant verification, a guarantee of correctness, a priority determination, or a Research Excellence Framework assessment. The finite program imports neither the submitted implementation nor its test helpers. Its conclusions about arbitrary real probability tables and arbitrary measurable disclosures come from the argument reconstructed below, not from enumeration.

The author notified the referee of a sign defect in an earlier version of the ancillary covariance formula during this review. The referee independently confirmed both the defect and its correction. The inspected snapshot has the corrected plus sign. The source definition, core variance criterion, and main rational witness do not depend on that ancillary formula.

**Version boundary.** The scored object is the corrected research notes with SHA-256 `25c02d16f8ad3051c9c338206f20ba876e7d6bc77287c4d0527c67052aeb1fd5`. The final manuscript, submitted implementation, and release collateral were not yet supplied for this phase. A later manuscript/code review is required before applying this report to that release. Originals and precise hashes are recorded in `inspected_manifest.json`; the notes and target are preserved under `inspected/`.

## 2. Exact literature quantifier

The inspected primary source is [Chen and Waggoner, *Informational Substitutes*, March 2017, arXiv:1703.08636v1](https://arxiv.org/pdf/1703.08636), Definition 2.2.3, printed page 9, together with Definitions 2.1.2–2.1.4 and Examples 2.1.3–2.1.4. Definition 2.2.3 keeps the two comparison elements in the subsets lattice while allowing the intermediate disclosure in the continuous lattice. Footnote 4 distinguishes this from submodularity of the entire continuous lattice. The paper describes randomized functions through added independent randomness and discusses measurability in footnote 3.

For two base sources, the only nontrivial incomparable subsets are the two singleton subsets. The resulting comparisons are exactly

\[
V(B,T)-V(T)\ge V(A,B)-V(A)
\]

for each disclosure of $A$, and the analogous comparison for disclosures of $B$. Comparable subsets produce identities or monotonicity statements. Thus the target does not mistakenly require simultaneous arbitrary garblings of both sources, nor does it replace strong substitutes by the one whole-signal comparison. The finite-valued operational interpretation of the source is matched, and the conditional-expectation proof extends sufficiency to arbitrary measurable disclosure outputs.

The source's literal strict-partition language has a separate issue involving irrelevant random coordinates. The notes correctly keep their operational strictness assertion separate from that syntactic condition. No equilibrium corollary based on literal strictness is established by this audit.

## 3. Reconstruction of the load-bearing proof

### 3.1 Score normalization

For $S(q,e)=2qe-q^2$, reporting $q=p$ maximizes $2pq-q^2$ and gives expected score $p^2$. Negative scalar Brier loss gives $p^2-p$, while the categorical quadratic expected score gives $p^2+(1-p)^2=2p^2-2p+1$. Because the expectation of a posterior probability equals the prior, all compared marginal gains differ only by a positive scale. The normalization is sound.

### 3.2 The two information losses

Suppose $0<a=P(A=1)<1$. Let $r_{ib}=P(B=b\mid A=i)$, $e_i=E[E\mid A=i]$, and $D=e_1-e_0$. Let $T\perp(E,B)\mid A$, and define $Q=E[1_{A=1}\mid\sigma(T)]$. This definition does not require a density, a finite output alphabet, or a regular conditional distribution on the output space. It gives $E[Q]=a$.

Conditionally on $T$, the finite vector of probabilities for ((E,B)) is the mixture of the two source rows with weight $Q$. The Markov condition gives $E[E\mid A,T]=e_A$, so the projection identity yields

\[
V(A)-V(T)=D^2 E[Q(1-Q)].
\]

For a fixed $b$, put $s_b(q)=(1-q)r_{0b}+qr_{1b}$. When both $r_{0b},r_{1b}>0$, the conditional chance of $A=1$ after $(T,B=b)$ is $qr_{1b}/s_b(q)$. The variance of the two possible cell means is therefore

\[
\frac{q(1-q)r_{0b}r_{1b}}{s_b(q)^2}(m_{1b}-m_{0b})^2.
\]

Multiplying by the probability $s_b(q)$ of observing $b$ gives the summand in the notes. If $b$ occurs in only one row, it identifies $A$, so that conditional variance is zero. Thus

\[
\Gamma(T):=V(B,T)-V(T)-V(A,B)+V(A)
=E[Q(1-Q)H(Q)],
\]

where

\[
H(q)=D^2-\sum_{b:r_{0b}r_{1b}>0}
\frac{r_{0b}r_{1b}(m_{1b}-m_{0b})^2}{(1-q)r_{0b}+qr_{1b}}.
\]

The exact mixture identity is valid for any finite $B$, with a binary source $A$. This is an oriented generalization: reversing a multivalued $B$ does not fall under the binary-source theorem. The notes do not claim otherwise.

### 3.3 Endpoint sufficiency

Every denominator remaining in $H$ is positive on the closed interval. For $x,y>0$, direct multiplication by ((1-q)x+qy) verifies

\[
\frac{xy}{(1-q)x+qy}
=(1-q)y+qx-\frac{q(1-q)(y-x)^2}{(1-q)x+qy}.
\]

Substitution yields

\[
H(q)=(1-q)H(0)+qH(1)
+q(1-q)\sum_{b\in O}
\frac{d_b^2(r_{1b}-r_{0b})^2}{s_b(q)}.
\]

If both endpoint margins are nonnegative, every term is nonnegative. Hence every measurable disclosure has nonnegative expected gap. Equivalently, each reciprocal-affine function is convex, so $H$ is concave and lies above its endpoint chord. The sign is in the correct direction. No finite-disclosure approximation is required for sufficiency.

### 3.4 Endpoint necessity

If $H(0)<0$, continuity provides $q\in(0,a)$ with $H(q)<0$. A disclosure with posterior support ({q,1}) and posterior mean $a$ is feasible: take

\[
P(T=\mathrm{mix}\mid A=0)=1,
\qquad P(T=\mathrm{mix}\mid A=1)=\frac{(1-a)q}{a(1-q)}.
\]

Both channel probabilities lie in ([0,1]); the remaining output reveals $A=1$. Its gap is $(1-a)qH(q)<0$. If $H(1)<0$, the symmetric construction uses posterior support ({0,q}), $q\in(a,1)$, and gap $a(1-q)H(q)<0$. Consequently both endpoints must be nonnegative. Applying the same argument with the source labels exchanged proves the complete four-inequality classification.

The witness formulas in the notes make this continuity argument effective. Their $L$ bounds (|H'|), and the chosen distance from the failed endpoint is at most (-H(i)/(2L)), giving a strictly negative $H(q)$. The branch $L=0$ is necessary and is handled. Rational input produces rational $L,q$, channel entries, and gap. The number of arithmetic operations is bounded for fixed binary alphabets; this is not an assertion that arbitrary-precision arithmetic has unit bit cost.

## 4. Complete support analysis

The following support classification exhausts the possible supports of two binary source variables. Null event atoms inside positive ((A,B)) cells only make their posterior means equal to zero or one; no extra case is needed.

| Positive ((A,B)) cells | Structural case | Treatment |
|---|---|---|
| One | Both sources constant | All relevant comparisons are equalities. |
| Two in one row or column | One source constant | A disclosure of that source is independent randomness; the other orientation adds no information. |
| Two in different rows and columns | Sources determine one another | The overlap set is empty in each orientation. The two inequalities reduce to $D^2\ge0$. |
| Three | One missing joint source cell | Exactly one overlap term remains in each orientation; the other outcome determines the source. |
| Four | Full source support | Both overlap terms occur in each orientation. |

This covers all fifteen nonempty source support masks. The independent enumeration also covers all 255 nonempty masks of the eight ((E,A,B)) atoms. In particular, no division by a zero row mass is performed. The program bypasses constant-source orientations and never assigns a mean to a null cell. If $E$ is constant, all conditional means coincide and all gaps vanish.

## 5. Corollaries and strictness

**Independent sources.** Independence and nondegeneracy give the same strictly positive weights in both conditional rows. Then $D=\sum_b r_b d_b$, and the desired inequality is the reverse of Jensen's inequality for the square. Both can hold only with equality, meaning $d_0=d_1$. This is exactly $m_{00}+m_{11}=m_{01}+m_{10}$. The displayed weak-margin formula $-W^2\operatorname{Var}(A)\operatorname{Var}(B)$ follows by writing the posterior in the orthogonal basis (1,A-a,B-b,(A-a)(B-b)). It confirms that weak substitutes already force the same zero-interaction condition.

**Additive posterior.** With full source support and $m_{ab}=\kappa+ua+vb$, the two conditions become $(u+v\delta_B)^2\ge u^2$ and $(v+u\delta_A)^2\ge v^2$. If $uvC\ge0$, where $C=\operatorname{Cov}(A,B)$, expansion proves both. If $uvC<0$, both ratios $v\delta_B/u$ and $u\delta_A/v$ are negative, and the squared inequalities require each to be at most (-2). Their product is $\operatorname{Corr}(A,B)^2<1$, a contradiction. The stated full-support assumption is retained. The weak-margin formula $2uvC+v^2C^2/\operatorname{Var}(A)+u^2C^2/\operatorname{Var}(B)$ follows directly by evaluating the two conditional linear regressions and subtracting the variance of the full additive posterior.

**Sufficient source.** If $E\perp A\mid B$, the right-hand marginal of adding $A$ after $B$ is zero, so that orientation follows from monotonicity. In the other orientation, every overlap contrast at fixed $B$ is zero, so the endpoint conditions hold. This argument is valid on sparse support.

**Operational equality.** Under the substitute endpoint conditions, the displayed nonnegative decomposition shows that $H\equiv0$ exactly when both endpoints vanish and each $d_b(r_{1b}-r_{0b})=0$. Alternatively, the second derivative is a sum of nonpositive terms. A nonnegative concave function that has an interior zero must vanish identically. Otherwise $H(q)>0$ for every interior $q$, and the nonnegative integrand (Q(1-Q)H(Q)) has zero expectation exactly when $Q\in\{0,1\}$ almost surely. The disclosure then determines the base source up to null sets. This is a correct statement about retained uncertainty in the source, with the strict-lattice qualification preserved.

**Bounds and sensitivity.** The lower bound $Gamma(T)\ge\min(H(0),H(1))E[Q(1-Q)]$ follows from the endpoint chord. The stronger $C$-bound follows from $s_b(q)\le\max(r_{0b},r_{1b})$. The oriented classification depends on the conditional rows but not their nonzero prior weights; the reverse orientation may change under reweighting. Continuity holds within full source support. None of these statements asserts continuity of conditional posteriors through a disappearing support cell.

## 6. Ancillary covariance and complement certificate

Let $b(q)=b_0+(b_1-b_0)q$, $c(q)=(1-q)c_0+qc_1+q(1-q)w$, and $l(q)=(1-q)h_0+qh_1$, with the zero-variance convention in the notes. Write

\[
N(q)=c(q)^2-b(q)(1-b(q))l(q).
\]

The row relation $c_i^2=v_i h_i$ holds even when $v_i=0$, because then $B$ is rowwise constant and $c_i=h_i=0$. Thus $N(0)=N(1)=0$. Its coefficient of $q^4$ is $w^2$, so $N(q)=q(1-q)J(q)$ for a quadratic $J$ whose leading coefficient is $-w^2$. Differentiating at the endpoints gives

\[
K_0=N'(0)=2c_0c_1+2c_0w-v_0h_1-(v_1+d^2)h_0,
\]

\[
K_1=-N'(1)=2c_0c_1+2c_1w-v_1h_0-(v_0+d^2)h_1.
\]

The corrected sign in $K_1$ is **plus**. These two endpoint values and the quadratic leading coefficient determine

\[
J(q)=(1-q)K_0+qK_1+w^2q(1-q).
\]

This coefficient argument verifies the quartic identity for all admissible row moments, including zero row variances. If $B$ is nonconstant under the mixture, $b(q)(1-b(q))>0$ for every $q\in(0,1)$, even when a row variance is zero. Therefore the sign of the oriented chord gap equals the sign of (J(q)). A globally constant $B$ is treated before division.

For complements, a positive (J(q)) at any interior posterior can be converted to a violating binary disclosure by the same posterior-splitting argument used above. Thus complements in one orientation are equivalent to $J\le0$ throughout the interval. Writing $R=w^2$, $T=K_1-K_0+R$, gives $J(q)=K_0+Tq-Rq^2$. The maximum occurs at an endpoint or, if $R>0$ and $0<T<2R$, at (T/(2R)). The criterion $K_0,K_1\le0$, with the additional vertex inequality $4RK_0+T^2\le0$ when relevant, is therefore exact. Both orientations are required.

**Resolved defect.** On the notes' positive example with source weights ((5,3,3,5)/16) and posterior means ((1/10,1/2,1/2,9/10)), the corrected value is $K_1=27/1280$. The earlier minus-sign expression gives $-33/1280$ and would wrongly reject that example under the ancillary substitute test. The independent program reproduces these exact values. The correction was reported by the author, not discovered first by this referee.

## 7. Independent computational evidence

The source is `independent_checks.py`; full counts, version, runtime, script hash, and exact example output are in `independent_results.json`. The command was `python research/referee/independent_checks.py` from `/workspace/scratch/28ef880bbcda`, using Python 3.12.14, standard-library `fractions.Fraction`, and no floating-point tolerances. It exited with status 0 in 16.904158 seconds as measured inside the program.

| Check domain | Actual completed count | Scope |
|---|---:|---|
| Nonzero count vectors in $\{0,1,2\}^8$ | 6,560 | Duplicate normalized tables retained; all 255 nonempty event-atom support masks occur. |
| Nonconstant-source orientations | 12,800 | Includes overlap sizes zero, one, and two. |
| Constant-source orientations | 320 | Direct gaps are zero for all five tested channels. |
| Direct four-score channel comparisons | 65,600 | Five channels per orientation; the last has three outputs. |
| Posterior identity checks | 64,000 | At $q=0,1/7,1/2,6/7,1$. |
| Rational failure witnesses | 9,236 | Valid channel probabilities and directly summed strictly negative gaps. |
| Corrected substitute polynomial decisions | 12,800 | Agreed with endpoint contrasts, including sparse support. |
| Complement endpoint/vertex checks | 12,800 | Exact rational maxima; supported by the independent coefficient derivation above. |
| Operational strictness checks | 3,564 | Every passing nonconstant-source orientation. |
| Additive-posterior grid | 2,025 | Source count vectors in ${1,2,3}^4$; $u,v\in\{-1/4,-1/8,0,1/8,1/4\}$, $kappa=1/2$. |
| Independent-source grid | 2,304 | $P(A=1),P(B=1)\in\{1/4,1/2,3/4\}$; cell posteriors in ${0,1/3,2/3,1}^4$. |

No submitted checker was imported or executed in this phase. The direct score computation aggregates event-zero and event-one masses after a disclosure, and computes each value as a sum of $(\text{event-one mass})^2/(\text{total mass})$. It does not use the contrast criterion. Some ancillary comparisons reuse the proposed polynomial formula in the independently written program; their independence is therefore implementation independence, supplemented by the separate algebraic derivation, rather than a proof of the formula from testing alone.

Attempts to import SymPy failed in both available Python environments because that optional package was absent. No package was installed. The review instead used elementary coefficient reasoning and exact standard-library arithmetic. This environment limitation was not a mathematical failure.

## 8. Quality rubric for the inspected notes

The fifteen half-point scores apply to mathematical exposition and reusable proof structure. They do not rate correctness, novelty, publishability, or REF quality. The informal mapping from proof-digest is used; `mathlib_style` is interpreted as conventional mathematical naming, statement shape, and locality, not literal Lean style.

| Dimension | Submetric | Score |
|---|---|---:|
| Structure | main_theorem_slimness | 4.5 |
| Structure | complexity_distribution | 4.5 |
| Structure | dependency_clarity | 4.5 |
| Signature quality | statement_naturalness | 5.0 |
| Signature quality | binder_economy | 4.5 |
| Signature quality | generality | 4.5 |
| Step transparency | tactic_transparency | 4.5 |
| Step transparency | explicit_lemma_use | 4.0 |
| Step transparency | broad_tactic_control | 5.0 |
| Reuse | helper_usefulness | 4.5 |
| Reuse | reuse_potential | 5.0 |
| Reuse | no_dead_helpers | 4.5 |
| Human readability | proof_readability | 4.5 |
| Human readability | mathlib_style (informal mapping) | 4.0 |
| Human readability | maintainability | 4.5 |

| Dimension | Mean |
|---|---:|
| Structure | 4.50 |
| Signature quality | 4.67 |
| Step transparency | 4.50 |
| Reuse | 4.67 |
| Human readability | 4.33 |
| Overall, all fifteen subscores | 4.53 |

**Structure.** Sections 2–4 expose a short chain from a stated oriented theorem to a variance identity, endpoint reduction, and a constructed failure witness. The optional covariance approach is separated in Section 6 and is not a hidden prerequisite of the main theorem. The corollaries in Sections 8–11 follow from the same function $H$, keeping dependencies shallow. Giving the variance identity and splitting argument named lemma numbers would make this structure easier to cite.

**Signature quality.** Section 2 states the natural binary-source theorem for arbitrary finite secondary signals, with exactly the nondegeneracy condition needed to form both conditional rows. The overlap notation makes the domain of every cell mean explicit. The square-integrable-target observation identifies genuine additional generality, although it is not a fully restated theorem. The paper should continue to say explicitly that the finite-secondary-signal result is oriented.

**Step transparency.** Section 3 displays the principal function and both endpoint values, and its nonnegative identity reveals the mechanism without a solver. Section 4 spells out the channel probabilities and exact gap rather than invoking a generic existence theorem. The conditional-variance calculation is somewhat compressed, and Section 6 initially relied on a coefficient identity whose endpoint sign was vulnerable to transcription error. The derivative argument in this audit is a useful short addition to that ancillary proof.

**Reuse.** The two-row variance formula and posterior-splitting construction can be used outside binary events, while the decomposition of a reciprocal affine term is reusable algebra. Section 8's independence and additive-posterior consequences are actual applications of the criterion. The optional complement criterion is justified by the same polynomial and is not a decorative helper. The notes use standard conditional expectation and concavity at the places where they carry mathematical content.

**Human readability.** The statement precedes its proof and the support rule is explained at the point where a null-cell posterior would otherwise appear. The three examples distinguish positive margins, universal equality, and failure of a strong condition despite a positive whole-signal margin. The draft-note format uses inline code for mathematics and lacks stable proposition numbers, reducing its quality as a final manuscript. Repairs to notation or the optional polynomial are localized; they do not require reorganizing the core proof.

## 9. Recommendations and remaining obligations

There is no unresolved core mathematical correction requested on this inspected version. Before release, inspect the final manuscript and implementation against this statement, particularly the corrected sign of $K_1$, the overlap rule, the constant-signal branch, and the exact channel convention. A final implementation should continue to verify a produced witness by direct event-mass scoring, not only by recomputing its defining formula.

For exposition, explicitly state $c_i^2=v_i h_i$, explain $K_1=-N'(1)$, and retain the strict-lattice qualification. Do not turn the oriented finite-$B$ observation into an unproved complete classification of arbitrary two-finite-signal structures. A separate prior-art review must decide the permitted bounded contribution language; this referee examined the foundational definition, not the entire novelty-search corpus.

### Concrete sanity check

For source weights ((3,1,1,3)/8) and posteriors ((9,1,11,3)/16), direct score summation gives a whole-signal substitute margin $1/1024$. The $A$-oriented endpoint margins are both zero, whereas the $B$-oriented margins are both $-15/256$. In the $B$ orientation, the rational disclosure with mixture probabilities (1) from $B=0$ and $5/123$ from $B=1$ has mixture posterior $5/128$ and direct gap $-256975/281870336$. This explicitly separates weak substitutes from the claimed strong classification.
