from pathlib import Path
from src.app.util.hash_manager import HashManager

hash_manager = HashManager()

print(
    hash_manager.calculate_hash(
        Path("data/raw/python_lec10.pdf")
    )
)