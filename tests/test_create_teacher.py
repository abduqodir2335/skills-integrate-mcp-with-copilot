import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.create_teacher import PBKDF2_ITERATIONS, add_teacher


class AddTeacherTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.credentials_path = Path(self.temp_dir.name) / "teachers.json"
        self.credentials_path.write_text("{}", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_adds_salted_hash_without_storing_password(self):
        add_teacher(
            "  teacher  ", "correct horse battery staple",
            "correct horse battery staple", self.credentials_path
        )

        contents = self.credentials_path.read_text(encoding="utf-8")
        credential = json.loads(contents)["teacher"]
        self.assertNotIn("correct horse battery staple", contents)
        self.assertEqual(len(bytes.fromhex(credential["salt"])), 16)
        self.assertEqual(
            hashlib.pbkdf2_hmac(
                "sha256",
                b"correct horse battery staple",
                bytes.fromhex(credential["salt"]),
                PBKDF2_ITERATIONS,
            ).hex(),
            credential["password_hash"],
        )

    def test_rejects_mismatched_confirmation_without_changing_file(self):
        original = self.credentials_path.read_text(encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Passwords do not match"):
            add_teacher("teacher", "secret", "different", self.credentials_path)

        self.assertEqual(self.credentials_path.read_text(encoding="utf-8"), original)

    def test_rejects_duplicate_username(self):
        add_teacher("teacher", "secret", "secret", self.credentials_path)
        original = self.credentials_path.read_text(encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "already exists"):
            add_teacher("teacher", "another secret", "another secret", self.credentials_path)

        self.assertEqual(self.credentials_path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
