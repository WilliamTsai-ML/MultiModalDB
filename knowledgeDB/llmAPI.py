from sentence_transformers import SentenceTransformer
class llmAPI:
    def __init__(self, model_name: str = "mixedbread-ai/mxbai-embed-large-v1"):
        """Loads the model from the given name."""
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.tokenizer = self.model.tokenizer

    def encode(self, input_text: list):
        """Encodes the given text using the model."""
        return self.model.encode(input_text)
    
    def encode_query(self, query_text):
        """Encodes the given query text using the model."""
        return self.encode(f"'Represent this sentence for searching relevant passages: {query_text}")

        
