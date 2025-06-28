# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# # Étape 1 : charger le texte
# with open("base_ansut.txt", "r", encoding="utf-8") as f:
#     full_text = f.read()

# # Étape 2 : découper le texte en morceaux
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
# docs = splitter.create_documents([full_text])

# # Étape 3 : générer les embeddings
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key="AIzaSyCchajXnFcyG0zSFo-DPudVdIqgSO0vwrs"  # ← remplace ici par ta vraie clé Google Generative AI
# )

# # Étape 4 : construire et sauvegarder la base FAISS
# vectordb = FAISS.from_documents(docs, embeddings)
# vectordb.save_local("vectordb_ansut")

# print("✅ Base vectorielle créée avec succès.")

# import os
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings


# def create_vector_database():
#     try:
#         # Étape 1 : Vérifier la clé API
#         api_key = os.getenv("GOOGLE_API_KEY")
#         if not api_key:
#             raise ValueError("❌ Clé API Google non trouvée. Définissez GOOGLE_API_KEY dans vos variables d'environnement.")
        
#         # Étape 2 : Charger le texte
#         try:
#             with open("base_ansut.txt", "r", encoding="utf-8") as f:
#                 full_text = f.read()
#         except FileNotFoundError:
#             raise FileNotFoundError("❌ Fichier 'base_ansut.txt' introuvable")
        
#         # Vérifier que le fichier n'est pas vide
#         if not full_text.strip():
#             raise ValueError("❌ Le fichier est vide")
        
#         print(f"📄 Texte chargé : {len(full_text)} caractères")
        
#         # Étape 3 : Découper le texte en morceaux
#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=500, 
#             chunk_overlap=100,
#             separators=["\n\n", "\n", " ", ""]
#         )
#         docs = splitter.create_documents([full_text])
#         print(f"✂️ Texte découpé en {len(docs)} morceaux")
        
#         # Étape 4 : Générer les embeddings
#         embeddings = GoogleGenerativeAIEmbeddings(
#             model="models/embedding-001",
#             google_api_key=api_key
#         )
        
#         # Étape 5 : Construire et sauvegarder la base FAISS
#         print("🔄 Création de la base vectorielle...")
#         vectordb = FAISS.from_documents(docs, embeddings)
#         vectordb.save_local("vectordb_ansut")
        
#         print("✅ Base vectorielle créée avec succès dans 'vectordb_ansut'")
#         return vectordb
        
#     except Exception as e:
#         print(f"❌ Erreur lors de la création : {e}")
#         return None

# if __name__ == "__main__":
#     create_vector_database()
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# from langchain.schema import HumanMessage
from langchain.schema import HumanMessage, Document




# def main():
#     # Configuration
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         print("❌ Définissez GOOGLE_API_KEY dans vos variables d'environnement")
#         return
    
#     # 1. Initialiser le chat model
#     chat_model = ChatGoogleGenerativeAI(
#         model="gemini-pro",
#         google_api_key=api_key,
#         temperature=0.7
#     )
    
#     # 2. Initialiser les embeddings
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=api_key
#     )
    
#     # 3. Charger et traiter le texte
#     try:
#         with open("base_ansut.txt", "r", encoding="utf-8") as f:
#             full_text = f.read()
#     except FileNotFoundError:
#         print("❌ Fichier 'base_ansut.txt' introuvable")
#         return
    
#     # 4. Découper le texte
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500, 
#         chunk_overlap=100
#     )
#     docs = splitter.create_documents([full_text])
    
#     # 5. Créer la base vectorielle
#     try:
#         vectordb = FAISS.from_documents(docs, embeddings)
#         vectordb.save_local("vectordb_ansut")
#         print("✅ Base vectorielle créée avec succès")
#     except Exception as e:
#         print(f"❌ Erreur lors de la création de la base vectorielle : {e}")
#         return
    
#     # 6. Test du chat model
#     try:
#         message = HumanMessage(content="Bonjour, comment allez-vous ?")
#         response = chat_model([message])
#         print(f"🤖 Réponse du modèle : {response.content}")
#     except Exception as e:
#         print(f"❌ Erreur lors du test du chat : {e}")

# if __name__ == "__main__":
#     main()

# def main():
#     # Configuration
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         print("❌ Définissez GOOGLE_API_KEY dans vos variables d'environnement")
#         return
    
#     # 1. Initialiser le chat model
#     chat_model = ChatGoogleGenerativeAI(
#         model="gemini-pro",
#         google_api_key=api_key,
#         temperature=0.7
#     )
    
#     # 2. Initialiser les embeddings
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=api_key
#     )
    
#     # 3. Charger et parser base_ansut.txt
#     try:
#         with open("base_ansut.txt", "r", encoding="utf-8") as f:
#             raw_blocks = f.read().split("SOURCE:")
#             docs = []
#             for block in raw_blocks:
#                 block = block.strip()
#                 if not block:
#                     continue
#                 lines = block.split("\n", 1)
#                 url = lines[0].strip()
#                 content = lines[1].strip() if len(lines) > 1 else ""
#                 if content:
#                     docs.append(Document(page_content=content, metadata={"source": url}))
#     except FileNotFoundError:
#         print("❌ Fichier 'base_ansut.txt' introuvable")
#         return

#     # 4. Découper les documents si nécessaire
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
#     split_docs = splitter.split_documents(docs)
    
#     # 5. Créer la base vectorielle avec métadonnées
#     try:
#         vectordb = FAISS.from_documents(split_docs, embeddings)
#         vectordb.save_local("vectordb_ansut")
#         print("✅ Base vectorielle créée avec succès avec metadata (sources)")
#     except Exception as e:
#         print(f"❌ Erreur lors de la création de la base vectorielle : {e}")
#         return
    
#     # 6. Test du chat model seul
#     try:
#         message = HumanMessage(content="Bonjour, comment allez-vous ?")
#         response = chat_model([message])
#         print(f"🤖 Réponse du modèle : {response.content}")
#     except Exception as e:
#         print(f"❌ Erreur lors du test du chat : {e}")

# if __name__ == "__main__":
#     main()


import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

def clean_and_parse_file(file_path: str):
    print("📄 Lecture du fichier :", file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("=== PAGE:")
    documents = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # extraire source et texte
        lines = block.split("\n", 1)
        if len(lines) < 2:
            continue

        url = lines[0].strip()
        texte = lines[1].strip()

        # Nettoyage supplémentaire (optionnel)
        texte = texte.replace("\n", " ").strip()
        if len(texte) < 100:
            continue  # ignorer trop court

        documents.append(Document(page_content=texte, metadata={"source": url}))

    print(f"✅ {len(documents)} documents extraits du site.")
    return documents

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Variable GOOGLE_API_KEY manquante")
        return

    # 1. Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )

    # 2. Lecture du fichier scrapé
    docs = clean_and_parse_file("base_ansut.txt")

    # 3. Split des documents longs
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    split_docs = splitter.split_documents(docs)
    print(f"🧩 {len(split_docs)} blocs générés après découpage")

    # 4. Création de la base vectorielle
    vectordb = FAISS.from_documents(split_docs, embeddings)
    vectordb.save_local("vectordb_ansut")
    print("✅ Base vectorielle enregistrée dans le dossier 'vectordb_ansut'")

if __name__ == "__main__":
    main()
