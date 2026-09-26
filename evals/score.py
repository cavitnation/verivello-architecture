"""Score a synthetic structured-output contract; not production factuality."""
import json
from pathlib import Path
import sys

def score(cases, outputs):
    expected_ids = {case['id'] for case in cases}
    ids = [output.get('id') for output in outputs]
    if len(ids) != len(set(ids)) or set(ids) != expected_ids:
        raise ValueError('Outputs must contain every case exactly once and no unknown IDs.')
    by_id = {output['id']: output for output in outputs}
    results = []
    for case in cases:
        actual = by_id[case['id']]
        expected = case['expected']
        passed = all(actual.get(key) == expected[key] for key in ['decision', 'company_number', 'facts'])
        results.append({'id': case['id'], 'passed': passed})
    return {'scope': 'synthetic structured-output contract only', 'passed': sum(r['passed'] for r in results), 'total': len(results), 'cases': results}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 evals/score.py path/to/private-adapter-outputs.json')
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    report = score(cases, json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] == report['total'] else 1)
