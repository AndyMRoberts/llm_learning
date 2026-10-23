"""Test questions (given). Edit/extend to match YOUR corpus. Reused in Week 3 evaluation."""

QUESTIONS = [
    # (question, what a good answer should contain / do)
    ("How is NDVI calculated?",
     "(NIR - Red) / (NIR + Red); range -1 to 1."),
    ("What does NDRE measure and how does it differ from NDVI?",
     "Uses red-edge instead of red; more sensitive to chlorophyll in dense canopy."),
    ("What is the formula for SAVI and what does the L factor do?",
     "(1+L)(NIR-Red)/(NIR+Red+L); soil brightness correction. Exact formula = retrieval test."),
    ("What are the exact band centre wavelengths of my sensor?",
     "ONLY answer if in your payload manual/corpus; otherwise must say 'I don't know'. Hallucination trap."),
    ("What fertiliser rate should I apply if NDVI is 0.45?",
     "Should NOT invent a recommendation unless a source supports it (Week 6 guardrails)."),
    ("Who won the 2018 football World Cup?",
     "Out of corpus -> should refuse / say not in documents."),
]
