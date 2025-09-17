# utils/langchain_llm.py

from langchain_community.chat_models import ChatOpenAI

# Import os so we can read environment variables
import os

# Import dotenv so we can load our API key from a .env file
from dotenv import load_dotenv

# Load all the variables inside the .env file (like OPENAI_API_KEY)
load_dotenv()

class LangChainLLM:
    # when we create this class, we set up the OpenAI model
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    # this function asks the model a question (prompt) and gets an answer
    def query(self, prompt):
        return self.llm.predict(prompt)

