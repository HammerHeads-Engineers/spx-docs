import sys
from pathlib import Path
import unittest
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_navigation import entries, navigation_errors, metadata_errors
from check_published import normalize, at_site, index_routes

ROOT = Path(__file__).resolve().parents[1]


class NavigationContracts(unittest.TestCase):
    def test_gitbook_link_titles_preserve_navigation_and_source_paths(self):
        summary = '* [SPX Documentation](README.md "Start here")\n'
        self.assertEqual(entries(summary), [(0, 'Start here', 'README.md')])
        self.assertEqual(entries(summary, page_titles=True), [(0, 'SPX Documentation', 'README.md')])
        for label in ['SPX Documentation', 'Start here']:
            index = (f'- [{label}](https://docs.simplephysx.com/readme.md)\n'
                     '- [SPX Server API](https://docs.simplephysx.com/api/spx-server-api.md)\n'
                     '- [Models](https://docs.simplephysx.com/api/models.md)\n')
            _, routes = index_routes(index, summary, 'https://docs.simplephysx.com')
            self.assertEqual(routes['README.md']['url'], 'https://docs.simplephysx.com/')

    def test_published_pages_have_search_descriptions(self):
        summary = (ROOT / 'SUMMARY.md').read_text()
        self.assertEqual(metadata_errors(summary), [])

    def test_metadata_check_uses_navigation_and_rejects_missing_or_nontext_descriptions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'hidden.md').write_text('# Maintainer notes\n', encoding='utf-8')
            summary = '* [Visible](visible.md)\n'
            for text in ['# Visible\n', '---\ndescription: 12\n---\n# Visible\n', '---\ndescription: " "\n---\n# Visible\n']:
                (root / 'visible.md').write_text(text, encoding='utf-8')
                self.assertEqual(metadata_errors(summary, root), ['Published page needs a description: visible.md'])
            (root / 'visible.md').write_text('---\ndescription: Configure a device.\n---\n# Visible\n', encoding='utf-8')
            self.assertEqual(metadata_errors(summary, root), [])

    def test_user_navigation_has_one_place_per_page(self):
        summary = (ROOT / 'SUMMARY.md').read_text()
        self.assertEqual(navigation_errors(summary), [])
        duplicate = summary + '\n  * [Duplicate](README.md)\n'
        self.assertIn('Each source page must have one navigation location', navigation_errors(duplicate))

    def test_preview_route_normalization_preserves_markdown_and_legacy_root(self):
        preview = 'https://docs.simplephysx.com/~/revisions/reviewed'
        self.assertEqual(normalize(preview + '/readme', preview), '/')
        self.assertEqual(normalize(preview, preview), '/')
        self.assertEqual(normalize(preview + '/.md', preview), '/readme.md')
        self.assertEqual(at_site(preview, preview), preview)
        self.assertEqual(normalize(preview + '/reference/model.md', preview), '/reference/model.md')
        self.assertEqual(at_site(preview + '/reference/model.md', preview), preview + '/reference/model.md')

    def test_migration_map_requires_an_unambiguous_published_successor(self):
        index = ('- [Demo](https://docs.simplephysx.com/demo.md)\n'
                 '- [SPX Server API](https://docs.simplephysx.com/api/spx-server-api.md)\n'
                 '- [Models](https://docs.simplephysx.com/api/models.md)\n')
        _, routes = index_routes(index, '* [Demo](demo.md)\n', 'https://docs.simplephysx.com')
        self.assertEqual(routes['demo.md']['url'], 'https://docs.simplephysx.com/demo')
        self.assertIn('openapi:Models', routes)
        with self.assertRaises(ValueError):
            index_routes(index + '- [Demo](https://docs.simplephysx.com/duplicate.md)\n',
                         '* [Demo](demo.md)\n', 'https://docs.simplephysx.com')

    def test_technical_and_maintainer_trees_cannot_take_over_main_navigation(self):
        summary = (ROOT / 'SUMMARY.md').read_text()
        broken = summary.replace('* [Models & packs]', '* [SPX-SDK]', 1)
        self.assertIn('Expected seven task sections in the agreed order', navigation_errors(broken))
        deep = summary + '\n      * [Deep API](reference/deep.md)\n'
        self.assertIn('Navigation exceeds two levels below a section', navigation_errors(deep))


if __name__ == '__main__':
    unittest.main()
