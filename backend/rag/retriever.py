from backend.config import VECTOR_DB_PATH

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def retrieve_chunks(query, k=8):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        str(VECTOR_DB_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    results = vectorstore.similarity_search(query, k=k)

    retrieved = []
    for idx, doc in enumerate(results):
        retrieved.append({
            "chunk_id": idx,
            "source": doc.metadata.get("source", "unknown"),
            "content": doc.page_content
        })

    return retrieved
