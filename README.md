# 🤖 CV match ChatBot

An AI-powered recruiter assistant that **matches job descriptions with candidate CVs**.  
This project uses **FastAPI** as a backend for retrieval-augmented generation (RAG)  
and **Streamlit** as a frontend chatbot interface.  

---

## 🚀 Features
- 📄 Load and process candidate CVs (PDF format).
- ✂️ Split CVs into chunks with metadata (preserving candidate names).
- 🔎 Store embeddings in a **Chroma vector database**.
- 🧠 Use **Google Generative AI Embeddings** for semantic search.
- 💬 Generate recruiter-style evaluations using **Cohere LLM**.
- 🖥️ Interactive **Streamlit chatbot** interface for easy querying.

---

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – Backend API  
- [Streamlit](https://streamlit.io/) – Frontend chatbot  
- [LangChain](https://www.langchain.com/) – Orchestration  
- [Chroma](https://www.trychroma.com/) – Vector database  
- [Google Generative AI Embeddings](https://ai.google.dev/) – Embeddings  
- [Cohere](https://cohere.ai/) – Large Language Model  

---

## 📂 Project Structure
```

.
├── main.py         # FastAPI backend (RAG + Cohere pipeline)
├── app.py          # Streamlit frontend chatbot
├── .env            # API keys (Google + Cohere)
├── CVs.zip         # Zipped CVs folder (uploaded to GitHub)
└── requirements.txt

````

---

## ⚙️ Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/mohamed-7oda/CV-match-chatbot-using-RAG.git
cd CV-match-chatbot-using-RAG
````

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add API keys

Create a **`.env`** file in the project root:

```ini
GOOGLE_API_KEY=your_google_api_key
CO_API_KEY=your_cohere_api_key
```

### 5️⃣ Unzip the CVs

If the repo has `CVs.zip`, extract it before running:

#### On Linux/Mac:

```bash
unzip CVs.zip -d CVs
```

#### On Windows (PowerShell):

```powershell
Expand-Archive -Path CVs.zip -DestinationPath CVs
```

After extraction, the structure should look like:

```
CVs/
   ├── John_Doe_CV.pdf
   ├── Jane_Smith_CV.pdf
   └── ...
```

---

## ▶️ Running the Project

### Start FastAPI backend

```bash
uvicorn main:app --reload
```

API will be available at:
👉 `http://127.0.0.1:8000`

### Start Streamlit frontend

```bash
streamlit run app.py
```

---

## 📡 API Endpoint

### `POST /match`

Match CVs against a job description.

**Request Body**

```json
{
  "job_description": "Looking for a Python Backend Developer with FastAPI experience",
  "n_results": 5
}
```

**Response**

```json
{
  "answer": "Ranked recruiter-style evaluation of CVs..."
}
```

---

## 🎯 Example Use Case

1. Upload CVs into the repo as `CVs.zip`.
2. Unzip them into a `CVs/` folder.
3. Run the backend (`uvicorn main:app --reload`).
4. Start the chatbot frontend (`streamlit run app.py`).
5. Ask questions like:

   * *“Find the best CVs for a Data Scientist role with NLP skills.”*
   * *“Who is the strongest match for a Frontend Developer position?”*

---

## 📌 Next Steps

* Add support for multiple document types (Word, TXT).
* Improve ranking by integrating **LLM scoring**.
* Deploy on **Railway / Render / Docker** for production use.

---

## 👨‍💻 Author

Developed by **Mohamed Mahmoud**
