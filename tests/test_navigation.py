import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_navigation import navigation_errors

ROOT = Path(__file__).resolve().parents[1]


class NavigationContracts(unittest.TestCase):
    def test_user_navigation_has_one_place_per_page(self):
        summary = (ROOT / 'SUMMARY.md').read_text()
        self.assertEqual(navigation_errors(summary), [])
        duplicate = summary + '\n  * [Duplicate](README.md)\n'
        self.assertIn('Each source page must have one navigation location', navigation_errors(duplicate))

    def test_technical_and_maintainer_trees_cannot_take_over_main_navigation(self):
        summary = (ROOT / 'SUMMARY.md').read_text()
        broken = summary.replace('* [Guides]', '* [SPX-SDK]', 1)
        self.assertIn('Expected seven task sections in the agreed order', navigation_errors(broken))
        deep = summary + '\n      * [Deep API](reference/deep.md)\n'
        self.assertIn('Navigation exceeds two levels below a section', navigation_errors(deep))


if __name__ == '__main__':
    unittest.main()
