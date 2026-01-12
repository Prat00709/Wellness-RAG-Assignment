import gradio as gr
from pathlib import Path
import os
import sys

# ONLY CHANGE: __file__ fallback for notebook environments
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except NameError:
    cwd = Path(os.getcwd()).resolve()
    if (cwd / "backend").exists():
        PROJECT_ROOT = cwd
    else:
        PROJECT_ROOT = cwd / "yoga-rag-microapp"

sys.path.append(str(PROJECT_ROOT / "backend"))

from safety import check_safety
from rag.retriever import retrieve_chunks
from llm.local_llm import generate_answer
from db import log_query


def answer_question(query):
    if not query.strip():
        return "Please enter a question.", "", ""

    safety = check_safety(query)
    is_unsafe = safety["isUnsafe"]
    reason = safety["reason"]

    retrieved_chunks = retrieve_chunks(query, k=3)

    answer = generate_answer(
        query=query,
        retrieved_chunks=retrieved_chunks,
        is_unsafe=is_unsafe
    )

    sources = "\n".join(
        f"- {chunk['source']}" for chunk in retrieved_chunks
    ) or "No sources found."

    warning = ""
    if is_unsafe:
        warning = (
            "⚠️ SAFETY WARNING: This query may involve health risks.\n"
            "Please consult a doctor or certified yoga therapist."
        )

    log_query(
        query=query,
        retrieved_chunks=retrieved_chunks,
        answer=answer,
        is_unsafe=is_unsafe,
        safety_reason=reason
    )

    return answer, sources, warning


demo = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(label="Ask anything about yoga"),
    outputs=[
        gr.Textbox(label="Answer"),
        gr.Textbox(label="Sources Used"),
        gr.Textbox(label="Safety Warning")
    ],
    title="🧘 Ask Me Anything About Yoga",
    description="RAG wellness assistant using FAISS retrieval + safety guardrails + MongoDB logging."
)

demo.launch(share=True)
