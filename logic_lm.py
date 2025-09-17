# models/logic_lm.py

from langchain_llm import LangChainLLM

from logic_utils import LogicSolver, check_logic_validity


# Class: LogicLMModel
class LogicLMModel:
    # when we make this model, we set up both the LLM and the solver
    def __init__(self, model_name="gpt-3.5-turbo"):
        # create a GPT model wrapper
        self.llm = LangChainLLM(model_name)
        # create a logic solver
        self.solver = LogicSolver()

    # Step 1: Turn English into Logic
    def logic_translate(self, question):
        # make a special prompt that tells GPT exactly how to format the output
        prompt = (
            "Translate the following description into symbolic Prolog-style logic facts and rules."
            " Only output facts and rules."
            " Do NOT include any queries, answers, or explanations."
            " Ensure correct syntax with a period at the end of each fact and rule."
            " Do NOT use markdown formatting or code blocks."
            "\n\n"
            f"{question}"  # the user’s natural language question goes here
        )
        # send the prompt to GPT and return the output
        return self.llm.query(prompt)

    # Step 2 (if needed): Fix Syntax Errors
    def refine_logic(self, broken_logic, errors):
        # join all error messages into one string
        error_message = "\n".join(errors)
        # tell GPT: “Here’s broken logic, just fix the syntax”
        prompt = (
            f"The following Prolog-like logic contains syntax errors:\n"
            f"{error_message}\n\n"
            "Please correct only the syntax errors while keeping ALL the original facts and rules."
            " Do NOT add, remove, or answer anything."
            " Only fix the syntax. Keep facts and rules exactly as they are."
            "\n\n"
            f"{broken_logic}"
        )
        # ask GPT to fix it
        return self.llm.query(prompt)

    # Step 3: Full Solve Pipeline
    def solve(self, question):
        # (1) Translate question into logic
        logic = self.logic_translate(question)

        print("\nGenerated Logic Output:\n")
        print(logic)

        # (2) Validate the logic (check for syntax errors)
        errors = check_logic_validity(logic)
        if errors:
            print("\nErrors Detected in Logic:")
            for error in errors:
                print(error)
            print("\nRefining Logic...\n")
            # if errors exist, ask GPT to fix them
            logic = self.refine_logic(logic, errors)

            print("\nRefined Logic Output:\n")
            print(logic)

        # (3) Solve logic using our LogicSolver
        solution = self.solver.solve_logic(logic)
        return solution
