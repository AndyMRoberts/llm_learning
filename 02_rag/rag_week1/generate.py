"""
STEP 4 – GENERATE: question + retrieved context -> grounded answer from a local LLM
"""
import ollama

from config import LLM_MODEL

SYSTEM_PROMPT = """Answer using only the provided text. Say 'I don't know based on the provided documents'
                if you are not confident in the answer. Do not invent or recall any numerical values 
                (wavelengths, thresholds, band centres), only quote values given in the text. 
                 Cite sources in the manner [<document name>.pdf p.<page number>] where the 
                 <document name> and <page number> are sourced from the context. after claims. 
                 Keep responses below 100 words.""" 



def format_context(chunks: list[dict]) -> str:
    """
    Turn retrieved chunks into a numbered context block.

    4.2: for each chunk produce e.g.
              "[1] (source: file.pdf, page 3)\\n<chunk text>"
              and join blocks with blank lines.
    WHY include source/page in the text itself? So the LLM can cite them.
    """
    context_block = ''
    for i, chunk in enumerate(chunks):
        line = f'[{i}] (source: {chunk['source']}, page {chunk['page']})\n{chunk['text']})'
        context_block += line
    return context_block


def build_prompt(question: str, chunks: list[dict]) -> str:
    """
    4.3: return a user prompt containing the context block then the question, e.g.
              "Context:\\n{context}\\n\\nQuestion: {question}\\nAnswer:"
    HINT: Put the question LAST – models attend most to the end of the prompt.
    """
    return f'Context:\n{format_context(chunks)}\n\nQuestion: {question}\nAnswer:'

def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    Call the local LLM via Ollama.

    4.4: response = ollama.chat(
                  model=LLM_MODEL,
                  messages=[{"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": build_prompt(question, chunks)}],
                  options={"temperature": 0})
    4.5: return response["message"]["content"]

    HINT: temperature=0 makes outputs (mostly) deterministic – important for comparing experiments.
    HINT: If you get a connection error, is `ollama serve` running? Did you `ollama pull` the model?
    """
    response = ollama.chat(
                    model=LLM_MODEL,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": build_prompt(question, chunks)}],
                    options={"temperature": 0})
    return response["message"]["content"]


def generate_without_rag(question: str) -> str:
    """
    Baseline: ask the LLM with NO retrieved context.

    TODO 4.6: same ollama.chat call, but only the question (a plain system prompt is fine).
    PURPOSE: compare against RAG. This is how you SEE what retrieval adds
             (and where the bare model hallucinates).
    """
    response = ollama.chat(
                    model=LLM_MODEL,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": question}],
                    options={"temperature": 0})
    return response["message"]["content"]
