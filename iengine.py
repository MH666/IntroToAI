import sys

def parse_input(filename):
    with open(filename, 'r') as f:
        content = [line.strip() for line in f.read().split('\n')]

    tell_index = content.index('TELL')
    ask_index = content.index('ASK')

    raw_knowledge_base = content[tell_index+1:ask_index]
    query = content[ask_index+1:][0]

    # Parse the knowledge base into a list of rules
    knowledge_base = []
    for item in raw_knowledge_base[0].split(';'):
        if '=>' in item:  # This is a rule
            body, head = item.split('=>')
            body = frozenset(body.split('&')) if '&' in body else frozenset([body.strip()])
            head = head.strip()
            knowledge_base.append((body, head))
        else:  # This is a fact
            knowledge_base.append((frozenset(), item.strip()))

    return knowledge_base, query

def forward_chaining(KB, query):
    count = {}  # count of the number of unknowns in each implication
    inferred = {}  # which symbols have been inferred
    agenda = []  # symbols known to be true but not yet processed

    # Initialize data structures
    for rule in KB:
        body, head = rule
        count[rule] = len(body)
        inferred[head] = False

    # Add known facts to the agenda
    for rule in KB:
        body, head = rule
        if len(body) == 0:
            agenda.append(head)

    # Main loop
    while agenda:
        p = agenda.pop(0)
        if p == query:
            return True
        if not inferred[p]:
            inferred[p] = True
            for rule in KB:
                body, head = rule
                if p in body:
                    count[rule] -= 1
                    if count[rule] == 0:
                        agenda.append(head)

    return False

def backward_chaining(KB, query):
    return bc_recursive(KB, query, [])

def bc_recursive(KB, query, inferred):
    if [rule for rule in KB if rule[1] == query and len(rule[0]) == 0]:  # The query is a known fact
        return True
    elif query in inferred:  # The query has already been inferred
        return True
    else:
        rules = [rule for rule in KB if rule[1] == query]  # Get rules that conclude the query
        for rule in rules:
            if all(bc_recursive(KB, p, inferred + [query]) for p in rule[0]):  # Check if all premises of the rule can be inferred
                return True
        return False


def truth_table(knowledge_base, query):
    # Implement Truth Table inference
    pass


def main():
    method = sys.argv[1]
    filename = sys.argv[2]

    knowledge_base, query = parse_input(filename)

    if method == 'TT':
        result = truth_table(knowledge_base, query)
    elif method == 'FC':
        result = forward_chaining(knowledge_base, query)
    elif method == 'BC':
        result = backward_chaining(knowledge_base, query)
    else:
        print('Invalid method')
        return

    print(result)


if __name__ == '__main__':
    main()
