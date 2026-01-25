from abc import ABC, abstractmethod

class LLMInterface(ABC):
    
    @abstractmethod
    def set_generation_model(self,model_id:str):
        """Set the generation model to be used by the LLM.

        Args:
            model_id (str): The identifier of the model to be set.
        """
        pass

    @abstractmethod
    def set_embedding_model(self,model_id:str, embedding_size:int):
        """Set the embedding model to be used by the LLM.

        Args:
            model_id (str): The identifier of the model to be set.
            embedding_size (int): The size of the embeddings.
        """
        pass

    @abstractmethod
    def generate_text(self,prompt:str,chat_history:list=[], max_output_tokens:int=None, temperature:float=None) :
        """Generate text based on the provided prompt.

        Args:
            prompt (str): The input prompt for text generation.
            chat_history (list): The chat history to be included in the prompt.
            max_output_tokens (int): The maximum number of tokens to generate.
            temperature (float): The temperature for sampling.
        """    
        pass

    @abstractmethod
    def embed_text(self,text:str,document_type:str = None):
        """Generate embeddings for the provided text.

        Args:
            text (str): The input text to be embedded.
            document_type (str): The type of document for context.
        """    
        pass

    @abstractmethod
    def construct_prompt(self,prompt:str,role:dict):
        """Construct a prompt with a specific role.

        Args:
            prompt (str): The base prompt.
            role (dict): The role information to be included in the prompt.
        """
        pass