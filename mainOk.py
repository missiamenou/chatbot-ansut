# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from langchain.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI

# class Question(BaseModel):
#     question: str

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 🔓 autorise toutes les origines (en dev)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # Charger les embeddings + base vectorielle + modèle LLM
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key="AIzaSyCchajXnFcyG0zSFo-DPudVdIqgSO0vwrs"  # ← remplace par ta vraie clé
# )

# db = FAISS.load_local("vectordb_ansut", embeddings, allow_dangerous_deserialization=True)

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     google_api_key="AIzaSyCchajXnFcyG0zSFo-DPudVdIqgSO0vwrs"  # ← la même clé
# )

# @app.post("/chat")
# def chat(req: Question):
#     question = req.question

#     # Étape 1 : recherche des documents les plus proches
#     docs_and_scores = db.similarity_search_with_score(question, k=3)

#     # Étape 2 : assembler le contexte
#     context = "\n\n".join([doc.page_content for doc, _ in docs_and_scores])

#     # Étape 3 : construire le prompt
#     prompt = f"""
# Tu es un assistant virtuel professionnel de l'ANSUT.
# Réponds de façon claire et factuelle en t'appuyant sur les informations suivantes :

# {context}

# Question : {question}
# """

#     # Étape 4 : génération de la réponse
#     response = llm.invoke(prompt)
#     return {"reponse": response.content}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS  # 👈 mise à jour recommandée
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

class Question(BaseModel):
    question: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key="AIzaSyCchajXnFcyG0zSFo-DPudVdIqgSO0vwrs"
)

db = FAISS.load_local("vectordb_ansut", embeddings, allow_dangerous_deserialization=True)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyCchajXnFcyG0zSFo-DPudVdIqgSO0vwrs"
)

@app.post("/chat")
def chat(req: Question):
    question = req.question

    # 🔍 Recherche les 3 documents les plus proches
    docs_and_scores = db.similarity_search_with_score(question, k=3)

    # 🔗 Récupère les contenus et leurs sources
    context = ""
    sources = set()

    for doc, _ in docs_and_scores:
        context += doc.page_content + "\n\n"
        source = doc.metadata.get("source")
        if source:
            sources.add(source)

    # 🧠 Construire le prompt
    prompt = f"""
Tu es un assistant virtuel professionnel de l'ANSUT.
Réponds uniquement à partir des informations suivantes :

{context}

Question : {question}
"""

    # 🤖 Génération de la réponse
    response = llm.invoke(prompt)

    return {
        "reponse": response.content.strip(),
        "sources": list(sources)
    }
