import sys
import copy
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from generate_device_catalog import get_source_snapshot
from update_catalog import content
from check_sources import checkout
from check_docs import anchors, frontmatter
from render_release import render, tutorial_requirements
import yaml


class DocumentationToolsTests(unittest.TestCase):
    def test_bundle_rejects_product_label_that_differs_from_installer(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'sources.json').read_text())
        changed = copy.deepcopy(manifest)
        changed['release']['version'] = '1.0'
        with self.assertRaisesRegex(ValueError, 'must match the stable installer'):
            render(changed)

    def test_bundle_manifest_rejects_a_moving_source_reference(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'sources.json').read_text())
        changed = copy.deepcopy(manifest)
        changed['sources']['spx-server']['commit'] = 'main'
        with self.assertRaises(ValueError):
            render(changed)

    def test_tutorial_pins_keep_the_released_client_prerelease(self):
        requirements = tutorial_requirements({'sources': {
            'spx-sdk': {'version': 'v1.0.0'},
            'spx-python': {'version': 'v1.0.0-rc.3'},
        }})
        self.assertIn('spx-sdk==1.0.0\n', requirements)
        self.assertIn('spx-python==1.0.0rc3\n', requirements)

    def test_missing_source_never_falls_back_to_head(self):
        with patch('generate_device_catalog.run_git', side_effect=subprocess.CalledProcessError(128, 'git')) as call:
            with self.assertRaises(subprocess.CalledProcessError):
                get_source_snapshot(Path('/missing'), 'bad-pin')
            self.assertEqual(call.call_count, 1)

    def test_catalog_metadata_does_not_trigger_an_update(self):
        old = 'Source snapshot: commit `' + 'a' * 40 + '` (old)\n[model](https://github.com/org/repo/blob/' + 'a' * 40 + '/sensor.yaml)\n'
        new = old.replace('a' * 40, 'b' * 40).replace('(old)', '(new)')
        self.assertEqual(content(old), content(new))
        self.assertNotEqual(content(old), content(new + 'new model\n'))

    def test_public_source_allowlist(self):
        with self.assertRaises(ValueError):
            checkout('/unused', {'repository': 'HammerHeads-Engineers/spx-installer', 'commit': 'a' * 40})
        with self.assertRaises(ValueError):
            checkout('/unused', {'repository': 'HammerHeads-Engineers/spx-examples', 'commit': 'main'})

    def test_gitbook_frontmatter_rejects_unquoted_colon(self):
        with self.assertRaises(yaml.YAMLError):
            frontmatter('---\ndescription: Read first: sources and modes\n---\n# Agent')
        self.assertEqual(frontmatter('---\ndescription: "Read first: sources and modes"\n---\n# Agent'),
                         {'description': 'Read first: sources and modes'})

    def test_duplicate_heading_anchors_and_code_fences(self):
        self.assertEqual(anchors('# Hello `world`\n# Hello world\n```md\n# Hidden\n```\n'), {'hello-world', 'hello-world-1'})
        self.assertEqual(anchors('## Before you start {#first-device-in-the-ui}\n'), {'first-device-in-the-ui'})


if __name__ == '__main__':
    unittest.main()
