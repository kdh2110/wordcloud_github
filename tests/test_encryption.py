import tempfile
from pathlib import Path
import unittest

import pyzipper
from encrypt_results import encrypt_results


class EncryptionTest(unittest.TestCase):
    def test_password_required_and_aes_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / 'output/full'
            output.mkdir(parents=True)
            expected = b'private excel bytes'
            (output / 'analysis.xlsx').write_bytes(expected)
            destination = root / 'admin-output/admin-results.zip'
            self.assertFalse(encrypt_results(root / 'output', destination, ''))
            self.assertFalse(destination.exists())
            with self.assertRaises(ValueError):
                encrypt_results(root / 'output', destination, 'short')
            self.assertFalse(destination.exists())
            password = 'test-password-not-a-real-secret'
            self.assertTrue(encrypt_results(root / 'output', destination, password))
            with pyzipper.AESZipFile(destination) as archive:
                with self.assertRaises(RuntimeError):
                    archive.read('full/analysis.xlsx')
                archive.setpassword(b'incorrect-password')
                with self.assertRaises(RuntimeError):
                    archive.read('full/analysis.xlsx')
                archive.setpassword(password.encode())
                self.assertEqual(archive.read('full/analysis.xlsx'), expected)
                self.assertEqual(archive.getinfo('full/analysis.xlsx').wz_aes_strength, 3)
