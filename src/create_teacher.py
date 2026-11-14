"""Provision teacher accounts for the Mergington activities application."""

import getpass
import hashlib
import json
import secrets
import sys
from pathlib import Path

PBKDF2_ITERATIONS = 600_000
TEACHERS_FILE = Path(__file__).with_name("teachers.json")


def add_teacher(
    username: str,
    password: str,
    password_confirmation: str,
    credentials_path: Path = TEACHERS_FILE,
) -> None:
    username = username.strip()
    if not username:
        raise ValueError("Username cannot be empty")
    if not password:
        raise ValueError("Password cannot be empty")
    if password != password_confirmation:
        raise ValueError("Passwords do not match")

    credentials = json.loads(credentials_path.read_text(encoding="utf-8"))
    if not isinstance(credentials, dict):
        raise ValueError("teachers.json must contain a JSON object")
    if username in credentials:
        raise ValueError(f"Teacher {username!r} already exists")

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    credentials[username] = {
        "salt": salt.hex(),
        "password_hash": password_hash.hex(),
    }
    credentials_path.write_text(
        json.dumps(credentials, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    username = input("Teacher username: ")
    password = getpass.getpass("Teacher password: ")
    password_confirmation = getpass.getpass("Confirm password: ")
    try:
        add_teacher(username, password, password_confirmation)
    except (OSError, ValueError) as error:
        print(f"Unable to add teacher: {error}", file=sys.stderr)
        return 1

    print(f"Teacher {username.strip()!r} added to {TEACHERS_FILE}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
