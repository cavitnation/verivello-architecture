import copy
import json
from pathlib import Path
import unittest
from score import score

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(Path(__file__).with_name('cases.json').read_text())
        self.outputs = [{'id': c['id'], **copy.deepcopy(c['expected'])} for c in self.cases]

    def test_expected_contract(self):
        self.assertEqual(score(self.cases, self.outputs)['passed'], len(self.cases))

    def test_wrong_fact_or_citation_fails(self):
        self.outputs[0]['facts'][0]['value'] = 'dissolved'
        self.assertEqual(score(self.cases, self.outputs)['passed'], len(self.cases)-1)
        self.outputs[0]['facts'][0]['value'] = 'active'
        self.outputs[0]['facts'][0]['source_id'] = 'invented-source'
        self.assertEqual(score(self.cases, self.outputs)['passed'], len(self.cases)-1)

    def test_missing_or_duplicate_case_fails(self):
        with self.assertRaises(ValueError): score(self.cases, self.outputs[:-1])
        with self.assertRaises(ValueError): score(self.cases, self.outputs+[self.outputs[0]])

if __name__ == '__main__': unittest.main()
