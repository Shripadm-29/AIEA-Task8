# logic_lm_chain.py


from langchain_llm import LangChainLLM

from logic_utils import LogicSolver, check_logic_validity

from retriever import create_retriever_from_kb

from langchain.prompts import PromptTemplate

from langchain.schema.runnable import RunnablePassthrough


class LogicLMChain:
    def __init__(self, kb_path, model_name="gpt-3.5-turbo"):
        # set up GPT model
        self.llm = LangChainLLM(model_name)

        # set up symbolic logic solver
        self.solver = LogicSolver()

        # make a retriever that can fetch info from a knowledge base file
        self.retriever = create_retriever_from_kb(kb_path)

        # save the KB path so we can load it later
        self.kb_path = kb_path

        # make a prompt template that tells GPT exactly what to do
        self.prompt = PromptTemplate(
            input_variables=["context", "description"],  # placeholders we fill later
            template=(
                "You are given some background knowledge:\n\n{context}\n\n"
                "Translate the following description into general Prolog-style logic rules."
                " Only output general rules. Do NOT output specific facts, queries, or answers."
                " The rules should work for any entity, not just a particular example."
                " Use the convention that sibling(X, Y) means X is a sibling of Y, and sibling relationships are symmetric."
                " Make sure to define uncle(X, Y) as: uncle(X, Y) :- parent(Z, Y), sibling(X, Z)."
                " Ensure each rule ends with a period.\n\n"
                "{description}"  # this is the actual user description
            )
        )

        # build a chain where the prompt feeds into the GPT model
        self.chain = self.prompt | self.llm.llm


    # Translate English into logic (with context)
    def logic_translate(self, context, description):
        # fill the prompt with actual context and description
        full_prompt = self.prompt.format(context=context, description=description)
        # send it to GPT
        return self.llm.query(full_prompt)


    # Fix broken logic if syntax errors are found
    def refine_logic(self, broken_logic, errors):
        # join all errors into a single message
        error_message = "\n".join(errors)
        # ask GPT to ONLY fix syntax problems
        prompt = (
            f"The following Prolog-like logic contains syntax errors:\n"
            f"{error_message}\n\n"
            "Please correct only the syntax errors while keeping ALL the original facts and rules."
            " Do NOT add, remove, or answer anything."
            " Only fix the syntax. Keep facts and rules exactly as they are."
            "\n\n"
            f"{broken_logic}"
        )
        return self.llm.query(prompt)

    # Load knowledge base facts from file
    def load_kb_facts(self):
        # open the KB file
        with open(self.kb_path, 'r') as f:
            lines = f.readlines()
        facts = []
        for line in lines:
            line = line.strip()
            # keep only real facts, skip comments (%) and skip rules (:-)
            if line and not line.startswith('%') and ':-' not in line:
                facts.append(line)
        # return all facts as a big string
        return "\n".join(facts)


    # Full Solve Pipeline
    def solve(self, description):
        # Step 1: Retrieve context from KB (optional, gives background info)
        docs = self.retriever.invoke(description)
        context = "\n".join([doc.page_content for doc in docs])

        # Step 2: Ask GPT to make logic rules
        logic_rule = self.logic_translate(context, description)

        print("\nGenerated Logic Output:\n")
        print(logic_rule)

        # Step 3: Check logic for syntax errors
        errors = check_logic_validity(logic_rule)
        if errors:
            print("\nErrors Detected in Logic:")
            for error in errors:
                print(error)
            print("\nRefining Logic...\n")
            logic_rule = self.refine_logic(logic_rule, errors)
            print("\nRefined Logic Output:\n")
            print(logic_rule)

        # Step 4: Load KB facts from file
        kb_facts = self.load_kb_facts()

        # Merge KB facts with the GPT-generated rules
        full_logic = kb_facts + "\n" + logic_rule

        # Step 5: Use symbolic solver to solve it
        solution = self.solver.solve_logic(full_logic)
        return solution
