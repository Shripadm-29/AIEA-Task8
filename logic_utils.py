# utils/logic_utils.py

import re                        # lets us use regular expressions for splitting text
from collections import defaultdict  # lets us create dictionaries with default values
from itertools import product    # lets us generate all combinations of items

# Function: check_logic_validity
def check_logic_validity(logic_text):
    errors = []  # make a list to store errors we find
    # go through each line in the logic text, removing extra spaces and splitting by line breaks
    for line in logic_text.strip().split('\n'):
        stripped = line.strip()  # remove spaces at start and end of the line
        # check if the line ends with a period
        if not stripped.endswith('.'):
            errors.append("Missing period at end.")
        # check if the line has parentheses
        if '(' not in stripped or ')' not in stripped:
            errors.append("Missing parentheses.")
    return errors  # return all the problems we found

# Function: split_predicates
def split_predicates(body_text):
    # This splits text into separate predicates by commas
    # but ignores commas that are inside parentheses
    return [x.strip() for x in re.split(r',\s*(?![^()]*\))', body_text)]

# Class: LogicSolver
class LogicSolver:
    def __init__(self):
        # when we create a LogicSolver, we start with no facts and no rules
        self.facts = []
        self.rules = []

    # Method: parse_logic
    def parse_logic(self, logic_text):
        # clear out any old facts and rules
        self.facts.clear()
        self.rules.clear()

        # split the text into lines
        lines = logic_text.strip().split('\n')
        for line in lines:
            # remove spaces and periods at the end
            line = line.strip().strip('.')
            # skip empty lines
            if not line:
                continue
            # if the line has ":-" then it’s a rule
            if ':-' in line:
                self.rules.append(line)
            else:
                # otherwise, it’s a fact (something like parent(john, mary))
                if '(' in line and ')' in line:
                    # split into the predicate (like "parent") and the arguments (like "john, mary")
                    predicate, args = line.split('(')
                    args = args.strip(')').split(',')  # remove the ) and split by commas
                    # store the fact as (predicate, [list of arguments])
                    self.facts.append((predicate.strip(), [arg.strip() for arg in args]))
                else:
                    # if it doesn’t look like a valid fact, skip it
                    print(f"Skipping invalid line: {line}")

        # Auto-add symmetric sibling facts
        new_sibling_facts = []
        for pred, args in self.facts:
            # if we find "sibling(X, Y)" we also add "sibling(Y, X)"
            if pred == "sibling" and len(args) == 2:
                reversed_fact = ("sibling", [args[1], args[0]])
                # only add if it’s not already in the list
                if reversed_fact not in self.facts:
                    new_sibling_facts.append(reversed_fact)
        # add the new sibling facts
        self.facts.extend(new_sibling_facts)

    # Method: solve_logic
    def solve_logic(self, logic_text):
            # first parse the text into facts and rules
            self.parse_logic(logic_text)

            # print the facts for debugging
            print("\nFacts:")
            for pred, args in self.facts:
                print(f"{pred}({', '.join(args)})")

            # print the rules for debugging
            print("\nRules:")
            for rule in self.rules:
                print(rule)

            # put facts into a dictionary grouped by predicate
            fact_dict = defaultdict(list)
            for predicate, args in self.facts:
                fact_dict[predicate].append(args)

            derived_facts = set()  # store new facts we figure out

            # go through each rule
            for rule in self.rules:
                # split the rule into head and body
                # Example: parent(X,Y) :- mother(X,Y)
                head, body = rule.split(':-')

                # separate the head predicate and its arguments
                head_predicate, head_args = head.strip().split('(')
                head_args = [h.strip() for h in head_args.strip(')').split(',')]

                # clean up the body (conditions)
                body = body.strip()
                if body.startswith('(') and body.endswith(')'):
                    body = body[1:-1]  # remove outer parentheses

                # split the body into its smaller predicates
                body_predicates = split_predicates(body)
                body_preds = []
                for b in body_predicates:
                    pred_name, pred_args = b.split('(')
                    pred_args = [arg.strip() for arg in pred_args.strip(')').split(',')]
                    body_preds.append((pred_name.strip(), pred_args))

                # collect all sets of facts that match the body predicates
                fact_sets = []
                for pred_name, pred_vars in body_preds:
                    fact_sets.append(fact_dict.get(pred_name, []))

                # try every possible combination of facts to see if they match
                for fact_combo in product(*fact_sets):
                    var_bindings = {}  # map variables (like X, Y) to actual values
                    match = True
                    # check each predicate in the body
                    for (pred_vars, fact_args) in zip([bp[1] for bp in body_preds], fact_combo):
                        for var, val in zip(pred_vars, fact_args):
                            # if variable is already bound, check if it matches
                            if var in var_bindings:
                                if var_bindings[var] != val:
                                    match = False
                                    break
                            else:
                                # if not bound yet, assign it
                                var_bindings[var] = val
                        if not match:
                            break
                    # if everything matched, create a new fact
                    if match:
                        result = tuple(var_bindings.get(var.strip(), '?') for var in head_args)

                        # skip if it’s something like sibling(X,X)
                        if result[0] != result[1]:
                            derived_facts.add((head_predicate, result))

            return derived_facts  # return all the new facts we found

