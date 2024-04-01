from pathlib import Path
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledgeDB.encoderAPI import blipAPI, llmAPI

class DBobject:
    def __init__(self, db_path: Path | str = "./local_db", collection: str = "local_collection"):
        '''
        Constructor for the DB object class.
        '''
        self.client = chromadb.PersistentClient(path=str(db_path))
        self.text_collection = self.client.get_or_create_collection(name=collection+"_text", metadata={"hnsw:space": "cosine"})
        self.image_collection = self.client.get_or_create_collection(name=collection+"_image", metadata={"hnsw:space": "cosine"})
        self.language_model = None
        self.blip_model = None
        self.text_splitter = None

    def set_language_model(self, model: llmAPI):
        '''
        Set the language model to use.
        '''
        self.language_model = model
        # self.text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(tokenizer=model.tokenizer, chunk_size=400, chunk_overlap=20)
    
    def set_blip_model(self, model: blipAPI):
        '''
        Set the language model to use.
        '''
        self.blip_model = model

    def to(self, device):
        self.language_model.model.to(device)
        self.blip_model.model.to(device)

    def add(self, ids: list, docs: list):
        '''
        Add documents to the collection.
        '''
        assert self.language_model is not None, "Please set a language model first."

        trunk_ids = []
        trunks = []
        embeddings = []
        metadatas = []

        image_ids = []
        image_embeddings = []

        for i, doc in enumerate(docs):
            if isinstance(doc, str):
                for j, chunk in enumerate(doc.split("\n\n")):
                    trunk_ids.append(f"{ids[i]}_{j}")
                    trunks.append(chunk)
                    embeddings.append(self.language_model.encode(chunk).tolist())
                    metadatas.append({"doc-id": ids[i], "doc-chunk": j})
            else:
                image_ids.append(f"{ids[i]}")
                image_embeddings.append(self.blip_model.encode(doc).tolist())

        
        self.text_collection.add(
            ids=trunk_ids,
            documents=trunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        self.image_collection.add(
            ids=image_ids,
            embeddings=image_embeddings
        )

    def query(self, query_text: str, n_results: int = 10):
        '''Query the database for matching results.'''
        text_query_emb = self.language_model.encode_query(query_text).tolist()
        results = self.text_collection.query(query_embeddings=[text_query_emb], n_results=n_results)
        
        query_text_results = []
        for i, (_, res) in enumerate(sorted(zip(results['distances'][0], results["ids"][0]))):
            query_text_results.append(f"{i}: {res} {results['metadatas'][0][i]} {results['documents'][0][i][:1000]}")
        
        image_query_embedding = self.blip_model.encode_query(str(query_text)).tolist()
        results = self.image_collection.query(query_embeddings=[image_query_embedding], n_results=n_results)
        query_image_results = []
        for i, (_, res) in enumerate(sorted(zip(results['distances'][0], results["ids"][0]))):
            query_image_results.append(f"{i}: {res}")

        return query_text_results, query_image_results
    
