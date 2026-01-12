# Yoga-rag-microapp 

This project is a Retrieval-Augmented Generation (RAG) micro-app that answers yoga and wellness questions using:
- A yoga knowledge base (text files)
- dataset link :- https://www.kaggle.com/datasets/pratik0912/yoga-kb/data
- FAISS vector search retrieval
- A local LLM (Flan-T5)
- A safety layer for risky/medical queries
- MongoDB logging (optional)

------------------------------------------------------------
FEATURES
------------------------------------------------------------
1) RAG pipeline
- Loads yoga documents (.txt)
- Splits into chunks
- Creates embeddings
- Stores vectors in FAISS
- Retrieves relevant chunks
- Generates answer using retrieved context

2) Safety layer
- Detects risky queries such as:
  - pregnancy / prenatal
  - hernia, glaucoma, high BP, surgery, injury etc.
- Shows warning
- Prevents unsafe medical advice
- Logs unsafe flag in MongoDB

3) MongoDB logging (optional)
Logs:
- query
- retrieved chunks
- answer
- isUnsafe flag
- safety reason
- timestamp

4) UI
Gradio UI shows:
- Answer
- Sources used
- Safety warning

------------------------------------------------------------
FOLDER STRUCTURE
------------------------------------------------------------
backend/        -> RAG + safety + MongoDB logic
frontend/       -> Gradio UI app
data/yoga_docs/ -> yoga knowledge base (.txt files)
faiss_index/    -> FAISS index generated locally

------------------------------------------------------------
RUN ON KAGGLE (EVALUATOR INSTRUCTIONS)
------------------------------------------------------------

1) Create a new Kaggle Notebook.
   - Go to Kaggle → Notebooks
   - Click “New Notebook”

2) Add the dataset (yoga-kb).
   - Open the Kaggle Notebook
   - On the right side panel, open “Input”
   - Click “Add Input”
   - Search: yoga-kb (dataset link :- https://www.kaggle.com/datasets/pratik0912/yoga-kb/data)
   - Click “Add”

3) Confirm dataset location.
   - Kaggle mounts datasets at: /kaggle/input/
   - This dataset will be available at:
     /kaggle/input/yoga-kb/yoga_docs/

4) Download the GitHub repo ZIP.
   - Open the GitHub repository
   - Click “Code”
   - Click “Download ZIP”
   - Upload the ZIP to Kaggle Inputs
   - Kaggle will automatically unzip the dataset.

5) Copy the extracted repo file into /kaggle/working/.
   - copy the path of the extracted file and past it in YOUR_PATH and run the code given below
   - Run:
   - !cp -r YOUR_PATH /kaggle/working/yoga-rag-microapp
     
7) Go inside the project folder.
   - Run:
   -  %cd /kaggle/working/yoga-rag-microapp

8) Copy yoga docs into the project knowledge base folder.
   - Run:
   - !cp -r /kaggle/input/yoga-kb/yoga_docs /kaggle/working/yoga-rag-microapp/data/
   - !ls /kaggle/working/yoga-rag-microapp/data/yoga_docs | head

9) Install dependencies.
   - Run:
   - !pip install -r requirements.txt

10) Build FAISS index.
   - Run:
   - !python -m backend.rag.ingest

11) Run the Gradio app.
    - Run:
    - !python -m frontend.app_gradio

12) Open the Gradio URL.
    - The output will show a URL like:
      http://127.0.0.1:7860
    - Open it in browser to use the app

Note:
If you face import errors while running scripts directly, use the module commands above.
(These commands are confirmed working on Kaggle)

------------------------------------------------------------
HOW TO RUN LOCALLY (SIMPLE)


1) Download the project
- Download ZIP from GitHub and extract
OR
- Download the zip generated from Kaggle

2) Open the folder in VS Code
- VS Code → File → Open Folder → select the project folder

3) Install dependencies
Open VS Code terminal: Terminal → New Terminal

Windows:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Linux/Mac:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

4) Add yoga documents (required)
Put all yoga .txt docs inside:
data/yoga_docs/

Example:
data/yoga_docs/doc1.txt
data/yoga_docs/doc2.txt
...

5) Build FAISS index (one-time)
Recommended:
python -m backend.rag.ingest

This generates:
faiss_index/

6) Run the app
Recommended:
python -m frontend.app_gradio

7) Open the link shown in terminal
Usually:
http://127.0.0.1:7860

------------------------------------------------------------
OPTIONAL: ENABLE MONGODB LOGGING LOCALLY
------------------------------------------------------------

1) Create file .env in the root folder
2) Add:

MONGO_URI=<mongodb_uri>
DB_NAME=nextyou_rag
COLLECTION_NAME=query_logs

If Mongo URI is not provided, the app will still run (only logging disabled).

------------------------------------------------------------
TROUBLESHOOTING
------------------------------------------------------------
1) Model is too slow/heavy locally
Flan-T5-XL can be heavy on CPU.

Fix:
Use smaller model (recommended):
MODEL_NAME=google/flan-t5-base

2) FAISS index error / missing index
Run again (recommended):
python -m backend.rag.ingest

