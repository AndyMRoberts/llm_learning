# Week 1 – Naive RAG on Agronomy / Hyperspectral Docs (4-hour plan)

Goal: build a pipeline that **ingests → chunks → embeds → stores → retrieves → generates**,
and be able to explain every step. Fill in each `TODO` yourself; hints are in the comments.

## Files (work through them in this order)
| Order | File | What you build |
|---|---|---|
| 0 | `config.py` | (given) all tunable settings in one place |
| 1 | `ingest.py` | load PDFs/text, split into overlapping chunks |
| 2 | `index.py` | embed chunks, store them in ChromaDB |
| 3 | `retrieve.py` | embed a query, fetch top-k similar chunks |
| 4 | `generate.py` | build a grounded prompt, call a local LLM |
| 5 | `main.py` | CLI that glues it together (+ no-RAG baseline) |
| 6 | `questions.py` | (given) test questions, incl. hallucination traps for Week 3 |

## Setup (≈20 min)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Local LLM (open weights, also useful for Weeks 5-8):
#   install Ollama from https://ollama.com then:
ollama pull llama3.1:8b        # or llama3.2:3b if short on RAM/VRAM
```

## Corpus (≈10 min)
Drop 3–10 files into `docs/`. Good sources: open-access PDFs on NDVI/NDRE/red-edge
crop monitoring (MDPI *Remote Sensing*, *Agronomy*, arXiv), your drone payload manuals,
or your own hyperspectral collection notes. A tiny `docs/sample_ndvi_notes.md` is
included only so you can test before your real corpus is ready.
Tip: avoid scanned PDFs (no text layer) for now – extraction will return empty strings.

I used: 
- (23Mb) Computational Intelligence Based Hyperspectral Image Analysis and Applications Volume 2, 2025
- (177Mb) Precision agriculture '23, Stafford, John V., editor.2023
- (11Mb) Unmanned Aerial Vehicle: Applications in Agriculture and Environment Ram Avtar, editor.; Watanabe, Teiji, editor.; 2020; 1st ed. 2020.



## Suggested timeline
| Time | Step |
|---|---|
| 0:00–0:30 | Setup, gather corpus, read this README + skim comments in every file |
| 0:30–1:15 | `ingest.py` – loading + chunking. Print chunks and *look at them* |
| 1:15–2:00 | `index.py` – embeddings + Chroma. Check collection count |
| 2:00–2:30 | `retrieve.py` – inspect top-k results and scores for 5 queries |
| 2:30–3:15 | `generate.py` + `main.py` – end-to-end answers with citations |
| 3:15–4:00 | Experiments (below) + write 5 bullet notes on what you learned |

## Concepts to be able to explain at the end
1. Why chunk, and what chunk size/overlap trade off (precision vs context).
2. What an embedding is; why query and document must use the *same* model.
3. Cosine similarity vs distance (Chroma returns distance).
4. Why "answer only from the context" prompting reduces – but doesn't eliminate – hallucination.
5. Failure modes you observed (e.g. formulas split mid-chunk, table text garbled).

## Experiments (do at least 3)
- Change `CHUNK_SIZE` 400 / 800 / 1500. Which questions improve/worsen?
- Change `TOP_K` 2 / 4 / 8. When does extra context hurt?
- Run `--no-rag` on the same question. Does the LLM hallucinate band values?
- Ask something *not* in your corpus. Does it refuse properly?
- Ask for an exact formula (NDVI, NDRE, SAVI). Does dense retrieval find it? (This motivates **hybrid search** in Week 2.)
- Look at a chunk with a table or equation. Note what the PDF extractor did to it (motivates semantic chunking / better parsers in Week 2).

## Done when
- `python main.py --ingest` builds the index without errors.
- `python main.py --ask "How is NDVI calculated?"` returns a grounded answer with source + page citations.
- You've logged results for the questions in `questions.py` (Week 3 will score these properly).
