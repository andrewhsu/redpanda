#!/usr/bin/env python3
import json
import lint_body
import unittest


class LintPRBodyTestCase(unittest.TestCase):
    def test_lint_pr_body(self):
        cases = {
            'test00-old-default.json': ['B01', 'B02', 'B03'],
            'test01-new-default.json': ['B01', 'B02', 'B03'],
            'test02-empty.json': ['B01', 'B02', 'B03'],
            'test03-old-backport.json': ['B01', 'B02', 'B03'],
            'test04-new-backport.json': ['B01', 'B02', 'B03'],
            'test05-old-feature.json': ['B01', 'B02', 'B03'],
            'test06-new-feature.json': ['B01', 'B02', 'B03'],
            'test07-bug-fix.json': []
        }

        for file, expected in cases.items():
            with self.subTest(file):
                j = {}
                with open(file) as f:
                    j = json.load(f)
                actual = lint_body.lint_pr_body(j)
                self.assertEqual(set(expected), set(actual),
                                 'unexpected error codes')


if __name__ == '__main__':
    unittest.main()
