def boolean_to_string(value):
    if value:
        return "YES"
    else:
        return "NO"

def convert_to_horn_notation(input_file):
    KB = []
    query = None
    inQuery = False
    
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            
            # Skip empty lines or comments (with TELL)
            if not line or line.startswith("#") or line.startswith("TELL"):
                continue
            
            # Check if line is a query (with ASK)
            if line.startswith("ASK"):
                inQuery = True
                continue
            
            # Checks line after query
            if inQuery: 
                inQuery = False
                query = ([line], [])
                continue

            # Split line into implications
            implications = line.split(";")
            for implication in implications:
                implication = implication.strip()
                
                # Split implication into antecedent and consequent
                arrow_index = implication.find("=>")

                if arrow_index < 0:
                    if len(implication) > 0:
                        KB.append(([implication], []))
                else:
                    antecedent_str = implication[:arrow_index].strip()
                    consequent = implication[arrow_index+2:].strip()
                    
                    # Handle conjunction in antecedent
                    if "&" in antecedent_str:
                        antecedent = ['and'] + antecedent_str.split("&")
                        antecedent2 = antecedent_str.split("&")
                    else:
                        antecedent = [antecedent_str]
                        antecedent2 = antecedent
                    
                    # Create KB tuple with 'implies' operator and add to KB list
                    KB.append((['implies', antecedent, consequent], antecedent2 + [consequent]))
    
    return KB, query

def evaluate_expression(expression, model):
    if isinstance(expression, str):
        return model[expression]
   
    operator, *operands = expression
   
    if operator == 'not':
        return not evaluate_expression(operands[0], model)
    elif operator == 'and':
        return all(evaluate_expression(operand, model) for operand in operands)
    elif operator == 'or':
        return any(evaluate_expression(operand, model) for operand in operands)
    elif operator == 'implies':
        return (not evaluate_expression(operands[0], model)) or evaluate_expression(operands[1], model)

def generate_models(symbols, model):
    if not symbols:
        yield model
    else:
        symbol, *remaining_symbols = symbols
        for value in [True, False]:
            new_model = model.copy()
            new_model[symbol] = value
            yield from generate_models(remaining_symbols, new_model)

def tt_entails(KB, query):
    modelCount = 0
    symbols = list(set(symbol for clause in KB + [query] for symbol in clause[1]))
    for model in generate_models(symbols, {}):
        all_true = all(evaluate_expression(clause[0], model) for clause in KB)
        if all_true and not evaluate_expression(query[0], model):
            return False
        modelCount += 1
    return True, modelCount



def truth_table(filename):
	input_file = (filename)
	KB, query = convert_to_horn_notation(input_file)
	entailed, model_count = tt_entails(KB, query)
	return entailed, model_count

"""
def main():
    method = sys.argv[1]
    filename = sys.argv[2]
    model_count = 0

    if method == 'TT': 
        result, model_count = truth_table(filename)
    else:
        knowledge_base, query = parse_input(filename)
        if method == 'FC':
            result = forward_chaining(knowledge_base, query)
        elif method == 'BC':
            result = backward_chaining(knowledge_base, query)
        else:
            print('Invalid method')
            return

    print(result)
"""





#OLD DO NO USE
# Knowledge Base in Horn form
# KB = [
#    (['implies', 'p2', 'p3'], ['p2', 'p3']),
#    (['implies', 'p3', 'p1'], ['p3', 'p1']),
#    (['implies', 'c', 'e'], ['c', 'e']),
#    (['implies', ['and', 'f', 'g'], 'h'], ['f', 'g', 'h']),
#    (['implies', ['and', 'b', 'e'], 'f'], ['b', 'e', 'f']),
#    (['implies', 'p1', 'd'], ['p1', 'd']),
#    (['implies', ['and', 'p1', 'p3'], 'c'], ['p1', 'p3', 'c']),
#    (['a'], []),    
#    (['b'], []),    
#    (['p2'], [])
#]

# Query
#query = (['d'], [])
#input_file = "test1.txt"
#KB, query = convert_to_horn_notation(input_file)

# Check entailment
#entailed, model_count = tt_entails(KB, query)
#answer = boolean_to_string(entailed)
#print(f"{answer}:{model_count}")  # Output: True if the query is entailed by the KB, False otherwise
