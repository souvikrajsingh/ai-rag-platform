from pathlib import Path
import hashlib
import json


class HashManager:

    def __init__(self):
        self.hash_file = Path("data/indexed_files.json")

    def calculate_hash(self, file_path: Path) -> str:
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    def load_hashes(self) -> dict[str, str]:
        if not self.hash_file.exists():
            return {}

        with open(self.hash_file, "r") as file:
            return json.load(file)

    def save_hashes(self, hashes: dict[str, str]) -> None:
        with open(self.hash_file, "w") as file:
            json.dump(hashes, file, indent=4)