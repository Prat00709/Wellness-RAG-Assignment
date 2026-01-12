from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-xl")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

def generate_answer(query, retrieved_chunks, is_unsafe=False):
    context = "\n\n".join(
        f"Source: {c['source']}\n{c['content']}"
        for c in retrieved_chunks
    ).strip()

    safety_note = ""
    if is_unsafe:
        safety_note = (
            "SAFETY RULES:\n"
            "- The query involves pregnancy or a medical condition.\n"
            "- Do NOT give medical advice.\n"
            "- Provide a gentle warning and recommend consulting a professional.\n\n"
        )

    prompt = f"""
You are a yoga and wellness assistant.

{safety_note}
INSTRUCTION:
Answer ONLY using the context.
If the answer is not in the context, reply exactly:
"I’m not sure based on the provided knowledge base."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
""".strip()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=220,
            temperature=0.2,
            do_sample=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
