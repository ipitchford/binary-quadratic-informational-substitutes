# Four tests for binary informational substitutes

Version 1.1.0 · 8 October 2026 · Unrefereed Evidence Press candidate

## Result

The manuscript gives a complete necessary-and-sufficient classification of strong informational substitutes for **a binary event and two binary signals under quadratic scoring**, for every joint distribution, including zero cells. Each orientation requires two weighted-square inequalities. Four tests decide the full property. Any failed test on rational input yields an explicit rational disclosure and an independently computed negative expected-score gap.

The exact definition is Chen and Waggoner (2017), Definition 2.2.3. One signal is partially disclosed, and the other is observed whole; the comparison is against full revelation of the first signal. The broader programme for arbitrary scoring rules, arbitrarily many signals, or arbitrary pairs of partial disclosures is not claimed solved.

An appendix also supplies a complete strong-complements test for the same binary model. The main proof generalises in one direction to a binary source and a finite second signal, and to square-integrable real or finite-dimensional vector targets under quadratic loss.

## Read first

- `manuscript/binary-quadratic-informational-substitutes.pdf`: complete revised paper (final page count in publication/qa.json).
- `manuscript/binary-quadratic-informational-substitutes.md`: editable mathematical source.
- `RELEASE_DRAFT.md`: public-facing release draft and specialist summary.
- `VERIFICATION.md`: exact checks, assurance boundaries, resolved defects and final replay status.
- `CLAIMS.json`: claim-by-claim proof and verification map.
- `RESEARCH_GATES.json`: machine-readable scope and completion status.
- `audit/referee/release_review.md`: historical AI-assisted review; identity and external independence not established.
- `audit/prior_art/prior_art_report.md`: inspected-source audit and bounded novelty finding.

No theorem here depends on a solver returning UNSAT or on a numerical tolerance. The unrestricted result is an informal analytic proof; the exact programs provide algebraic and finite verification evidence. No proof-assistant formalisation or external human peer review is claimed. Version DOI: https://doi.org/10.5281/zenodo.23238557.

## Run a decision

The decision tools use **exact rational inputs and the Python standard library only** (tested environments are recorded in ENVIRONMENT.txt). They do not require an optimiser, SymPy, NumPy or network access.

From this package's root:

```sh
python3 code/exact_checker.py examples/weak_not_strong.json
python3 code/complements.py examples/weak_not_strong.json
```

The first command prints the four exact margins, the whole-signal margin and a directly verified disclosure for each failed substitutes direction. The second prints endpoint/vertex certificates and directly verified disclosures for complement failures. The witnesses need not equal the hand-selected short witness in the paper: every returned witness is valid and carries its exact gap.

The executable labels are mapped as follows.

| Paper | Code | Meaning |
|---|---|---|
| `E` | `E` | Binary event |
| `A` | `X` | First binary source |
| `B` | `Y` | Second binary source |
| `T` | `Z` | Randomised disclosure |

An input JSON object contains `probabilities`, an array of eight nonnegative integers or rational strings summing to one. The order is lexicographic **(E,X,Y)**:

```json
{
  "probabilities": [
    "21/128", "15/128", "5/128", "39/128",
    "27/128", "1/128", "11/128", "9/128"
  ]
}
```

The first four entries have `E=0`; the next four have `E=1`. Floating-point inputs are rejected so that a tolerance cannot silently change the answer. With arbitrary real input, the theorem is still exact; a computation needs exact input representations or certified bounds on the margins.

`directions.X.margins[0]` uses the conditional weights from source row 0, and `margins[1]` uses row 1. The residual's endpoint values have the reverse order: H(0) is row-margin 1 and H(1) is row-margin 0. A source with a zero-probability outcome bypasses those undefined conditionals.

## Replay the verification

```sh
python3 code/check_integrity.py
python3 code/run_all.py --out replay
```

`run_all.py` copies the check code into an isolated temporary directory, runs all declared checks, compares stable result fields with the frozen records and writes fresh results and logs to `replay/`. It leaves the original recorded evidence unchanged. It needs no network access. The observed fresh replay took less than one minute in the provided environment; runtime depends on hardware.

The replay covers:

- Exact integer-polynomial expansion of the reciprocal identity and the alternative quartic identity, with zero residuals.
- All 6,560 nonzero count vectors in `{0,1,2}^8`, normalised to probability tables, covering all 255 nonempty event-table support patterns. Duplicate normalised tables are retained; this is not a prevalence sample.
- 62,144 direct kernel comparisons on accepted orientations and 9,236 explicit negative witnesses on rejected orientations.
- A separate implementation, with no import of the main classifier, checking 65,600 direct channel comparisons, 64,000 posterior identities, support degeneracies, strictness, 2,025 additive-posterior examples and 2,304 independent-source examples.
- 105 one-direction finite-alphabet cases, 1,785 direct comparisons and 90 negative witnesses.
- A complements audit with 15,250 direct comparisons and 174 positive witnesses, including interior-vertex failures.

The supplied referee report additionally cross-checked every output direction and every returned failure witness on the 6,560-table grid: 9,236 substitute witnesses and 3,616 complement witnesses. These numbers count oriented claims, not distinct probability models.

## Rebuild the manuscript

The delivered PDF is ready to read. Rebuilding it requires `reportlab`, `matplotlib` and `numpy`; these are presentation dependencies, not checker dependencies.

```sh
python3 code/build_pdf.py
```

This rebuilds the manuscript PDF and the analytical figure from the Markdown source. Display equations use vector glyphs; inline equations are rendered at 600 dpi. The figure evaluates the paper's stated rational function, with no fitted data. PDF metadata and library versions can change PDF bytes across rebuilds, so a rebuilt PDF need not match the distributed PDF hash. The mathematical source and exact checks are separately hashed.

## Prior work and scope

The formulation follows [Chen and Waggoner (2017)](https://arxiv.org/abs/1703.08636). The generic disclosure-alphabet reduction follows [Kong and Schoenebeck (2018)](https://doi.org/10.4230/LIPIcs.ITCS.2018.14), and posterior optimisation was developed in [Anunrojwong et al. (2019/2020)](https://arxiv.org/abs/2009.03607). These are credited as prior machinery.

The recorded search did not locate the present weighted-contrast endpoint criterion. That is a bounded finding, not proof of historical priority. No claim of a first-ever result is made. The package's findings concern exact specified distributions, with no empirical forecast data or estimated probability table.

## Integrity and provenance

`MANIFEST.json` and `SHA256SUMS` identify the delivered bytes. Their role is integrity, not proof of correctness. `audit/input_manifest.json` identifies the supplied shortlist and the inspected foundational source. Third-party full-text papers are not redistributed. The paper and code were developed with AI assistance, with separate mathematical derivations, an independent implementation and a supplied AI-assisted referee report whose identity and independence are not established. The audit records an early sign error in an optional polynomial formula and its correction before release; the main weighted-contrast theorem did not depend on that expression.

## Version 1.1.0 review actions

See [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md) for every adopted correction, [AI_INDEX.md](AI_INDEX.md) for the machine-readable route through claims and checks, and [ASSURANCE.md](ASSURANCE.md) for the evidence ceiling. The reviewer-derived strong/projective comparison is proved in Proposition 4 and checked directly in `code/revision_checks.py`. Original intake status files are preserved under `publication/intake-history/`; they are historical, not current publication status.
