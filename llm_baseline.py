# models/llm_baseline.py

# Import our GPT wrapper class
from langchain_llm import LangChainLLM

class LLMBaselineModel:
    # when we create this class, we set up the GPT model
    def __init__(self, model_name="gpt-3.5-turbo"):
        # make a LangChainLLM object (this talks to GPT)
        self.llm = LangChainLLM(model_name)

    def answer_question(self, question):
        # make a simple prompt that asks GPT to answer the question
        prompt = f"Answer the following logical reasoning question:\n\n{question}"

        # send the prompt to GPT and return the model’s answer
        return self.llm.query(prompt)
