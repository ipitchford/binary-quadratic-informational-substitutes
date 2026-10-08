# Independent release review: binary quadratic informational substitutes

Date: 8 October 2026. Review track: **informal mathematical audit**. Version: Evidence Press candidate 1.0.0, corrected Markdown manuscript and the byte-identical code copies identified in the accompanying manifests.

## Decision and publication-blocker classification

**No unresolved mathematical or reproducibility blocker was found within the inspected release scope.** The four-test strong-substitutes theorem, the one-direction binary-source extension to a finite second signal, the rational failure disclosures, the structural consequences, and the corrected strong-complements appendix all withstand the independent derivations and the exact checks described here. The manuscript matches the intended Chen–Waggoner (2017), Definition 2.2.3 quantifier. The actual theorem concerns arbitrary probability tables and all admissible measurable disclosures; the proof establishes those scopes analytically.

The final manuscript identity is recorded in `final_manuscript_manifest.json`. The exact source checkers and their release copies agree byte-for-byte, as recorded in `release_code_identity.json`. The earlier notes audit is preserved in `review.md`; this release report supersedes its statement that the final manuscript and code were not yet available. Its detailed proof reconstruction remains supporting evidence.

This is a separate AI-agent mathematical review, not external human peer review. It provides no proof-assistant certificate and does not establish historical priority or a REF rating. Publication also involves editorial fit, attribution, and the separate prior-art audit; this finding only says that the reviewed mathematical statement and inspected implementations have no remaining identified blocker.

### Findings and disposition

| Finding | Original impact | Disposition |
|---|---|---|
| Ancillary $K_1$ formula previously had $-2c_1w$ | Material error in the optional polynomial criterion; the core overlap proof did not use it. | **Resolved.** Author notified the referee; independent endpoint differentiation confirms $+2c_1w$. Corrected paper and code agree. |
| XOR example assigned fair-bit numbers under an unqualified independence sentence | Numerical claim was false for biased independent bits. | **Resolved.** Referee found the issue; manuscript now specifies independent fair bits. A biased-input countercheck is preserved. |
| Abstract's rational-witness sentence did not explicitly restrict the input | Could overstate what the explicit arithmetic construction outputs. | **Resolved.** The abstract now says “For rational input.” |
| Brier normalization wording was ambiguous | Could obscure the score conversion. | **Resolved.** The manuscript explicitly gives $V(X)-P(E=1)$ for negative binary Brier loss. |
| New factorization check described $w^2$ as the leading coefficient of $N$ | Not literally true if $w=0$ and $N$ has lower degree. | **Resolved.** It now specifies the coefficient of $q^4$; the $w=0$ branch is covered. |
| Historical priority; all later expanded replay and packaging artifacts | Outside this delegated inspection boundary. | **Separate evidence obligation.** No priority, full-archive, or external-peer-review conclusion is inferred here. |

No change to the main four inequalities was required. The reviewer did not edit any candidate manuscript or implementation. Corrections were relayed to the author and then verified in the final source.

## 1. Mathematical scope and proof check

The primary source [Chen and Waggoner (2017), *Informational Substitutes*](https://arxiv.org/pdf/1703.08636), Definition 2.2.3 and footnote 4, fixes the comparison elements in the subsets lattice and permits the intermediate disclosure to range over the continuous lattice. The only nontrivial two-source comparisons are the two single-source disclosure directions. Thus manuscript Section 1 uses the correct strong-substitutes requirement. It does not substitute whole-signal submodularity or require a different full-lattice condition.

Theorem 2 makes the oriented extension explicit: the disclosed source is binary, while the secondary signal may be finite and the real target square-integrable. It expressly declines to classify the reverse orientation when the secondary signal is not binary. The two conditional-variance identities in Section 3.1 then give

\[
\Gamma_A(T)=E[Q(1-Q)H(Q)].
\]

Here $Q=E[1_{A=1}\mid\sigma(T)]$, so the argument works for arbitrary measurable output alphabets. It does not depend on a finite alphabet approximation, posterior density, or bounded number of outputs. The conditional independence of the disclosure randomness is stated and used exactly where it is needed.

The overlap rule is load-bearing and correctly retained. Outcomes of the other signal supported in only one source row reveal the source and contribute zero residual conditional variance. This both justifies the omitted terms and avoids inventing posteriors on null cells. Every two-binary-source support is either constant, a two-cell deterministic correspondence, a three-cell support with one overlap term in each direction, or full support with two terms. The event may be deterministic or have zero atoms within a positive source cell without requiring another convention.

Section 3.2 displays an exact decomposition of $H$ into its endpoint chord and nonnegative square terms. This proves sufficiency pointwise and then under expectation. Section 3.3 proves necessity using a mixed posterior near a failed endpoint and one pure posterior, with channel entries shown explicitly. Section 4 correctly restricts rational arithmetic guarantees to rational input and distinguishes the bounded number of arithmetic operations from bit cost. The one-sided bounds actually used in the executable were separately checked against the displayed $H$, including the zero-bound branches.

Theorem 1 follows by applying Theorem 2 twice, with constant sources handled before conditional rows are formed. Its definition matches the manuscript's stated target and includes every zero-cell pattern. No mismatch between the mathematical classifier and its implementation was found.

## 2. Corollaries, strictness, and examples

The deterministic coarsenings of a binary source are constant or fully revealing up to null outcomes and relabeling. The manuscript's weak/moderate equivalence is therefore valid for this two-binary-source definition. It does not assert weak/strong equivalence.

The independent-source condition is exactly zero interaction in the posterior mean, and its weak-margin formula is $-t^2\operatorname{Var}(A)\operatorname{Var}(B)$. Jensen's equality case and an independent orthogonal-basis calculation support both statements. Corollary 3 retains full source support and correctly characterizes an additive posterior by $uv\operatorname{Cov}(A,B)\ge0$. The contradiction using the product of two negative ratios and squared correlation is valid, including the cases where a coefficient or covariance is zero in the sufficient direction.

The sufficient-source observation remains valid on sparse support. Section 5's operational equality statement correctly asks whether the disclosure retains uncertainty about the source. It does not automatically equate that statement with literal strictness of every partition refinement in a lattice carrying extra independent randomness. The lower bound by the smallest endpoint margin, the relative value-loss bound when $D\ne0$, and the continuity statement within full support all follow from the same certificate.

All newly displayed exact numerical examples were checked. The conditionally independent error model in Section 6.3 has weak margin $2/11475$ but a failed oriented margin $-989/585225$, as claimed. The short manual disclosure in Section 6.2 has gap $-11/10240$. The marked figure values $H(1/2)=1/256$ and $H(1/4)=-11/1280$ are consistent with the exact formula and its plotted shape. The XOR correction is substantive but local: independent inputs with probabilities $1/4,1/3$ give margins $-8/9$ and $-3/4$, with weak margin $-1/6$; the manuscript now reserves $-1,-1/4$ for fair bits.

## 3. Ancillary complements appendix

Appendix A now includes both row identities $c_i^2=v_i h_i$, which remain valid at zero variance because then $c_i=h_i=0$. The covariance mixture and binary variance formula give a quartic $N(q)$ with zeros at both endpoints. The derivative calculation $K_0=N'(0)$, $K_1=-N'(1)$ and the $q^4$ coefficient $w^2$ determine the stated factorization. In particular, both cross terms $2c_iw$ have positive signs.

If the secondary signal is globally nonconstant, its mixture variance is positive for every interior posterior, even when a conditional row variance is zero. This makes the sign reduction to the concave quadratic valid throughout the interval's interior. Constant sources are handled before any division. The endpoint and possible interior-vertex tests are exactly the maximum test for that quadratic, and a positive value yields a feasible disclosure by binary posterior splitting. The implementation's positive-gap witnesses also passed the referee's independent raw-score recomputation.

This completes the ancillary classification within the claimed binary model. Neither this appendix nor the main theorem claims that every model is in one of the two strong classes.

## 4. Reproduction and independent implementation check

The reviewer inspected the entire `exact_checker.py`, `complements.py`, `audit_checks.py`, `complements_checks.py`, and `polynomial_certificate.py` before executing preserved copies. The replayed scripts make no network calls; no dependencies were changed and no candidate sources were mutated. The review used Python 3.12.14, integer coefficients, and `fractions.Fraction`; no numerical tolerance or floating-point sign test is involved.

All submitted non-timing replay fields matched. The substitute replay reproduced 12,750 binary comparisons, 48 multi-output comparisons, 212 negative witnesses, and eight examples. The complement replay reproduced 15,250 raw-score/quadratic checks, 174 positive witnesses, six examples, the specified random seed, and every classification count. The polynomial replay produced zero reciprocal residual terms and reduced eight raw quartic terms to zero. Both generated example JSON files matched the submitted files byte-for-byte.

Two additional independent programs distinguish the referee's own work from reproduction of the supplied code. `independent_checks.py` imports no submitted module and computes values directly by grouping event-zero and event-one masses. It covered all 6,560 nonzero count vectors in $\{0,1,2\}^8$, hence all 255 nonempty event-table support masks, with 65,600 direct channel comparisons, 64,000 posterior identity checks, 9,236 negative rational witnesses, and separate additive/independent corollary grids. It ran in 16.904158 seconds.

The later `release_checks.py` compares the preserved submitted implementations with those independent functions on all 6,560 vectors and 13,120 orientations. Every classification and coefficient agreed. Every one of the 9,236 returned substitute failure witnesses had a negative gap under the referee's direct scorer; every one of the 3,616 complement failure witnesses had a positive gap. It ran in 17.781884 seconds. These finite counts support implementation consistency and adversarial error detection; they do not replace the unrestricted analytic proof.

Detailed commands, environments, scope, hashes, logs, and limitations are in `VERIFICATION.md`, `independent_results.json`, `release_check_results.json`, `reproduction/reproduction_results.json`, and `claim_check_ledger.csv`. Later expanded enumeration scripts and archive/PDF assembly were not independently replayed by this referee and are not silently included in these results.

## 5. Fifteen-submetric quality assessment

These scores assess structure, signatures, transparency, reuse, and human readability of the corrected manuscript. They are judgments on a half-point 1–5 scale, not correctness probabilities, novelty judgments, publishability predictions, or REF ratings. They use proof-digest's informal mapping. All fifteen are assessable; no Lean parser or formal metrics were applied to prose.

| Dimension | Submetric | Score |
|---|---|---:|
| Structure | main_theorem_slimness | 4.5 |
| Structure | complexity_distribution | 4.5 |
| Structure | dependency_clarity | 5.0 |
| Signature quality | statement_naturalness | 5.0 |
| Signature quality | binder_economy | 4.5 |
| Signature quality | generality | 5.0 |
| Step transparency | tactic_transparency | 4.5 |
| Step transparency | explicit_lemma_use | 4.5 |
| Step transparency | broad_tactic_control | 5.0 |
| Reuse | helper_usefulness | 5.0 |
| Reuse | reuse_potential | 5.0 |
| Reuse | no_dead_helpers | 4.5 |
| Human readability | proof_readability | 4.5 |
| Human readability | mathlib_style (informal mapping) | 4.5 |
| Human readability | maintainability | 4.5 |

| Dimension | Mean |
|---|---:|
| Structure | 4.67 |
| Signature quality | 4.83 |
| Step transparency | 4.67 |
| Reuse | 4.83 |
| Human readability | 4.50 |
| Overall mean of fifteen scores | **4.70** |

**Structure.** Theorem 1 states the concrete four-test result, and Theorem 2 supplies its general proof. Sections 3.1–3.3 separate the variance identity, endpoint certificate, and necessity construction. The software witness follows in Section 4, while equality and examples follow the main proof. Appendix A is an independent ancillary result and does not hide a dependency needed for Theorem 1.

**Signature quality.** Theorem 2 states the binary-source result at the finite-secondary-signal and square-integrable-target generality its argument supports. Its hypotheses form precisely the rows used in the proof, and the overlap domain is explicit. Corollary 3 is quotable as a natural distributional condition, with full source support retained. The scalar-to-vector/Hilbert observations identify the role of the squared norm without overstating a reverse multivalued-source theorem.

**Step transparency.** The main calculation now shows the conditional Bernoulli variance after a secondary-signal observation and explains the zero-support branch. The endpoint identity displays all nonnegative terms, and both necessity kernels are explicit. Appendix A's derivative calculation removes the earlier reliance on an unilluminating sign-sensitive expansion. Remaining routine algebra is local; no solver or case-enumeration assertion hides the unrestricted proof.

**Reuse.** The oriented variance identity and posterior split are useful beyond the final binary-event application. The same residual drives the algorithm, structural corollaries, equality statement, and quantitative bounds. The complement appendix reuses the disclosure argument while exposing a distinct quadratic maximum test. There are no vacuous numbered helpers; the three numbered statements are two theorems and one corollary, with real mathematical content.

**Human readability.** The paper leads with a concrete decision rule and explains its interpretation before presenting the general proof. Its notation distinguishes row-weighted margins from the reversed endpoint indices, reducing a likely implementation error. The weak-but-not-strong example gives all four whole-signal values and an exact channel, making the operational difference inspectable. Future changes to the ancillary polynomial or implementation need not rewrite the main theorem; the preserved support and strictness qualifications make maintenance more reliable.

The prior notes scored 4.53 under the same rubric. The final score's increase reflects explicit theorem labels, clearer conditional-variance steps, standard mathematical notation, strengthened statement boundaries, and the added endpoint-derivative explanation. It is not a claim that the probability of correctness increased by a measurable amount.

## 6. Remaining evidence limits and final sanity check

No further mathematical edits are requested for the final inspected version. The source's exact definition was independently checked, but the separate novelty-search corpus was not fully re-audited in this task. The paper's bounded priority language must remain bounded. The absence of an identified issue is not a guarantee that no issue exists, and the final archive must still preserve the reviewed bytes and truthful verification descriptions.

The decisive sanity check remains the full-support separation example: $W=1/1024>0$ while an explicit two-report disclosure gives $Gamma_B=-11/10240<0$. A criterion based only on four whole-signal values would miss it; the four oriented endpoint margins identify the failure and the supplied code returns independently checkable witnesses.
