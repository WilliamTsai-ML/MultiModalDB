from sentence_transformers import SentenceTransformer
from transformers import AutoModel,AutoProcessor, logging
logging.set_verbosity_error()

from PIL import Image
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
    
    def to(self, device):
        """Moves the model to the given device."""
        self.model = self.model.to(device)
        return self

        
class blipAPI:
    def __init__(self, model_name: str = "openai/clip-vit-large-patch14"):
        """Loads the model from the given name."""
        self.model_name = model_name
        self.model = AutoModel.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)

    def encode(self, input: str | Image.Image):
        """Encodes the given text or image using the model."""
        if isinstance(input, str):
            text_input = self.processor(text=input, return_tensors="pt").to("cuda")
            return self.model.get_text_features(**text_input)[0]
        elif isinstance(input, Image.Image):
            image_input = self.processor(images=input, return_tensors="pt")
            return self.model.get_image_features(**image_input)[0]
        else:
            raise ValueError("Input must be a string or an Image object.")
    
    def encode_query(self, query_text):
        """Encodes the given query text using the model."""
        return self.encode("A photo of a " + query_text)
    
    def to(self, device):
        """Moves the model to the given device."""
        self.model = self.model.to(device)
        return self

        
