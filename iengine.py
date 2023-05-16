def parse_input(filename):
    with open(filename, 'r') as f:
        content = [line.strip() for line in f.read().split('\n')]

    tell_index = content.index('TELL')
    ask_index = content.index('ASK')

    knowledge_base = content[tell_index+1:ask_index]
    query = content[ask_index+1:][0]

    # Split the knowledge base into individual propositions
    knowledge_base = [item.strip() for sublist in knowledge_base for item in sublist.split(';') if item]

    return knowledge_base, query
