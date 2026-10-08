# Prior-art and definition audit: binary quadratic informational substitutes

Search date: 8 October 2026. Scope: the uploaded shortlist's binary event, two binary signals, fixed quadratic scoring rule, Chen–Waggoner 2017 strong-disclosure quantifier. This is a bounded audit, not a priority determination. The frozen target and finite fingerprints are in `target.yaml`; the query families are in `search_log.json`.

## Result for the research team

No inspected source states the candidate four endpoint inequalities, or their equivalent two row-weighted squared-contrast tests per orientation. No exact match was found by the formula and alias searches recorded here. The candidate contribution is the **quadratic-score-specific reduction to endpoint inequalities**, including arbitrary support and the extension with one binary signal and an arbitrary finite other signal. The general reduction to posterior distributions and the existence of small disclosure alphabets are established methods. Neither may be claimed as a new general theorem.

This leaves the mathematical theorem clear to prove within the recorded boundary. Historical novelty remains bounded uncertainty. Suitable language is: “We give an explicit criterion for this binary quadratic-scoring case. We did not find this criterion in the bounded prior-art search documented with the release.” Avoid “first”, “previously unknown”, and any claim to solve the unrestricted characterisation programme.

## 1. Definition that the theorem must use

Chen and Waggoner's March 2017 Definition 2.2.3 (printed p. 9; PDF p. 12) has **A and B on the subsets lattice**, with only A′ ranging over the continuous lattice and A∧B ≤ A′ ≤ A. Footnote 4 explicitly distinguishes earlier full-lattice definitions. With two base signals, the substantive inequalities are the two orientations involving a randomised disclosure of one signal and the other whole signal. The independent randomness construction is in §2.1.2 (printed pp. 7–8), especially Example 2.1.3. Definitions 2.4.1–2.4.3 give equivalent convex-score, entropy and Bregman descriptions. Under the vector quadratic score, all scalar squared-posterior marginal gains acquire a factor of two.

Source: Chen, Y., & Waggoner, B. (2017). *Informational substitutes*. https://arxiv.org/abs/1703.08636. Inspected PDF: https://arxiv.org/pdf/1703.08636.

### Quantifier translation used in the candidate proof

Let T be generated from A using a random seed independent of the information structure. Then T is conditionally independent of (E,B) given A. The oriented requirement is

\[
V(T,B)-V(T)\ge V(A,B)-V(A)\qquad\text{for every such }T.
\]

Exchange A and B for the second orientation. Requiring inequalities between two arbitrary partial disclosures, or requiring both terms designated A and B to range over the whole continuous lattice, changes the problem. In particular, global concavity of a disclosure value curve is not necessary merely because a generic Jensen argument would make it sufficient.

## 2. Closest inspected antecedents

| Source and location | What is already established | Difference from this target |
|---|---|---|
| Börgers, Hernando-Veciana, and Krähmer (2013), §3.1, Proposition 2 | An explicit binary-state, binary-signal classification when the substitute inequality holds for every decision problem; expressed through extreme posterior values and conditional uninformativeness. | Quantifies over all decision problems and considers whole signals. A fixed-score randomised-disclosure classification has different quantifiers. |
| Kong and Schoenebeck (2018), Lemma 14; Theorem 17 and Claim 18, pp. 14:10–14:12 | The relevant expected payment decomposes by disclosed messages. Optimisation over finite disclosure alphabets reduces to at most the original signal-alphabet size. Theorem 9/Corollary 10 provide an approximation scheme for fixed alphabet size. | The binary two-message reduction is prior art. They do not state the inspected four endpoint tests. Their numerical examples include genuinely partial binary revelation. |
| Anunrojwong, Chen, Waggoner, and Xu (2019/2020), §5, Theorems 4–5, pp. 10–12 of arXiv version | Optimisation over Bayes-plausible posterior distributions is explicit, with approximation schemes covering quadratic scoring. Theorem 3/Corollary 1 give exact tests for piecewise-linear expected score functions. | The exact piecewise-linear result does not immediately give the proposed exact constant-size criterion for the smooth quadratic score. |
| Anunrojwong (2018), Definition 2.9, pp. 9–10; Chapters 3–4 | Studies universal complements and scoring-rule design; almost all substantive work uses weak substitutes. | Its stated strong definition is the older full continuous-lattice version, so it is not a silent interchangeable source for the target definition. |
| Neyman and Roughgarden (2022), Definition 2.8, p. 9 | Projective substitutes constrain squared errors in iterated forecasts, with a finite subset quantifier. | Does not define the target by all randomised disclosures. A formula-level identification would need a separate proof. No such identification was found. |
| Frongillo, Neyman, and Waggoner (2021), Definition 2.6, p. 5 | Rectangle substitutes require weak substitutes after conditioning on every deterministic subrectangle. | For two binary signals, every proper nonempty subrectangle fixes at least one signal, so those added comparisons are trivial; it does not supply the target randomisation condition. |

The last sentence about binary rectangles is a direct inference from the inspected definition, not a theorem attributed to that paper.

## 3. Formula fingerprints and structural reruns

The first reduction writes the marginal gain for binary B as

\[
h(q)=\frac{\operatorname{Cov}_q(E,B)^2}{\operatorname{Var}_q(B)},
\]

where q mixes the two conditional rows given A. The oriented property asks whether h dominates its endpoint chord. In the binary-B case, clearing its quadratic denominator leaves q(1−q) times a concave quadratic. This structural discovery prompted searches for chord, derivatives, local truthful revelation, Brier information, covariance, and binary prediction markets.

The stronger simplification uses a square-integrable real target Y and finite B. Define

\[
r_{ib}=P(B=b\mid A=i),\quad m_{ib}=E[Y\mid A=i,B=b],\quad\mu_i=E[Y\mid A=i],
\]

and include only b with r₀b r₁b>0. The proposed disclosure residual is q(1−q)H(q), where

\[
H(q)=(\mu_1-\mu_0)^2-
\sum_b\frac{r_{0b}r_{1b}(m_{1b}-m_{0b})^2}{(1-q)r_{0b}+qr_{1b}}.
\]

Each reciprocal term is convex; hence H is concave. This yields the two proposed endpoint tests

\[
(\mu_1-\mu_0)^2\ge\sum_b r_{ib}(m_{1b}-m_{0b})^2,\quad i=0,1.
\]

This prompted a second formula/alias rerun: weighted mean-square forecast differences, projective and rectangle substitutes, binary experiments, conditional-variance submodularity, suppressor variables, reciprocal/harmonic means and chi-squared information. No matching classification was located.

The exact finite fingerprints include a symmetric noisy common-event case (all four margins 9/100), an independent additive case (all margins zero), XOR (all margins −1), and a repeated-signal support boundary (empty overlap). Their tables are recorded in `target.yaml`. They identify the normalisation and provide checks against false object matches. There is no natural enumerative sequence or generating-function family for an OEIS audit here; the rational functions, support patterns and exact tables are the relevant fingerprints.

## 4. Adjacent domains and why they do not settle the target

The variance formula resembles linear-regression explained variance and the absence of suppressor variables. Those conditions normally concern selected whole predictors and a linear predictor class. The target instead permits arbitrary randomised disclosures and uses the Bayes conditional mean. A result for set-function submodularity alone is insufficient.

Chi-squared information is another relevant alias because binary-state squared-posterior variation is a rescaled chi-squared dependence quantity. Abbe and Boix-Adserà (2019), Theorem 1.2 and Appendix A, study chi-squared subadditivity for spin-synchronisation models. Their graphical and channel assumptions differ from arbitrary joint (E,A,B), and no matching endpoint criterion was found there. This source was inspected to check the probability/mathematical-physics translation, not to claim an identification.

## 5. Missingness and limits

The corpus includes the originating GitHub statement, the inspected arXiv and Dagstuhl papers, Harvard's thesis repository, publisher records and author pages. The date is 8 October 2026. Searches were in English. No paid MathSciNet or zbMATH database was searched directly; Google Scholar's complete citing-paper graph was not exported. Broad web results are dependent on indexing, and mathematical formula search has low recall. No author enquiry was made because the user did not authorise contacting anyone. No unpublished correspondence or inaccessible manuscript can be ruled out.

The failed author-hosted thesis URL was replaced with the accessible Harvard DASH bitstream. The Harvard-hosted 2019 chapter timed out; the full arXiv version 2009.03607 was obtained instead. The Durham full-text download returned 403 via the web tool; its publication record and publisher's full introductory discussion were accessible, and the author-deposited 2010 version supplies an additional route if finer comparison is required.

## 6. Contribution adjudication

| Unit | Outcome | Permitted claim |
|---|---|---|
| General score/entropy/Bregman reformulation | COLLISION | Use and cite Chen–Waggoner. |
| Bayes-plausible posterior optimisation | COLLISION | Established information-design machinery; used explicitly in Anunrojwong et al. |
| At most two disclosure messages for a binary source | COLLISION | Special case of Kong–Schoenebeck's support reduction. |
| Endpoint-chord reduction at a fixed binary prior | BOUNDED UNCERTAINTY / routine corollary of established machinery | State and prove it as a lemma; avoid presenting the underlying splitting principle as new. |
| Four scalar tests for two binary signals and fixed quadratic scoring, with arbitrary support | CLEAR TO PROVE within this corpus; priority BOUNDED UNCERTAINTY | Give the exact criterion and proof; say no equivalent was found in the recorded search. |
| Two scalar tests for one binary source, finite other signal, real square-integrable target | CLEAR TO PROVE within this corpus; priority BOUNDED UNCERTAINTY | Present as the proved extension if the independent audit confirms all boundary cases. |
| Reproducible exact verifier and witnesses | Independently producible verification artefact | State what it checks and retain proof/code distinction. |

## References

### Definitions and nearest algorithmic work

Anunrojwong, J. (2018). *Structure and design of informational substitutes* [Undergraduate thesis, Harvard University]. https://dash.harvard.edu/entities/publication/1bf75cbb-60fb-456f-9ac0-2ad745440cc8

Anunrojwong, J., Chen, Y., Waggoner, B., & Xu, H. (2019). Computing equilibria of prediction markets via persuasion. In *Web and Internet Economics* (pp. 45–56). https://doi.org/10.1007/978-3-030-35389-6_4. Inspected expanded preprint (2020): https://arxiv.org/abs/2009.03607

Börgers, T., Hernando-Veciana, A., & Krähmer, D. (2013). When are signals complements or substitutes? *Journal of Economic Theory, 148*(1), 165–195. https://doi.org/10.1016/j.jet.2012.12.012

Chen, Y. (2026). *Operational characterizations of informational substitutes and complements* [Contributed problem statement]. EconCS-bench. https://github.com/aieconcs/econcs-bench/blob/main/informational-substitutes-complements/PROBLEM.md

Chen, Y., & Waggoner, B. (2017). *Informational substitutes* [Expanded preprint of FOCS 2016 paper]. https://arxiv.org/abs/1703.08636

Kong, Y., & Schoenebeck, G. (2018). Optimizing Bayesian information revelation strategy in prediction markets: The Alice Bob Alice case. *Leibniz International Proceedings in Informatics, 94*, 14:1–14:20. https://doi.org/10.4230/LIPIcs.ITCS.2018.14

### Alternative notions and probability alias

Abbe, E., & Boix-Adserà, E. (2019). *Subadditivity beyond trees and the chi-squared mutual information* [Preprint]. https://arxiv.org/abs/1902.02431

Frongillo, R., Neyman, E., & Waggoner, B. (2021). *Agreement implies accuracy for substitutable signals* [Preprint]. https://arxiv.org/abs/2111.03278

Neyman, E., & Roughgarden, T. (2022). *Are you smarter than a random expert? The robust aggregation of substitutable signals* (Version 2) [Preprint]. https://arxiv.org/abs/2111.03153

## Sanity check

The fixed-score target must accept independent additive signals with zero margins and reject XOR with negative margins. It must also tolerate empty overlap for perfectly repeated signals. These cases distinguish the proposed test from an accidental conditional-independence rule, an all-score universal criterion, and a strict-inequality convention.
