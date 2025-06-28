from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

# Chargement des variables d'environnement
load_dotenv()

class Question(BaseModel):
    question: str

app = FastAPI()

# CORS pour accès frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialisation des modèles
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY non défini dans l'environnement")

# Embeddings & vector DB
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

db = FAISS.load_local("vectordb_ansut", embeddings, allow_dangerous_deserialization=True)
print("📦 Nombre de documents vectorisés :", db.index.ntotal)
query = "Qui est le directeur général de l'ANSUT ?"
print(f"\n🔎 TEST: {query}")

results = db.similarity_search(query, k=3)
for i, doc in enumerate(results, 1):
    print(f"\n--- Résultat {i} ---")
    print(doc.page_content[:500])
    print("📎 Source :", doc.metadata.get("source"))



# Modèle LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

@app.post("/chat")
def chat(req: Question):
    question = req.question

    try:
        docs_and_scores = db.similarity_search_with_score(question, k=3)

        context = ""
        sources = set()

        for doc, _ in docs_and_scores:
            context += doc.page_content + "\n\n"
            source = doc.metadata.get("source")
            if source:
                sources.add(source)

        # Limiter le contexte à 8000 caractères (~5000 tokens)
        MAX_CHARS = 8000
        if len(context) > MAX_CHARS:
            context = context[:MAX_CHARS] + "\n\n[...contenu tronqué]"

        prompt = f"""
Tu es un assistant virtuel professionnel de l’ANSUT, chargé d’accueillir, renseigner et orienter les visiteurs comme une secrétaire expérimentée.

Tu t’exprimes avec courtoisie et clarté, mais sans saluer inutilement à chaque réponse. Garde un ton respectueux et professionnel, mais ne répète pas "Bonjour" ou "Bienvenue" à chaque message.

Tu dois répondre uniquement à partir des informations suivantes, issues du site officiel de l’ANSUT (https://ansut.ci).  
Si une information n’est pas disponible dans ce contexte, indique simplement et poliment :  
"Je suis désolé(e), je n’ai pas trouvé cette information sur le site de l’ANSUT."

Tu dois également garder le fil de la conversation, comme le ferait une assistante efficace.

Voici les informations disponibles :  
{context}

Question : {question}
"""


        response = llm.invoke(prompt)

        return {
            "reponse": response.content.strip(),
            "sources": list(sources)
        }

    except Exception as e:
        return {
            "reponse": f"❌ Erreur pendant le traitement : {str(e)}",
            "sources": []
        }
