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
        item = item.strip()  # Strip each item
        if item:  # Only process the item if it's not empty
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
    inferred_symbols = []  # order of inferred symbols

    # Initialize data structures
    for rule in KB:
        body, head = rule
        inferred[head] = False
        if len(body) == 0:  # this is a fact
            inferred[head] = True
            if head not in agenda:  # add only if not already in the agenda
                agenda.append(head)
            inferred_symbols.append(head)
        else:
            # count only those body items that are not yet inferred
            count[rule] = len([item for item in body if item not in inferred_symbols])

    # Main loop
    while agenda:
        p = agenda.pop(0)  # popping from the front, treating agenda as a queue
        if p == query:
            return True, inferred_symbols
        for rule in KB:
            body, head = rule
            if p.strip() in body and not inferred[head]:  # check if p is in the body and head is not inferred yet
                count[rule] -= 1
                if count[rule] == 0:  # all symbols in the body are true
                    inferred[head] = True
                    if head not in agenda:  # add only if not already in the agenda
                        agenda.append(head)
                    inferred_symbols.append(head)

    return False, inferred_symbols


def backward_chaining(KB, query):
    return bc_recursive(KB, query, [])


def bc_recursive(KB, query, inferred):
    if query in inferred:  # The query has already been inferred
        return True, []
    else:
        rules = [rule for rule in KB if rule[1] == query]  # Get rules that conclude the query
        for rule in rules:
            all_true = True  # boolean flag to track if all premises are true
            inferred_symbols = []  # list to collect inferred symbols for each rule
            for p in rule[0]:
                result, symbols = bc_recursive(KB, p, inferred + [query])
                inferred_symbols += symbols
                if not result:
                    all_true = False
                    break  # No need to continue checking other premises
            if all_true:  # All premises of the rule can be inferred
                return True, inferred_symbols + [query]
        return False, []

def truth_table(knowledge_base, query):
    # Implement Truth Table inference
    pass


def main():
    method = sys.argv[1]
    filename = sys.argv[2]

    knowledge_base, query = parse_input(filename)

    if method == 'TT':
        result, inferred = truth_table(knowledge_base, query)
    elif method == 'FC':
        result, inferred = forward_chaining(knowledge_base, query)
    elif method == 'BC':
        result, inferred = backward_chaining(knowledge_base, query)
        inferred.reverse()  # Reverse the order of inferred symbols in BC
    else:
        print('Invalid method')
        return

    print('YES' if result else 'NO', ':', ', '.join(inferred) if inferred else 'None')



if __name__ == '__main__':
    main()
