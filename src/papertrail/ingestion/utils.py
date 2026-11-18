import hashlib
from pathlib import Path

def get_file_metadata(pdf_path: str | Path) -> dict:
    path = Path(pdf_path)
    sha256_hash = hashlib.sha256()
    
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
            
    return {
        "filename": path.name,
        "sha256": sha256_hash.hexdigest(),
        "size_bytes": path.stat().st_size
    }