# main.py

from logic_lm_chain import LogicLMChain

def main():
    kb_path = "kb.txt"
    logic_lm_chain = LogicLMChain(kb_path)

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


    solution = logic_lm_chain.solve(description)

    print("\nFinal Derived Facts:")
    for pred, args in solution:
        print(f"{pred}({', '.join(args)})")

if __name__ == "__main__":
    main()
