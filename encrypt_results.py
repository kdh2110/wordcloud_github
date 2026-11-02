"""Store analysis outputs only in a password-protected AES-256 ZIP."""
import argparse
import os
from pathlib import Path
import tempfile

import pyzipper


def encrypt_results(output_root, destination, password):
    output_root, destination = Path(output_root), Path(destination)
    if not password:
        print('::warning::RESULTS_PASSWORD Secret이 없어 관리자용 결과 업로드를 생략합니다.')
        return False
    if len(password) < 16:
        raise ValueError('RESULTS_PASSWORD는 16자 이상으로 설정하세요.')
    files = sorted(p for p in output_root.rglob('*') if p.is_file())
    if not files:
        print('업로드할 분석 결과가 없습니다.')
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, suffix='.tmp', delete=False) as f:
        temporary = Path(f.name)
    try:
        with pyzipper.AESZipFile(temporary, 'w', compression=pyzipper.ZIP_DEFLATED,
                                encryption=pyzipper.WZ_AES) as archive:
            archive.setpassword(password.encode('utf-8'))
            archive.setencryption(pyzipper.WZ_AES, nbits=256)
            for file in files:
                archive.write(file, file.relative_to(output_root).as_posix())
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    print('AES-256 관리자용 결과 생성 완료')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', type=Path, default=Path('output'))
    parser.add_argument('--destination', type=Path, default=Path('admin-output/admin-results.zip'))
    args = parser.parse_args()
    encrypt_results(args.output_root, args.destination, os.environ.get('RESULTS_PASSWORD', ''))


if __name__ == '__main__':
    main()
