"""
STEP 3 – RETRIEVE: question -> query vector -> top-k most similar chunks
"""
from config import TOP_K, QUERY_PREFIX
from index import get_collection, embed_texts


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """
    Return the k most relevant chunks as:
        {"text": ..., "source": ..., "page": ..., "score": similarity (higher = better)}

    3.1: embed the query: embed_texts([QUERY_PREFIX + query])  -> list with one vector.
     3.2: res = get_collection().query(query_embeddings=that_list, n_results=k)
     3.3: Chroma returns dicts of lists-of-lists (one inner list per query).
              Use res["documents"][0], res["metadatas"][0], res["distances"][0].
              Print res.keys() and one result the first time to see the shape.
     3.4: convert distance -> similarity: score = 1 - distance  (valid for cosine space).
     3.5: return list of dicts sorted best-first.

    HINT: zip the three lists together.
    """
    query_list = embed_texts([QUERY_PREFIX + query])
    result = get_collection().query(query_embeddings=query_list, n_results=k)
    # print(result.keys())
    # print(result["ids"])
    docs = result["documents"][0]
    metas = result["metadatas"][0]
    dists = result['distances'][0]

    hits = []
    for text, meta, distance in zip(docs, metas, dists):
        hits.append({
            'text': text, 
            'source': meta['source'],
            'page': meta['page'],
            'score': 1 - distance, 
        })

    hits.sort(key=lambda hit: hit["score"], reverse=True)
    return hits


if __name__ == "__main__":
    # Try these and LOOK at what comes back before moving on.
    for q in [
        "What does Radiometric calibration do?",
        "Which wavelengths are the red edge bands?",
        "What is the capital of France?",   # off-topic: what do the scores look like?
        ]:
        print("\n=== ", q)
        for r in retrieve(q):
            print(f"[{r['score']:.3f}] {r['source']} p.{r['page']}: {r['text'][:150]}...")
    # TODO 3.6: Note the score range for relevant vs irrelevant queries.
    #           Could you use a score threshold to say "I don't know"? (Try it in main.py.)
