# AI index: binary quadratic informational substitutes

## Start here
[README](README.md), [paper source](manuscript/binary-quadratic-informational-substitutes.md), [PDF](manuscript/binary-quadratic-informational-substitutes.pdf), [claims](CLAIMS.json), [assurance](ASSURANCE.md), [review response](REVIEW_RESPONSE.md).

## Exact scope and dependencies
Binary event and two binary sources, a fixed quadratic score, arbitrary joint probabilities including zero cells; Chen–Waggoner March 2017 Definition 2.2.3. The finite-second-source extension is only oriented. Not arbitrary scoring rules, arbitrary pairs of partial disclosures or empirical forecasts. Read [citation comparison](CITATION_AUDIT.md) before interpreting novelty.

## Claims to evidence
T1: manuscript Sections 2–3, four endpoint margins in [classifier](code/exact_checker.py). T2: conditional-variance argument and [finite-alphabet audit](code/finite_alphabet_audit.py). Failure witnesses: raw-score computation in classifier and [recorded corpus](results/exhaustive_witnesses.jsonl). Complements: Appendix A and [complements](code/complements.py). Reviewer-derived Proposition 4: Section 7.2 and [revision checks](code/revision_checks.py), including 32 projective comparisons. Equality/strictness and additive-posterior cases: [separate implementation](code/independent_checks.py). Finite counts do not prove universal claims.

## Replay
From the package root: `python3 code/check_integrity.py`; `python3 code/run_all.py --out /tmp/binary-replay-NEW`; `python3 -O code/run_all.py --out /tmp/binary-optimized-NEW`; `python3 -O code/revision_checks.py`. Choose fresh absent output paths. Standard library only for checking. The runner forwards optimisation to children. [Environment](ENVIRONMENT.txt), [verification](VERIFICATION.md), [current gates](RESEARCH_GATES.json), [manifest](MANIFEST.json). Historical intake records under publication/intake-history are not current status.

## Limits and rights
Written proof, not proof-assistant formalisation. Internal checks and supplied AI-assisted review do not establish external independence. Bounded search does not establish priority. Exact rational executable; real-input theorem is broader than machine representations. [Licences and provenance](LICENSES.md). Scholarly attribution Anonymous, DOI 10.5281/zenodo.23238557.
