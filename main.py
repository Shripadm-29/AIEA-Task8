# main.py

# Import the LogicLMChain class (this ties GPT + KB + Solver together)
from logic_lm_chain import LogicLMChain

# Main function (program starts here)
def main():
    # Path to the knowledge base file (facts + rules are stored here)
    kb_path = "kb.txt"

    # Make a LogicLMChain object using the KB
    logic_lm_chain = LogicLMChain(kb_path)

    # Natural language description we want GPT to turn into logic rules
    description = """
Define the following relations using pure Prolog-style logic rules:

- Uncle: uncle(X, Y) :- parent(Z, Y), sibling(X, Z).
- Aunt: aunt(X, Y) :- parent(Z, Y), sibling(X, Z).
- Cousin: cousin(X, Y) :- parent(Z, X), parent(W, Y), sibling(Z, W).
- Grandparent: grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
- Great-grandparent: greatgrandparent(X, Y) :- parent(X, Z), parent(Z, W), parent(W, Y).

Important:
- Only output pure logic rules.
- No explanations, no bullet points, no extra text.
- Each rule must end with a period.
- Do NOT label the rules or explain them — just list the logic code directly.
"""

    # Step 1: Give description to the chain → GPT makes rules → Solver derives facts
    solution = logic_lm_chain.solve(description)

    # Step 2: Print all the final derived facts
    print("\nFinal Derived Facts:")
    for pred, args in solution:
        # Format like: uncle(john, alice)
        print(f"{pred}({', '.join(args)})")

# Run main() if this file is executed directly
if __name__ == "__main__":
    main()
