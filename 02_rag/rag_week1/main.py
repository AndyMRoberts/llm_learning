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
from asyncio import QueueShutDown

from ingest import load_documents, build_chunks
from index import build_index
from retrieve import retrieve
from generate import generate_answer, generate_without_rag
from questions import QUESTIONS
from config import TOP_K, MIN_SCORE




def ingest() -> None:
    """TODO 5.1: load_documents -> build_chunks -> build_index."""
    docs = load_documents()
    chunks = build_chunks(docs)
    build_index(chunks)

def answer(question: str, use_rag: bool = True, k: int = TOP_K) -> str:
    """
    5.2: if not use_rag: return generate_without_rag(question).
    5.3: chunks = retrieve(question, k); print sources + scores (transparency!).
    5.4 (stretch): if the best score is below a threshold you chose in retrieve.py's
              experiments, return "I don't know based on the provided documents" WITHOUT calling the LLM.
    5.5: return generate_answer(question, chunks).
    """
    if not use_rag:
        return generate_without_rag(question)
    top_chunks = retrieve(question, k)
    for chunklet in top_chunks:
        print(f'Source:{chunklet['source']}, Score: {chunklet['score']}')
    if top_chunks[0]['score'] < MIN_SCORE:
        return "I don't know based on the provided documents."
    else:
        return generate_answer(question, top_chunks)

def run_questions() -> None:
    """
    5.6: for each q in QUESTIONS: get answer with RAG and without RAG;
              write a markdown file results.md with question, expected note, both answers.
    5.7: read results.md. Mark each answer correct / partly / wrong / hallucinated.
              This manual scoring is what Week 3 (Ragas/TruLens) will automate.
    """
    with open('results.md', 'w',  encoding='utf-8') as f:
        i = 1
        for q, a in QUESTIONS:
            print(f'Question: {q}, Answer: {a}')
            f.write("---")
            f.write(f"\n\n# Question {i}:\n")
            f.write(q)
            f.write(f'\n\n**RAG Response:**\n')
            print('Asking using RAG:')
            f.write(answer(q, use_rag=True))
            f.write(f'\n\n**No RAG Response:**\n')
            print('Asking without RAG:')
            f.write(answer(q, use_rag=False))
            f.write(f'\n\n**Actual Answer:**\n')
            f.write(a)
            f.write(f'\n\n**My Rating:**\n\n')
            i += 1
        

def main() -> None:
    parser = argparse.ArgumentParser(description=main.__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,)
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
        # 5.8: simple input() loop; 'quit' exits; print answer(q) each time.
        while True:
            question = input("Ask a question:\n")
            if question in ['q', 'quit']:
                break
            print(answer(question, use_rag=not args.no_rag))

if __name__ == "__main__":
    main()
