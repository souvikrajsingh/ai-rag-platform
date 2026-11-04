from io import BytesIO
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.app.util.hash_manager import HashManager

hash_manager = HashManager()

print(hash_manager.calculate_hash(BytesIO(b"sample document content")))