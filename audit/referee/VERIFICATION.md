# Verification record

No proof-assistant verification was performed. The listed exact finite computations reproduced, and the unrestricted mathematical statement was examined by independent informal derivation.

## Scope and evidence boundary

Track: **I — Informal**, applying proof-digest and its informal, rubric, exposition, completion, and verification references. The work concerns the Chen–Waggoner (2017) Definition 2.2.3 strong-substitutes classification for a binary event and two binary sources under $V(X)=E[P(E=1\mid X)^2]$, its oriented finite-secondary-signal extension, the displayed structural consequences, and the ancillary binary complements classification.

The research notes, target statement, entire final Markdown manuscript, main exact classifier, ancillary complement classifier, three submitted replay scripts, submitted replay results, and exact example records were inspected. The source definition and relevant lattice passages were checked in the primary March 2017 PDF and its supplied text extraction. The plot of the weak-but-not-strong example was visually inspected and its marked values independently checked.

The initial notes-based mathematical report is `review.md`; the release-specific conclusion and final quality scores are in `release_review.md`. The argument's outline is `outline.md`. This report does not independently adjudicate the full novelty-search corpus, the later expanded enumeration scripts `audit_exhaustive.py` and `finite_alphabet_audit.py`, the PDF-building program, archive assembly, or external publication. The root package's separate records cover those activities.

## Preserved files and identity

`inspected_manifest.json` records the initial notes, target, foundational PDF/text, and supplied problem statement. The notes and target were copied under `inspected/`. `release_inspected_manifest.json` records the initially supplied full manuscript and submitted code/results. `final_manuscript_manifest.json` records the corrected manuscript hash and previous inspected hash. `release_code_identity.json` confirms that six released code copies are byte-identical to their reviewed sources.

Submitted scripts were inspected before being executed. Exact copies were placed under `reproduction/`, so scripts that write outputs alongside themselves wrote only inside the referee's assigned directory. All submitted originals were preserved. Hash agreement establishes the identity of bytes, not the truth of a mathematical statement or the provenance of its source.

## Reproduction and independent checks

All commands below ran with Python 3.12.14 and exact integer or `fractions.Fraction` arithmetic. No floating-point decision or tolerance is used. The executable reported by `sys.executable` was `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python`. Commands shown with `python` use that environment.

| Check | Exact command | Working directory | Result and evidence |
|---|---|---|---|
| Independent mathematical finite checks | `python research/referee/independent_checks.py` | `/workspace/scratch/28ef880bbcda` | **passed**, exit 0; `independent_results.json`; 16.904158 seconds inside program. |
| Submitted substitutes replay | `python audit_checks.py` | `/workspace/scratch/28ef880bbcda/research/referee/reproduction` | **passed**, exit 0; `reproduction/audit_checks.py.stdout.log`; 4.843186 seconds subprocess wall time. |
| Submitted complements replay | `python complements_checks.py` | `/workspace/scratch/28ef880bbcda/research/referee/reproduction` | **passed**, exit 0; `reproduction/complements_checks.py.stdout.log`; 4.114999 seconds. |
| Submitted exact polynomial expansion | `python polynomial_certificate.py` | `/workspace/scratch/28ef880bbcda/research/referee/reproduction` | **passed**, exit 0; `reproduction/polynomial_certificate.py.stdout.log`; 0.027017 seconds. |
| Independent comparison with submitted implementations | `python research/referee/release_checks.py` | `/workspace/scratch/28ef880bbcda` | **passed**, exit 0; `release_check_results.json`; 17.781884 seconds inside program. |
| Proof-assistant compilation and axiom audit | None | N/A | **not applicable**: no formal development supplied; no formal verification claimed. |
| Optional SymPy use | Two `import sympy` attempts | Workspace | **blocked**: module absent in both Python entry points; replaced by direct coefficient derivation and standard-library exact arithmetic. No dependencies installed. |

`reproduction/reproduction_results.json` records full command paths, working directory, subprocess exit status, elapsed time, and stdout/stderr file names for the three replayed scripts. Their stderr files are empty. Every non-timing field of the supplied replay results matched. Both `examples.json` and `complements_examples.json` reproduced byte-for-byte. The submitted first replay reported 4.095 seconds originally and 4.785 seconds in the referee run; only this timing field changed.

### Actual finite domains

The independent mathematical program enumerated all 6,560 nonzero count vectors in $\{0,1,2\}^8$, retaining duplicate normalized tables. They cover all 255 nonempty event-atom support masks. There were 12,800 nonconstant-source and 320 constant-source orientations, 65,600 direct channel comparisons across five kernels, and 64,000 posterior identity checks at $q=0,1/7,1/2,6/7,1$. It constructed and directly checked 9,236 negative rational witnesses. Additional grids comprised 2,025 additive-posterior structures and 2,304 independent-source structures.

The separate release-comparison program covered the same 6,560 input vectors and 13,120 orientations. It compared submitted classifications and coefficient values against independently written parameters. It recomputed all 9,236 returned substitute failure witnesses and all 3,616 returned complement failure witnesses using the referee's own direct event-mass score routine. Every score agreed exactly and had the required strict sign.

The submitted substitutes replay reproduced 255 uniform-support structures, 510 orientations, 12,750 binary-kernel comparisons, 48 multi-output comparisons, 212 constructed negative witnesses, and eight named examples. The submitted complements replay reproduced all 255 uniform-support structures and 50 weighted pseudorandom structures, with seed 20261008, 15,250 direct comparisons, 174 positive witnesses, and six named examples. Its classification counts and witness-construction counts matched exactly.

The polynomial script performs formal algebra in a hand-written eleven-variable integer polynomial representation, not numerical sampling. It produced zero terms for the reciprocal identity, eight terms in the raw quartic residual, and zero after substitutions using $c_0^2=v_0h_0$, $c_1^2=v_1h_1$. This is an exact computational algebra check under the inspected Python implementation; it is not a theorem-prover certificate of the probabilistic reduction.

## Mathematical checks and their independence

The referee separately derived the two conditional-variance losses, the measurable-disclosure reduction, the overlap restriction, the endpoint decomposition, both directions of necessity, the rational witness bounds, and all five source-support shapes. The score normalization, independent-source interaction condition, additive-posterior covariance-sign characterization, sufficient-source consequence, operational equality classification, and quantitative bounds were reconstructed from definitions.

The ancillary factorization was checked by a second route: $N(0)=N(1)=0$, $K_0=N'(0)$, $K_1=-N'(1)$, and the coefficient of $q^4$ is $w^2$. These facts determine the quadratic after factoring (q(1-q)). This derivation confirms the corrected plus sign on $2c_1w$ and remains valid when a row variance is zero. The complement endpoint/vertex test then follows by maximizing a concave quadratic and realizing a positive interior residual by a binary posterior split.

The independent finite program was written before importing or examining the submitted implementation and does not import it. The later release-comparison program deliberately imports preserved submitted copies to compare their outputs with the independently written event-mass evaluator. The submitted complement evaluator shares its direct-score function with the submitted substitutes code; the referee's direct score function supplies an additional independent implementation for witness checking.

## Claim/check ledger

The machine-readable ledger is `claim_check_ledger.csv`. It includes twenty claims or evidence obligations and explicitly identifies the priority review, archive assembly, later expanded replay scripts, and formal verification limits. The detailed mathematical reasoning is in `review.md`, with release-specific changes and blocker classification in `release_review.md`.

## Formal trust audit

Not applicable. There is no Lean, Rocq, Isabelle, or other proof-assistant artifact in the reviewed submission. No compiler output, theorem axiom set, kernel check, formal statement comparison, or native-evaluation trust claim exists. Python assertion success is reported only for the displayed finite scopes and algebraic computations.

## Changes and resolved findings

The referee did not modify the original notes, manuscript, source implementations, or release code. Corrections were sent to the root author. The earlier ancillary minus sign in $K_1$ was author-notified and independently confirmed. The missing fair-bit qualification in the XOR numerical example was found by this referee. Rational-input scope and Brier-normalization wording were clarified, and Appendix A gained an endpoint-derivative derivation. The phrase about the quartic's leading coefficient was tightened to specify its $q^4$ coefficient, preserving zero-degree branches.

## Remaining obligations and conclusion

No unresolved mathematical or implementation counterexample was identified for the final inspected claim. This is a bounded informal review, with preserved code and enumerated domains. It does not establish historical priority, certify the entire generated release archive, or provide external human peer review. Any later mathematical manuscript or implementation change must be assessed against the recorded hashes before this report is reused.

## Sanity checks

The whole-signal separation example has $W=1/1024$, yet its short two-report disclosure has directly computed gap $-11/10240$. The corrected covariance formula yields $K_1=27/1280$ on a positive substitute example, whereas the earlier minus sign yields $-33/1280$. Independent biased XOR with source probabilities $1/4,1/3$ gives oriented margins (-8/9,-3/4) and weak margin $-1/6$, confirming why the manuscript's values $-1,-1/4$ require fair bits.
