from pathlib import Path
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledgeDB.llmAPI import llmAPI

class DBobject:
    def __init__(self, db_path: Path | str = "./local_db", collection: str = "local_collection"):
        '''
        Constructor for the DB object class.
        '''
        self.client = chromadb.PersistentClient(path=str(db_path))
        self.collection = self.client.get_or_create_collection(name=collection)
        self.language_model = None
        self.text_splitter = None

    def set_language_model(self, model: llmAPI):
        '''
        Set the language model to use.
        '''
        self.language_model = model
        self.text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(tokenizer=model.tokenizer, chunk_size=400, chunk_overlap=20)

    def add(self, ids: list, docs: list):
        '''
        Add documents to the collection.
        '''
        assert self.language_model is not None, "Please set a language model first."
        embeddings = []
        trunk_ids = []
        metadatas = []
        for i, doc in enumerate(docs):
            for j, chunk in enumerate(self.text_splitter.split_text(doc)):
                trunk_ids.append(f"{ids[i]}_{j}")
                embeddings.append(self.language_model.encode(chunk))
                metadatas.append({"doc-id": ids[i], "doc-chunk": j})
        
        self.add_embeddings(
            ids=trunk_ids,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def add_embeddings(self, ids: list, embeddings: list, metadatas: list | None):
        '''
        Add documents to the collection.
        '''
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, query_text: str, n_results: int = 5):
        query_emb = self.language_model.encode_query(query_text).tolist()
        results = self.collection.query(query_embeddings=[query_emb], n_results=n_results)
        return [f"{r['doc-id']}_{r['doc-chunk']: d}" for r, d in zip(results['metadatas'][0], results['distances'][0])]

    
