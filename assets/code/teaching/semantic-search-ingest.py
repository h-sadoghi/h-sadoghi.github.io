from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def main():
    urls = [
        "https://visupimmigration.com/netherland-startup-visa/",
        "https://visupimmigration.com/canada-startup-visa/",
        "https://visupimmigration.com/finland-startup-visa/",
        "https://visupimmigration.com/denmark-startup-visa/",
        "https://visupimmigration.com/portugal-startup-visa/",
        "https://visupimmigration.com/latvia-startup-visa/",
        "https://visupimmigration.com/estonia-startup-visa/",
        "https://visupimmigration.com/france-startup-visa/",
        "https://visupimmigration.com/germany-startup-visa/",
        "https://visupimmigration.com/england-startup-visa/",
    ]

    loader = WebBaseLoader(urls)
    docs = loader.load()
    print("Loaded docs:", len(docs))

    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    print("Total chunks:", len(split_docs))

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vs = FAISS.from_documents(split_docs, embeddings)
    vs.save_local("/root/knowledge/visup-faiss")
    print("Saved to /root/knowledge/visup-faiss")

if __name__ == "__main__":
    main()
 