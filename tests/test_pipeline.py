"""Real English/Korean NLP, citation ranking, report and archive integration checks."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from openpyxl import load_workbook
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class PipelineTest(unittest.TestCase):
    def test_bilingual_reports_and_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            cfg = json.loads((ROOT / 'config.json').read_text())
            cfg.update(WORDCLOUD_WIDTH=480, WORDCLOUD_HEIGHT=320,
                       WORDCLOUD_MAX_WORDS=8, WORDCLOUD_MAX_FONT=50,
                       WORDCLOUD_MIN_FONT=12, WORDCLOUD_ATTEMPTS=80,
                       SAMPLE_SIZE=5)
            if os.environ.get('TEST_FONT_PATH'):
                cfg['WORDCLOUD_FONT_PATH'] = os.environ['TEST_FONT_PATH']
            config = tmp / 'config.json'
            config.write_text(json.dumps(cfg))
            for mode, count in [('sample', 5), ('full', 6)]:
                result = subprocess.run([
                    sys.executable, str(ROOT / 'run_analysis.py'),
                    str(ROOT / 'data/example.xlsx'), '--mode', mode,
                    '--config', str(config), '--output-dir', str(tmp / 'out'),
                    '--cache-dir', str(tmp / 'cache')],
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                out = tmp / 'out' / mode
                data = (out / 'paper_explorer_assets/data.js').read_text()
                payload = json.loads(data.split(' = ', 1)[1].strip().removesuffix(';'))
                self.assertEqual(len(payload['papers']), count)
                self.assertTrue(payload['terms'])
                self.assertTrue(any(t['language'] == 'KO' for t in payload['terms']))
                self.assertTrue(any(t['language'] == 'EN' for t in payload['terms']))
                self.assertTrue(any(t['score']['citation'] > t['score']['no_idf']
                                    for t in payload['terms']))
                self.assertEqual(set(payload['clouds']),
                                 {'no_idf', 'idf', 'citation', 'citation_idf'})
                for variants in payload['clouds'].values():
                    self.assertEqual(set(variants), {'diverse', 'orthogonal', 'horizontal'})
                self.assertTrue(any(p['citations'] is None for p in payload['papers']))
                self.assertTrue(payload['warnings'])  # missing citation is neutral, not zero
                with Image.open(out / 'wordcloud_citation.png') as png:
                    self.assertEqual(png.size, (480, 320))
                    png.verify()
                wb = load_workbook(out / 'analysis.xlsx', read_only=True)
                info = {r[0]: json.loads(r[1]) for r in
                        wb['실행정보'].iter_rows(min_row=2, values_only=True)}
                wb.close()
                self.assertTrue(info['complete'])
                self.assertEqual(info['error_count'], 0)
                if mode == 'full':
                    self.assertGreater(info['cache_hits'], 0)
                with zipfile.ZipFile(tmp / 'out' / f'v8_4_{mode}_results.zip') as z:
                    self.assertIsNone(z.testzip())
                    self.assertIn('paper_explorer_assets/images.js', z.namelist())
                    self.assertIn('paper_explorer.html', z.namelist())
            # Reusing output must fail rather than packaging stale results.
            retry = subprocess.run([sys.executable, str(ROOT / 'run_analysis.py'),
                                    str(ROOT / 'data/example.xlsx'), '--mode', 'full',
                                    '--output-dir', str(tmp / 'out')], capture_output=True)
            self.assertNotEqual(retry.returncode, 0)


if __name__ == '__main__':
    unittest.main()
