from pathlib import Path
from typing import BinaryIO
import hashlib
import json


class HashManager:

    def __init__(self):
        self.hash_file = Path("data/indexed_files.json")

    def calculate_hash(self, file_source: Path | BinaryIO) -> str:
        sha256 = hashlib.sha256()

        if isinstance(file_source, Path):
            file = file_source.open("rb")
            should_close = True
        else:
            file = file_source
            should_close = False

        try:
            if not should_close:
                file.seek(0)
            while chunk := file.read(4096):
                sha256.update(chunk)
        finally:
            if should_close:
                file.close()
            else:
                file.seek(0)

        return sha256.hexdigest()

    def load_hashes(self) -> dict[str, str]:
        if not self.hash_file.exists():
            return {}

        with open(self.hash_file, "r") as file:
            return json.load(file)

    def save_hashes(self, hashes: dict[str, str]) -> None:
        with open(self.hash_file, "w") as file:
            json.dump(hashes, file, indent=4)