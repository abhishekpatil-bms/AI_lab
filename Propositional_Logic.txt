
import re
from itertools import product

def pl_true(sentence, model):
    try:
        return eval(sentence, model)
    except NameError:
        return False

def tt_entails(kb, alpha):
    kb = kb.replace('¬', 'not ').replace('∧', ' and ').replace('∨', ' or ')
    alpha = alpha.replace('¬', 'not ').replace('∧', ' and ').replace('∨', ' or ')
    symbols = sorted(list(set(re.findall(r'[A-Z]', kb + alpha))))
   
    print(f"Symbols found: {symbols}")
    for values in product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        if pl_true(kb, model):
            if not pl_true(alpha, model):
                print(f"Counterexample found: {model}")
                return False
    return True
if __name__ == "__main__":
    kb_formula = "(A ∨ C) ∧ (B ∨ ¬C)"
    alpha_formula = "A ∨ B"
    print(f"Knowledge Base (KB): {kb_formula}")
    print(f"Query (α): {alpha_formula}\n")
    result = tt_entails(kb_formula, alpha_formula)
    print("\n------ RESULT ------")
    if result:
        print(f"The Knowledge Base entails the Query.")
        print(f"   '{kb_formula}' |= '{alpha_formula}'")
    else:
        print(f"The Knowledge Base does NOT entail the Query.")
        print(f"   '{kb_formula}' |/= '{alpha_formula}'")
