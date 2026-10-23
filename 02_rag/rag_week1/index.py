"""
STEP 2 – INDEX: chunks -> embedding vectors -> vector database (ChromaDB, on disk)
"""
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL

_model = None  # cache so we load the model once per process


def get_embedder() -> SentenceTransformer:
    """
    TODO 2.1: lazily load SentenceTransformer(EMBED_MODEL) into the global `_model`
              and return it. (First run downloads the model – needs internet once.)
    """
    raise NotImplementedError


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Return one vector (list of floats) per text.

    TODO 2.2: call get_embedder().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    TODO 2.3: convert numpy array to a plain list (HINT: .tolist()) – Chroma wants lists.

    WHY normalize? With unit-length vectors, cosine similarity == dot product, and
    it makes scores comparable across queries.
    HINT: Do NOT add QUERY_PREFIX here – only queries get it (see retrieve.py).
    """
    raise NotImplementedError


def get_collection(reset: bool = False):
    """
    Open (or recreate) the persistent Chroma collection.

    TODO 2.4: client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    TODO 2.5: if reset: try client.delete_collection(COLLECTION_NAME) (ignore if missing).
    TODO 2.6: return client.get_or_create_collection(
                  name=COLLECTION_NAME,
                  metadata={"hnsw:space": "cosine"})   # makes distance = 1 - cosine_similarity

    HINT: Forgetting the "hnsw:space" metadata gives you L2 distance by default –
          scores would then mean something different. Know which one you're using!
    """
    raise NotImplementedError


def build_index(chunks: list[dict], batch_size: int = 64) -> None:
    """
    Embed all chunks and add them to Chroma.

    TODO 2.7: collection = get_collection(reset=True)  (rebuild from scratch each time for now)
    TODO 2.8: loop over chunks in batches (tqdm(range(0, len(chunks), batch_size))).
    TODO 2.9: for each batch call collection.add(
                  ids=[...], documents=[texts], embeddings=embed_texts(texts),
                  metadatas=[{"source": ..., "page": ...}, ...])
    TODO 2.10: print collection.count() at the end and confirm it equals len(chunks).

    CHECK YOURSELF: what would happen if you embedded the documents with one model
    and queries with another? (Answer: vectors live in different spaces -> nonsense results.)
    """
    raise NotImplementedError


if __name__ == "__main__":
    from ingest import load_documents, build_chunks

    build_index(build_chunks(load_documents()))
    # TODO 2.11: peek at the stored data: get_collection().peek(2) – what's inside?
