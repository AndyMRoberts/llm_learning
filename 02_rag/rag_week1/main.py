"""
STEP 5 – Glue everything together with a small CLI.

Usage:
    python main.py --ingest
    python main.py --ask "How is NDVI calculated?"
    python main.py --ask "What is NDRE?" --no-rag
    python main.py --run-questions        # runs questions.py and saves results.md
    python main.py                        # interactive chat loop
"""
import argparse

from ingest import load_documents, build_chunks
from index import build_index
from retrieve import retrieve
from generate import generate_answer, generate_without_rag
from questions import QUESTIONS
from config import TOP_K


def ingest() -> None:
    """TODO 5.1: load_documents -> build_chunks -> build_index."""
    raise NotImplementedError


def answer(question: str, use_rag: bool = True, k: int = TOP_K) -> str:
    """
    TODO 5.2: if not use_rag: return generate_without_rag(question).
    TODO 5.3: chunks = retrieve(question, k); print sources + scores (transparency!).
    TODO 5.4 (stretch): if the best score is below a threshold you chose in retrieve.py's
              experiments, return "I don't know based on the provided documents" WITHOUT calling the LLM.
    TODO 5.5: return generate_answer(question, chunks).
    """
    raise NotImplementedError


def run_questions() -> None:
    """
    TODO 5.6: for each q in QUESTIONS: get answer with RAG and without RAG;
              write a markdown file results.md with question, expected note, both answers.
    TODO 5.7: read results.md. Mark each answer correct / partly / wrong / hallucinated.
              This manual scoring is what Week 3 (Ragas/TruLens) will automate.
    """
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--ask", type=str)
    parser.add_argument("--no-rag", action="store_true")
    parser.add_argument("--run-questions", action="store_true")
    args = parser.parse_args()

    if args.ingest:
        ingest()
    elif args.ask:
        print(answer(args.ask, use_rag=not args.no_rag))
    elif args.run_questions:
        run_questions()
    else:
        # TODO 5.8: simple input() loop; 'quit' exits; print answer(q) each time.
        raise NotImplementedError


if __name__ == "__main__":
    main()
