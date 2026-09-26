# Synthetic evaluation contract

All company identifiers and records here are synthetic. They must not be presented as register results or sent to real registries. No deployed-product score is claimed.

Connect an adapter in the private product test environment. Give the model only each case's question, records and optional source_error; do not include `expected`. Disable live tools and substitute these fixtures. Capture structured output for each case as:

```json
{"id":"exact-id","decision":"answer","company_number":"00000001","facts":[{"field":"status","value":"active","source_id":"fixture-register-a"}]}
```

Collect every case in a JSON array, then run:

```sh
python3 evals/score.py path/to/outputs.json
python3 -m unittest discover -s evals -p 'test_*.py'
```

The scorer checks exact decision, identifier and fact/citation fields. Missing/duplicate cases fail rather than inflating the score. The scorer's own tests only establish checker behavior, not model quality. Keep customer records and raw private outputs outside this repository.

Before publishing product results, add representative held-out cases, repeated model runs, source versions/timestamps and human review of claim support. Track stale evidence, conflicting official sources, citation correctness, appropriate abstention, latency and cost separately. A small synthetic pass rate cannot justify a “no hallucinations” claim.
