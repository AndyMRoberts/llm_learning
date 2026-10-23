"""
STEP 4 – GENERATE: question + retrieved context -> grounded answer from a local LLM
"""
import ollama

from config import LLM_MODEL

SYSTEM_PROMPT = """TODO 4.1: write the system prompt yourself.
It should instruct the model to: (a) answer ONLY using the provided context,
(b) say "I don't know based on the provided documents" if the context is insufficient,
(c) never invent numerical values (wavelengths, thresholds, band centres),
(d) cite sources like [paper.pdf p.3] after claims.
HINT: be explicit and short. Small models follow short, concrete rules best.
"""


def format_context(chunks: list[dict]) -> str:
    """
    Turn retrieved chunks into a numbered context block.

    TODO 4.2: for each chunk produce e.g.
              "[1] (source: file.pdf, page 3)\\n<chunk text>"
              and join blocks with blank lines.
    WHY include source/page in the text itself? So the LLM can cite them.
    """
    raise NotImplementedError


def build_prompt(question: str, chunks: list[dict]) -> str:
    """
    TODO 4.3: return a user prompt containing the context block then the question, e.g.
              "Context:\\n{context}\\n\\nQuestion: {question}\\nAnswer:"
    HINT: Put the question LAST – models attend most to the end of the prompt.
    """
    raise NotImplementedError


def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    Call the local LLM via Ollama.

    TODO 4.4: response = ollama.chat(
                  model=LLM_MODEL,
                  messages=[{"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": build_prompt(question, chunks)}],
                  options={"temperature": 0})
    TODO 4.5: return response["message"]["content"]

    HINT: temperature=0 makes outputs (mostly) deterministic – important for comparing experiments.
    HINT: If you get a connection error, is `ollama serve` running? Did you `ollama pull` the model?
    """
    raise NotImplementedError


def generate_without_rag(question: str) -> str:
    """
    Baseline: ask the LLM with NO retrieved context.

    TODO 4.6: same ollama.chat call, but only the question (a plain system prompt is fine).
    PURPOSE: compare against RAG. This is how you SEE what retrieval adds
             (and where the bare model hallucinates).
    """
    raise NotImplementedError
