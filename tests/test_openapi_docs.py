import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from render_openapi_docs import (API_TITLE, API_DESCRIPTION, HTTP_METHODS,
                                 documented_spec, render_models)

ROOT = Path(__file__).resolve().parents[1]


class OpenAPIPresentation(unittest.TestCase):
    def test_presentation_metadata_preserves_released_contract_and_input(self):
        source = json.loads((ROOT / 'api-v3-reference/openapi.json').read_text())
        source.pop('tags', None)
        for path in source['paths'].values():
            for method, op in path.items():
                if method in HTTP_METHODS:
                    op.pop('tags', None)
        before = json.dumps(source, sort_keys=True)
        result = documented_spec(source)
        self.assertEqual(json.dumps(source, sort_keys=True), before)
        self.assertEqual(result.pop('tags'), [{'name': API_TITLE, 'x-page-description': API_DESCRIPTION}])
        for path in result['paths'].values():
            for method, op in path.items():
                if method in HTTP_METHODS:
                    self.assertEqual(op.pop('tags'), [API_TITLE])
        self.assertEqual(result, source)

    def test_presentation_is_idempotent_and_does_not_replace_other_tags(self):
        sample = {'paths': {'/health': {'get': {'summary': 'Health'}}}}
        once = documented_spec(sample)
        self.assertEqual(documented_spec(once), once)
        sample['paths']['/health']['get']['tags'] = ['another-page']
        with self.assertRaises(ValueError):
            documented_spec(sample)

    def test_schema_wrapper_has_exact_schema_coverage_and_existing_spec_identity(self):
        spec = json.loads((ROOT / 'api-v3-reference/openapi.json').read_text())
        page = render_models(spec)
        self.assertEqual(page.count('{% openapi-schemas'), len(spec['components']['schemas']))
        for name in spec['components']['schemas']:
            self.assertIn(f'spec="hammerheadsengineers-api" schemas="{name}"', page)
        self.assertIn('description:', page)
        self.assertIn('not device definitions', page)


if __name__ == '__main__':
    unittest.main()
