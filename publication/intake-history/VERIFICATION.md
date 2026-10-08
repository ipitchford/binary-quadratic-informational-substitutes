# Verification record

**The exact checks passed. The universal theorem has a complete informal analytic proof and has not been formalised in a proof assistant.** A separate AI-agent referee independently reconstructed the proof and wrote an implementation before inspecting the submitted classifier. The final reviewed manuscript has no unresolved mathematical or reproducibility blocker within that stated review scope.

## What establishes the unrestricted claim

Theorem 2 in manuscript Section 3 derives the gap for every admissible measurable disclosure from conditional expectation. The reciprocal identity in Section 3.2 writes its residual as endpoint margins plus nonnegative square terms. Section 3.3 constructs a violating disclosure from either negative endpoint. Applying this oriented equivalence twice proves Theorem 1 for every real joint table, with all support cases included.

The proof uses neither a finite table search nor a numerical approximation to establish its universal quantifier. The finite checks below inspect the algebra, the implementation, boundary handling and concrete consequences of that proof.

## Verification layers and completed results

| Layer | Result | What the evidence establishes |
|---|---|---|
| Exact definition audit | Passed | Matches Chen–Waggoner (2017), Definition 2.2.3, including its subset/continuous-lattice quantifiers and the independent-randomisation interpretation. |
| Three mathematical derivations and separate referee | Passed after corrections | Conditional-variance identity, necessity, sufficiency, null cells, equality, real/vector target extension, additive/independence corollaries and complements appendix were reconstructed and challenged. This is AI-agent review, not external human peer review. |
| Symbolic polynomial identities | Passed | Exact integer-polynomial expansion: reciprocal residual 0 terms; quartic residual 8 terms before row reduction and 0 after using c_i²=v_i h_i. |
| Primary finite audit | Passed | All 6,560 nonzero count vectors in {0,1,2}^8, all 255 support masks, 13,120 orientations; 3,884 accepted directions, 9,236 rejected directions. |
| Accepted-direction direct calculations | Passed | 62,144 binary-kernel score comparisons, evaluated directly from event masses, with nonnegative gaps. |
| Rejected-direction certificates | Passed | All 9,236 rational witnesses have strictly negative direct gaps. The complete corpus is `results/exhaustive_witnesses.jsonl`. |
| Independent implementation | Passed | 65,600 direct channel comparisons, 64,000 posterior identities, 12,800 polynomial decisions, 3,564 operational strictness checks, 2,025 additive-posterior cases and 2,304 independent-source cases. |
| One-direction finite-alphabet extension | Passed | 105 finite cases; 1,785 raw-score comparisons; 90 negative witnesses; two to four event outcomes and three to seven outcomes of the second signal. |
| Complements implementation | Passed | 15,250 exact raw-score/quadratic comparisons; 174 positive failure witnesses, including 132 interior-vertex constructions. |
| Referee comparison of released implementations | Passed | All 13,120 oriented classifications agree with independently computed parameters; all 9,236 returned substitute witnesses and 3,616 returned complement witnesses have the required sign under the referee's own raw-mass scorer. |
| Fresh package replay | Passed | Five programs exited 0; seven stable result records matched; the full exact witness corpus reproduced byte-for-byte. Elapsed time 52.109 seconds. |
| PDF rendering | Passed | Eleven A4 pages rendered; visual review of all pages and full-resolution inspection of the central proof and examples found no clipping, missing equations or broken table rows. |

The count-vector domain contains duplicate normalised distributions. It covers every event-table support mask but is not an estimate of how frequently substitutes occur among all distributions. The independent programs use Python `fractions.Fraction`; no floating-point mathematical decisions or external solvers are involved.

## Commands, environment and records

The main replay command was:

```sh
python output/evidence_press_binary_quadratic_v1_0_0/code/run_all.py --out research/package_replay
```

Working directory: `/workspace/scratch/28ef880bbcda`. Interpreter: CPython 3.12.14 on Linux. The replay script copied the delivered code into an isolated temporary directory and preserved the original result files. Its ordered subprocesses were:

1. `python polynomial_certificate.py` — exit 0, 0.032 seconds.
2. `python audit_checks.py` — exit 0, 4.737 seconds.
3. `python audit_exhaustive.py` — exit 0, 26.693 seconds.
4. `python independent_checks.py` — exit 0, 16.219 seconds.
5. `python complements_checks.py` — exit 0, 4.412 seconds.

Timing is descriptive and hardware dependent. The exact logs and fresh receipt are in `results/fresh_replay/`. Frozen primary records are in `results/`. The referee's separate commands, preserved source identities, cross-check code and replay logs are in `audit/referee/`.

The final PDF was generated from the Markdown source using ReportLab and Matplotlib. Display equations use vector glyphs; inline equations are embedded at 600 dpi. The plotted curve is the declared exact rational residual evaluated for display. Its marked rational values were checked directly. Image generation was not used for mathematical content.

## Resolved defects

- An early optional covariance formula incorrectly used a minus sign on `2*c1*w` in `K1`. Exact polynomial expansion caught the error. The corrected plus sign was independently derived from `K1=-N'(1)` and tested on a positive example. The core contrast proof did not depend on the faulty intermediate expression.
- The numerical XOR margins initially lacked the qualification that the independent input bits are fair. The referee supplied biased-input checks; the final text states the fair-bit condition.
- The abstract now explicitly restricts its rational-witness statement to rational input. The score-normalisation wording states the exact additive constant for negative Brier loss.
- The ancillary factorisation now specifies the coefficient of `q^4`, avoiding a false leading-coefficient statement when `w=0`.
- The prior-art query count was calculated from the delivered log: **67 queries in five families**. An earlier progress estimate was not used as evidence.

No unresolved mathematical correction remains for the selected target. A future change to a proof statement, formula or implementation requires review against the frozen hashes.

## Novelty, missingness and scope

The source-search boundary and formula translations are recorded in `audit/prior_art/`. No equivalent four-test or binary-source weighted-contrast criterion was found among the inspected sources and recorded searches. That negative search evidence cannot establish historical priority. General scoring-rule geometry, posterior splitting and small disclosure-alphabet reductions receive explicit prior-work credit.

There is no empirical dataset, treatment effect or estimated forecast model in this package. The eight probabilities are mathematical inputs. Null cells are handled by support overlap; no posterior is imputed to a missing cell. Full-support positive margins are locally robust by continuity, but the paper does not supply statistical confidence regions for probabilities estimated from data.

The result does not settle arbitrary proper scoring rules, arbitrarily many base signals, full continuous-lattice submodularity, or both directions when one source has more than two outcomes. The real/vector target generalisation still keeps the garbled source binary. Operational strictness concerns retained uncertainty about that source, not removal of irrelevant random coordinates from the formal lattice.

## Delivery integrity

`MANIFEST.json` records the size and SHA-256 hash of each substantive delivered file. It excludes itself and `SHA256SUMS` to avoid circular hashing. `code/check_integrity.py` checks every listed file. The final ZIP was tested for archive integrity, and the standalone PDF is byte-identical to the PDF inside the package. Hashes establish byte identity; they do not establish mathematical truth.

## Concrete sanity check

For the full-support separation table, the event-zero integer masses `(21,15,5,39)` and event-one masses `(27,1,11,9)` sum to 128. Direct scores give a whole-signal margin of `1/1024`. The disclosure that always sends the mixed report when B=0 and sends it with probability 1/3 when B=1 gives the exact gap `-11/10240`. Independent scoring reproduces the reversal without any numerical tolerance.
