import re

def tt_entails_user_input(KB_sentences, query):
    # Get all symbols from KB and query
    symbols = set()
    for sentence in KB_sentences + [query]:
        symbols.update(extract_symbols(sentence))
    symbols = list(symbols)

    return tt_check_all(KB_sentences, query, symbols, {})


def tt_check_all(KB, alpha, symbols, model):
    if not symbols:
        # If KB is true in this model, check if alpha is true
        if pl_true(KB, model):
            return pl_true([alpha], model)
        else:
            return True  # if KB is false, then it doesn't matter
    else:
        P = symbols[0]
        rest = symbols[1:]

        model_true = model.copy()
        model_true[P] = True

        model_false = model.copy()
        model_false[P] = False

        return (tt_check_all(KB, alpha, rest, model_true)
                and tt_check_all(KB, alpha, rest, model_false))


def pl_true(sentence_set, model):
    for sentence in sentence_set:
        if not evaluate(sentence, model):
            return False
    return True


def extract_symbols(sentence):
   
    tokens = re.findall(r'[A-Za-z_][A-Za-z_0-9]*', sentence)
    logical_ops = {"and", "or", "not", "implies", "iff", "true", "false"}
    # Also exclude operators used like '->', '~' etc, but they won't match this regex
    symbols = set(t for t in tokens if t.lower() not in logical_ops)
    return symbols


def evaluate(expr, model):
    """
    Evaluate the propositional logic expression 'expr' under the assignment in 'model'.
    Supports:
    - Symbols (variables)
    - Negation: ~
    - And: &
    - Or: |
    - Implication: ->
    - Biconditional: <->
    Parentheses are supported.
    """
   
    expr = expr.replace('<->', '<=>') 
    expr = expr.replace('->', '=>')
    expr = expr.replace('<=>', '==') 
    expr = expr.replace(' ', '')

    def parse_expr(s):
        
        while '(' in s:
            
            p = re.search(r'\([^()]*\)', s)
            if not p:
                break
            inner = p.group()[1:-1]
            val = parse_expr(inner)
            s = s[:p.start()] + ('T' if val else 'F') + s[p.end():]

       
        s = eval_negation(s)

     
        if '==' in s:
            parts = split_top_level(s, '==')
            return all(parse_expr(part) == parse_expr(parts[0]) for part in parts[1:])

        
        if '=>' in s:
            parts = split_top_level(s, '=>')
           
            for i in range(len(parts) - 1):
                if not (not parse_expr(parts[i]) or parse_expr(parts[i+1])):
                    return False
            return True

       
        if '|' in s:
            parts = split_top_level(s, '|')
            return any(parse_expr(part) for part in parts)

    
        if '&' in s:
            parts = split_top_level(s, '&')
            return all(parse_expr(part) for part in parts)

        if s == 'T':
            return True
        if s == 'F':
            return False
     
        if s in model:
            return model[s]
        else:
          
            return False

    def eval_negation(s):
      
        while True:
            m = re.search(r'~[TF]', s)
            if not m:
                break
            val = m.group()
            if val == '~T':
                s = s[:m.start()] + 'F' + s[m.end():]
            elif val == '~F':
                s = s[:m.start()] + 'T' + s[m.end():]
    
        m = re.search(r'~[A-Za-z_][A-Za-z_0-9]*', s)
        while m:
            sym = m.group()[1:]
            val = model.get(sym, False)
            val = not val
            s = s[:m.start()] + ('T' if val else 'F') + s[m.end():]
            m = re.search(r'~[A-Za-z_][A-Za-z_0-9]*', s)
        return s

    def split_top_level(s, delimiter):
        """
        Split expression s by delimiter, but only at top-level (not inside T/F or inside nested expressions).
        Since we've removed parentheses already, splitting by delimiter directly is safe.
        """
        parts = []
        depth = 0
        last = 0
        for i in range(len(s)):
            if s[i] == '(':
                depth += 1
            elif s[i] == ')':
                depth -= 1
            elif depth == 0 and s.startswith(delimiter, i):
                parts.append(s[last:i])
                last = i + len(delimiter)
        parts.append(s[last:])
        return parts

    return parse_expr(expr)


def main():
    print("Enter KB sentences (enter blank line to finish):")
    KB = []
    while True:
        line = input().strip()
        if line == '':
            break
        KB.append(line)

    query = input("Enter query sentence:\n").strip()

    result = tt_entails_user_input(KB, query)

    if result:
        print("KB entails Query (KB ⊨ Query)")
    else:
        print("KB does NOT entail Query (KB ⊭ Query)")


if __name__ == "__main__":
    main()
