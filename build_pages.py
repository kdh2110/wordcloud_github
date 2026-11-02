"""Prepare the same successful analysis for GitHub Pages and direct downloads."""
import argparse
from pathlib import Path
import shutil

DOWNLOADS = '''<nav aria-label="분석 결과 다운로드" style="padding:16px 24px;background:#eef3f8;display:flex;gap:24px;flex-wrap:wrap">
  <a href="results.zip" download>전체 결과 ZIP 다운로드</a>
  <a href="analysis.xlsx" download>Excel 다운로드</a>
</nav>
'''


def build_site(output_root, mode, site_dir):
    output_root, site_dir = Path(output_root), Path(site_dir)
    out = output_root / mode
    files = ['analysis.xlsx', 'paper_explorer.html',
             'paper_explorer_assets/data.js', 'paper_explorer_assets/images.js']
    files += [f'wordcloud_{v}.png' for v in ('no_idf', 'idf', 'citation', 'citation_idf')]
    archive = output_root / f'v8_4_{mode}_results.zip'
    for path in [out / f for f in files] + [archive]:
        if not path.is_file():
            raise FileNotFoundError(f'필수 분석 결과가 없습니다: {path}')
    source = (out / 'paper_explorer.html').read_text(encoding='utf-8')
    if source.count('<main>') != 1:
        raise ValueError('분석 HTML에서 본문을 찾을 수 없습니다.')
    if site_dir.exists() and any(site_dir.iterdir()):
        raise ValueError(f'게시 폴더가 비어 있지 않습니다: {site_dir}')
    site_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
        target = site_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(out / name, target)
    shutil.copyfile(archive, site_dir / 'results.zip')
    (site_dir / 'index.html').write_text(
        source.replace('<main>', DOWNLOADS + '<main>', 1), encoding='utf-8')
    (site_dir / '.nojekyll').touch()
    return site_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', type=Path, default=Path('output'))
    parser.add_argument('--mode', choices=['sample', 'full'], required=True)
    parser.add_argument('--site-dir', type=Path, default=Path('site'))
    args = parser.parse_args()
    print(f'Pages 게시 파일 준비 완료: {build_site(args.output_root, args.mode, args.site_dir)}')


if __name__ == '__main__':
    main()
