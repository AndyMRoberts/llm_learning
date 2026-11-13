"""Central settings. (Given – no TODOs.) Change values here when experimenting."""
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
CHROMA_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "agronomy_naive"

# Embedding model. bge-small is fast on CPU (384 dims) and strong for its size.
# NOTE: BGE models recommend prefixing *queries* (not documents) with QUERY_PREFIX.
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# Chunking (measured in CHARACTERS for simplicity; ~4 chars ≈ 1 token)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Retrieval
TOP_K = 4
MIN_SCORE = 0.6

# Generation (Ollama model tag)
LLM_MODEL = "qwen3:8B"
