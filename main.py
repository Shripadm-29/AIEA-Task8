# main.py

from logic_lm_chain import LogicLMChain

def main():
    kb_path = "kb.txt"
    logic_lm_chain = LogicLMChain(kb_path)

    description = """
Define who is an uncle in terms of parent and sibling relationships.
"""

    solution = logic_lm_chain.solve(description)

    print("\nFinal Derived Facts:")
    for pred, args in solution:
        print(f"{pred}({', '.join(args)})")

if __name__ == "__main__":
    main()
