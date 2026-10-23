"""
STEP 1 – INGEST: documents -> text -> chunks

Output of this module is a list of "chunk dicts":
    {"id": "paper.pdf::p3::c2", "text": "...", "source": "paper.pdf", "page": 3}
Metadata (source, page) is what lets you CITE answers later, so keep it.
"""
from pathlib import Path
from pypdf import PdfReader

from config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents(docs_dir: Path = DOCS_DIR) -> list[dict]:
    """
    Read every .pdf / .txt / .md file in docs_dir.
    Return one dict per PAGE (PDF) or per FILE (txt/md):
        {"source": filename, "page": page_number_or_1, "text": raw_text}

    TODO 1.1: iterate over files with docs_dir.glob("*") (sorted for reproducibility).
    TODO 1.2: for ".pdf": use PdfReader(path); loop `enumerate(reader.pages, start=1)`;
              get text with page.extract_text(). Skip pages whose text is empty/whitespace.
    TODO 1.3: for ".txt"/".md": path.read_text(encoding="utf-8", errors="ignore").
    TODO 1.4: print how many files / pages were loaded (sanity check!).

    HINT: Keep page-level granularity now; it makes citations like "paper.pdf p.7" possible.
    HINT: Wrap PDF reading in try/except – one corrupt PDF shouldn't kill the run.
    """

    raise NotImplementedError



def clean_text(text: str) -> str:
    """
    Light cleanup of extracted text.

    TODO 1.5: collapse runs of whitespace/newlines into single spaces
              (HINT: " ".join(text.split()) does the job).
    STRETCH: re-join words hyphenated across line breaks ("chloro-\\nphyll").
             Do this BEFORE collapsing whitespace (HINT: re.sub).
    """
    raise NotImplementedError


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Fixed-size sliding-window chunking with overlap.

    Example: size=10, overlap=3 over "ABCDEFGHIJKLMNOP" ->
        "ABCDEFGHIJ", "HIJKLMNOP"   (each chunk starts `size - overlap` after the previous)

    TODO 1.6: validate overlap < chunk_size (raise ValueError otherwise).
    TODO 1.7: step = chunk_size - overlap; loop start in range(0, len(text), step);
              slice text[start:start+chunk_size]; strip; keep if non-empty.
    TODO 1.8: stop when a chunk reaches the end of the text (avoid a tiny duplicate tail chunk).

    WHY overlap? A sentence/formula cut at a boundary still appears whole in one chunk.
    STRETCH (preview of Week 2): try to end chunks at a sentence boundary
            (look for the last ". " within the window) instead of mid-word.
    """
    raise NotImplementedError


def build_chunks(docs: list[dict]) -> list[dict]:
    """
    Turn page-level docs into chunk dicts with unique ids + metadata.

    TODO 1.9: for each doc -> clean_text -> chunk_text -> for each chunk create
              {"id": f"{source}::p{page}::c{i}", "text": chunk, "source": ..., "page": ...}
    TODO 1.10: print total chunk count and average chunk length.

    HINT: ids MUST be unique, Chroma rejects duplicates.
    KNOWN LIMITATION (note it down!): chunking per page means text spanning a page break is split.
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Quick manual test – run:  python ingest.py
    docs = load_documents()
    # chunks = build_chunks(docs)
    # for c in chunks[:3]:
    #     print("-" * 60)
    #     print(c["id"])
    #     print(c["text"])
    # TODO 1.11: READ the chunks. Are formulas intact? Is table text garbled? Write down 2 observations.
    # TODO Add timing and compute usage measurement to assess effectiveness. 
