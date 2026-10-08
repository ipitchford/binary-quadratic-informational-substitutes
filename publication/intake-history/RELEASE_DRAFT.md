# Four checks show when two binary reports are informational substitutes

**Prospective Evidence Press release · 8 October 2026 · Research candidate v1.0.0**

## For curious readers

Two reports can repeat information, or one can make the other more useful. That distinction can change when a report is only partially disclosed. A forecaster might receive a vague summary, an occasional alert or a message produced with deliberate randomisation.

This paper gives an exact test for that situation when the event and both reports are binary and forecasts are assessed with quadratic scoring. For each report, compare how much its two outcomes change the forecast before and after the other report is known. Four weighted comparisons settle whether the reports are strong informational substitutes under the paper's specified definition. The test covers every randomised way of partially revealing either source, including disclosures with arbitrarily many possible messages.

The result is a theorem for every joint distribution in this model. It includes missing probability cells and highly unequal outcome frequencies. When a rational input fails a test, the accompanying program constructs a small disclosure that demonstrates the failure and computes its expected scores exactly.

An example shows why inspecting only complete reports can mislead. The two full reports have a positive substitutes margin of **1/1024**. A simple partial disclosure of one report changes the relevant margin to **−11/10240**. All eight event-report combinations have positive probability, so the failure does not depend on an impossible outcome or an undefined conditional forecast.

The proof also yields quantitative margins and equality conditions. An appendix provides an exact test for strong complements in the same binary model. The result offers a complete mathematical base case for studying information purchase, forecast aggregation and disclosure incentives. It does not establish which category any real forecasting system belongs to without a defensible joint probability model.

## For specialists

Let `V(S)=E[P(E=1|S)^2]`, and use Chen–Waggoner (2017), Definition 2.2.3. In the orientation that garbles binary A and adds B, put `r_ib=P(B=b|A=i)`, `D=P(E=1|A=1)−P(E=1|A=0)` and `d_b=P(E=1|A=1,B=b)−P(E=1|A=0,B=b)`. Sum only over the overlap `O={b:r_0b*r_1b>0}`. The oriented property holds precisely when `D^2 ≥ sum_O r_0b*d_b^2` and `D^2 ≥ sum_O r_1b*d_b^2`. Applying these conditions in both directions gives the complete four-test classification.

For a disclosure posterior `Q=P(A=1|T)`, the substitute gap equals `E[Q(1−Q)H(Q)]`, where

\[
H(q)=D^2-\sum_{b\in O}\frac{r_{0b}r_{1b}d_b^2}{(1-q)r_{0b}+qr_{1b}}.
\]

The reciprocal identity decomposes H into the interpolation of its endpoint values plus explicit nonnegative square terms. Negative endpoint values yield exact binary-report witnesses by balancing an interior posterior with a pure posterior. The oriented theorem extends to binary A, finite B and square-integrable real targets; a multivalued B does not automatically receive the reverse-direction classification.

For independent nondegenerate binary sources, strong substitutes hold exactly when the posterior table has no interaction term. For full support and an additive posterior `κ+uA+vB`, the condition is `uv Cov(A,B)≥0`.

## Evidence attached

The package includes the complete manuscript, editable mathematical source, exact classifiers for substitutes and complements, all 9,236 recorded substitute failure witnesses from the small-grid audit, independent check code, source-search records and an independent AI-agent referee report. Exact enumeration covered 6,560 nonzero count vectors and all 255 event-atom support patterns. Independent raw-score checks agreed with the classification. These finite results audit the implementation; the general theorem rests on the displayed proof.

## Status and limits

The selected binary quadratic-scoring problem is resolved by a complete analytic classification. The work remains a prospective publication candidate, with no external human peer review or proof-assistant formalisation claimed. The bounded literature search did not locate an equivalent endpoint criterion. Earlier work already supplies the general scoring-rule framework, small disclosure-alphabet reductions and posterior-optimisation methods; the manuscript credits those antecedents. The unrestricted information-substitutes programme remains outside the result.

### Primary sources

Chen, Y., & Waggoner, B. (2017). *Informational substitutes*. https://arxiv.org/abs/1703.08636

Kong, Y., & Schoenebeck, G. (2018). Optimizing Bayesian information revelation strategy in prediction markets: The Alice Bob Alice case. https://doi.org/10.4230/LIPIcs.ITCS.2018.14

Anunrojwong, J., Chen, Y., Waggoner, B., & Xu, H. (2019). Computing equilibria of prediction markets via persuasion. https://doi.org/10.1007/978-3-030-35389-6_4. Expanded preprint: https://arxiv.org/abs/2009.03607

### Sanity check

The explicit example's eight integer masses sum to 128. Its full-report margin is positive, while the declared mixed-report kernel produces a strictly negative gap when evaluated directly from those masses. The exact checker reproduces both signs without a floating-point tolerance.
