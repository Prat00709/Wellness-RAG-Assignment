from backend.config import DATA_PATH, VECTOR_DB_PATH

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_documents():
    docs = []
    for file_path in sorted(DATA_PATH.glob("*.txt")):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            docs.append(Document(page_content=content, metadata={"source": file_path.name}))
    return docs


def build_faiss_index():
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(str(VECTOR_DB_PATH))

    print(f"✅ FAISS index built with {len(chunks)} chunks at: {VECTOR_DB_PATH}")


if __name__ == "__main__":
    build_faiss_index()
