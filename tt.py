import re
import itertools

# Create the knowledge base from a txt file
def readKB(filename):
    with open(filename) as file:
        for line in file:
            line = line.strip()

            # Read in the knowledge base
            if line == "TELL":
                line = file.readline().strip().replace(" ", "")
                kb = line.split(";")
                kb = list(filter(None, kb))

            # Read in the query to ask
            elif line == "ASK":
                line = file.readline()
                query = line.strip()

    return kb, query

# This creates a Truth Table
def generateTT(kb):
    statements = [] # List to store individual statements
    tt = {} # Dictionary to store truth table

    # Extracts statements from KB
    for argument in kb:
        temp = re.split("&|=>", argument)
        for temp in temp:
            if temp not in statements:
                statements.append(temp)

    # Create values for TT
    values = list(itertools.product([0, 1], repeat=len(statements)))
    size = range(len(values))

    # Initialize truth table dictionary with empty lists for each statement
    for statement in statements:
        tt[statement] = []
    # Populate the truth table with corresponding truth values for each statement
    for values in values:
        for i, value in enumerate(values):
            tt[statements[i]].append(value)

     # Evaluate the truth values of arguments based on the truth values of its parameters
    for argument in kb:
        if "=>" in argument:
            tt[argument] = []
            parameters = re.split("&|=>", argument)
            for i in size:
                argumentvalue = 1
                if tt[parameters[-1]][i] == 0:
                    argumentsvalues = []
                    for argumentparam in parameters[:-1]:
                        argumentsvalues.append(tt[argumentparam][i])
                    if all(argumentsvalues):
                        argumentvalue = 0
                tt[argument].append(argumentvalue)

    # Evaluate the truth value of the final statement (conjunction of all statements in the knowledge base)
    finalstatement = "^".join(kb)
    tt[finalstatement] = []
    for i in size:
        argumentvalue = 1
        for argument in kb:
            if tt[argument][i] == 0:
                argumentvalue = 0
        tt[finalstatement].append(argumentvalue)

    return tt

# Ask the truth table the query
def truth_table(kb, query):
    model_count = 0
    tt = generateTT(kb)
    kb = list(tt)[-1]  # Get the final statement from the truth table

    # Check if the query is true when the kb is true - if query is not true function returns, if both KB and query true, counts  the number of true instances of the query in the truth table
    for i, value in enumerate(tt[kb]):
        if value == 1:
            if tt[query][i] == 0:
                print("NO")
                return
            else:
                model_count += 1
    
    # Print the number of true instances of the query
    print(f"YES: {model_count}")
    return



#OLD DO NO USE

"""
def boolean_to_string(value):
    if value:
        return "YES"
    else:
        return "NO"
"""

"""
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
"""

"""
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
"""

"""
def generate_models(symbols, model):
    if not symbols:
        yield model
    else:
        symbol, *remaining_symbols = symbols
        for value in [True, False]:
            new_model = model.copy()
            new_model[symbol] = value
            yield from generate_models(remaining_symbols, new_model)
"""

"""
def tt_entails(KB, query):
    modelCount = 0
    symbols = list(set(symbol for clause in KB + [query] for symbol in clause[1]))
    for model in generate_models(symbols, {}):
        all_true = all(evaluate_expression(clause[0], model) for clause in KB)
        if all_true and not evaluate_expression(query[0], model):
            return False
        modelCount += 1
    return True, modelCount
"""

"""def truth_table(filename):
	input_file = (filename)
	KB, query = convert_to_horn_notation(input_file)
	entailed, model_count = tt_entails(KB, query)
	return entailed, model_count
"""


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


# Knowledge Base in Horn form
"""
KB = [
    (['implies', 'p2', 'p3'], ['p2', 'p3']),
    (['implies', 'p3', 'p1'], ['p3', 'p1']),
    (['implies', 'c', 'e'], ['c', 'e']),
    (['implies', ['and', 'f', 'g'], 'h'], ['f', 'g', 'h']),
    (['implies', ['and', 'b', 'e'], 'f'], ['b', 'e', 'f']),
    (['implies', 'p1', 'd'], ['p1', 'd']),
    (['implies', ['and', 'p1', 'p3'], 'c'], ['p1', 'p3', 'c']),
    (['a'], []),    
    (['b'], []),    
    (['p2'], [])
]
"""

# Query
"""
query = (['d'], [])
input_file = "test1.txt"
KB, query = convert_to_horn_notation(input_file)
"""

# Check entailment
"""
#entailed, model_count = tt_entails(KB, query)
#answer = boolean_to_string(entailed)
#print(f"{answer}:{model_count}")  # Output: True if the query is entailed by the KB, False otherwise
"""
