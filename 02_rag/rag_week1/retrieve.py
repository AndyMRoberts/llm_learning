"""
STEP 3 – RETRIEVE: question -> query vector -> top-k most similar chunks
"""
from config import TOP_K, QUERY_PREFIX
from index import get_collection, embed_texts


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """
    Return the k most relevant chunks as:
        {"text": ..., "source": ..., "page": ..., "score": similarity (higher = better)}

    TODO 3.1: embed the query: embed_texts([QUERY_PREFIX + query])  -> list with one vector.
    TODO 3.2: res = get_collection().query(query_embeddings=that_list, n_results=k)
    TODO 3.3: Chroma returns dicts of lists-of-lists (one inner list per query).
              Use res["documents"][0], res["metadatas"][0], res["distances"][0].
              Print res.keys() and one result the first time to see the shape.
    TODO 3.4: convert distance -> similarity: score = 1 - distance  (valid for cosine space).
    TODO 3.5: return list of dicts sorted best-first.

    HINT: zip the three lists together.
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Try these and LOOK at what comes back before moving on.
    for q in [
        "How is NDVI calculated?",
        "Which wavelengths are the red edge bands?",
        "What is the capital of France?",   # off-topic: what do the scores look like?
    ]:
        print("\n=== ", q)
        for r in retrieve(q):
            print(f"[{r['score']:.3f}] {r['source']} p.{r['page']}: {r['text'][:150]}...")
    # TODO 3.6: Note the score range for relevant vs irrelevant queries.
    #           Could you use a score threshold to say "I don't know"? (Try it in main.py.)
