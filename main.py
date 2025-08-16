from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain_cohere import ChatCohere
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# =========================
# 0. Setup
# =========================
load_dotenv()

app = FastAPI()

# Google API key (embedding)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Cohere API key
os.environ["CO_API_KEY"] = os.getenv("CO_API_KEY")


# =========================
# 1. Load and preprocess CVs
# =========================
load = PyPDFDirectoryLoader("C:\\Users\\mohamed mahmoud emam\\OneDrive\\Desktop\\CVs RAG\\CVs")  # <-- folder inside project
pdf_docs = load.load()

# Split into chunks (preserve metadata)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(pdf_docs)

# Attach filename as cv_name
for chunk in chunks:
    source = chunk.metadata.get("source", "Unknown CV")
    chunk.metadata["cv_name"] = source.split("/")[-1]

# Generate embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Store in Chroma vector DB
db = Chroma.from_documents(documents=chunks, embedding=embeddings, collection_name="rag_collection")


# =========================
# 2. Retrieval
# =========================
def get_relevant_chunks_with_scores(question, db, n_results=5):
    results = db.similarity_search_with_score(question, k=n_results)
    sorted_results = sorted(results, key=lambda x: x[1])  # sort by similarity
    return [
        f"From CV: {doc.metadata.get('cv_name')}\n\n{doc.page_content}"
        for doc, score in sorted_results
    ]


# =========================
# 3. LLM Setup
# =========================
llm = ChatCohere(model="command-a-03-2025")

prompt = ChatPromptTemplate.from_template(
    """You are an expert recruiter helping to evaluate CVs against a job description.  
Each chunk below includes the candidate’s CV name.  
Use this information to explain which CVs best fit the role.  
Mention the CV name when discussing strengths/weaknesses.  

Job Description:
{question}

Relevant CV Chunks:
{context}

Answer in a recruiter style, grouping analysis by CV name and ranking candidates from strongest to weakest.
"""
)


def generate_recruiter_response(job_description, db, n_results=5):
    relevant_chunks = get_relevant_chunks_with_scores(job_description, db, n_results)
    context = "\n\n".join(relevant_chunks)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"context": context, "question": job_description})
    return response


# =========================
# 4. FastAPI Models
# =========================
class JobRequest(BaseModel):
    job_description: str
    n_results: int = 5


class JobResponse(BaseModel):
    answer: str


# =========================
# 5. Endpoint
# =========================
@app.post("/match", response_model=JobResponse)
async def match_candidates(request: JobRequest):
    """
    Takes a job description and returns ranked CVs with recruiter-style evaluation.
    """
    answer = generate_recruiter_response(request.job_description, db, request.n_results)
    return JobResponse(answer=answer)
