"""
STEP 1 – INGEST: documents -> text -> chunks

Output of this module is a list of "chunk dicts":
    {"id": "paper.pdf::p3::c2", "text": "...", "source": "paper.pdf", "page": 3}
Metadata (source, page) is what lets you CITE answers later, so keep it.
"""
from pathlib import Path
from pypdf import PdfReader
import re
import time

from config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents(docs_dir: Path = DOCS_DIR) -> list[dict]:
    """
    Read every .pdf / .txt / .md file in docs_dir.
    Return one dict per PAGE (PDF) or per FILE (txt/md):
        {"source": filename, "page": page_number_or_1, "text": raw_text}

    1.1: iterate over files with docs_dir.glob("*") (sorted for reproducibility).
    1.2: for ".pdf": use PdfReader(path); loop `enumerate(reader.pages, start=1)`;
              get text with page.extract_text(). Skip pages whose text is empty/whitespace.
    1.3: for ".txt"/".md": path.read_text(encoding="utf-8", errors="ignore").
    1.4: print how many files / pages were loaded (sanity check!).

    HINT: Keep page-level granularity now; it makes citations like "paper.pdf p.7" possible.
    HINT: Wrap PDF reading in try/except – one corrupt PDF shouldn't kill the run.
    """
    docs = []
    print("Starting documents loading...")
    paths = sorted(docs_dir.glob("*"))
    print(f"Found the following docs: {paths}")
    for path in paths:
        print(f"Loading {path.name}:")
        if path.suffix == '.pdf':
            try:
                reader = PdfReader(path)
                for ind, page in enumerate(reader.pages, start=1):

                    text = page.extract_text()
                    if text == '':
                        continue
                    text_dict = {"source": path.name, "page": ind, "text": text}
                    page_count = ind
                    docs.append(text_dict)
            except:
                print(f"Error opening {path}")
                continue
        elif path.suffix == '.txt' or path.suffix == 'md':
            text = path.read_text(encoding="utf-8", errors="ignore")
            text_dict = {"source": path.name, "page": ind, "text": text}
            docs.append(text_dict)
            page_count = 1
        print(f"     {page_count} pages loaded.")
    return docs



def clean_text(text: str) -> str:
    """
    Light cleanup of extracted text.

    1.5: collapse runs of whitespace/newlines into single spaces
              (HINT: " ".join(text.split()) does the job).
    STRETCH: re-join words hyphenated across line breaks ("chloro-\\nphyll").
             Do this BEFORE collapsing whitespace (HINT: re.sub).
    """
    text = re.sub(r"(\w)-\r?\n(\w)", r"\1\2", text)
    text = text.replace("\u02c6", " ")
    return " ".join(text.split())
    


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Fixed-size sliding-window chunking with overlap.

    Example: size=10, overlap=3 over "ABCDEFGHIJKLMNOP" ->
        "ABCDEFGHIJ", "HIJKLMNOP"   (each chunk starts `size - overlap` after the previous)

    1.6: validate overlap < chunk_size (raise ValueError otherwise).
    1.7: step = chunk_size - overlap; loop start in range(0, len(text), step);
              slice text[start:start+chunk_size]; strip; keep if non-empty.
    1.8: stop when a chunk reaches the end of the text (avoid a tiny duplicate tail chunk).

    WHY overlap? A sentence/formula cut at a boundary still appears whole in one chunk.
    STRETCH (preview of Week 2): try to end chunks at a sentence boundary
            (look for the last ". " within the window) instead of mid-word.
    """
    if overlap > chunk_size:
        raise ValueError(f"Chunk size {chunk_size} is smaller than overlap {overlap}")
    step = chunk_size - overlap
    chunks = []
    end = max(1, len(text) - overlap) if text else 0
    for start in range(0, end, step):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks
        

def build_chunks(docs: list[dict]) -> list[dict]:
    """
    Turn page-level docs into chunk dicts with unique ids + metadata.

    1.9: for each doc -> clean_text -> chunk_text -> for each chunk create
              {"id": f"{source}::p{page}::c{i}", "text": chunk, "source": ..., "page": ...}
    1.10: print total chunk count and average chunk length.

    HINT: ids MUST be unique, Chroma rejects duplicates.
    KNOWN LIMITATION (note it down!): chunking per page means text spanning a page break is split.
    """
    total_chunk_count = 0
    total_chunk_cumulative = 0
    chunks = []
    for doc in docs:
        cleaned_text = clean_text(doc["text"])
        chunked_text = chunk_text(cleaned_text)
        for i, chunk in enumerate(chunked_text):
            chunk_dict ={
                "id": f"{doc["source"]}::p{doc["page"]}::c{i}", 
                "text": chunk
                } 
            total_chunk_count += 1
            total_chunk_cumulative += len(chunk)
            chunks.append(chunk_dict)
            average_chunk_size = int(total_chunk_cumulative / total_chunk_count)
    print(f"{total_chunk_count} chunks built, average length: {average_chunk_size}")
    return chunks, total_chunk_count, average_chunk_size




if __name__ == "__main__":
    # Quick manual test – run:  python ingest.py
    start = time.time()
    docs = load_documents()
    print(f"Example Uncleaned Text: {docs[0]}")
    chunks, total_chunk_count, average_chunk_size = build_chunks(docs)
    # Add timing and compute usage measurement to assess effectiveness. 
    end = time.time()
    duration = float(end - start)
    chars_processed = average_chunk_size * total_chunk_count
    print(f"Total Processing Time: {duration:.2f} seconds")
    print(f"Time Per Character: {(duration/chars_processed):.6f}")
    print(f"Time Per Chunk: {(duration/total_chunk_count):.6f}")
    print(f"Example Cleaned Chunks:")
    for c in chunks[:5]:
        print("-" * 60)
        print(c["id"])
        print(c["text"])
    # 1.11: READ the chunks. Are formulas intact? Is table text garbled? Write down 2 observations.
