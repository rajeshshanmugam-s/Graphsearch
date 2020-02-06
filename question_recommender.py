import yaml

def suggestion_finder(query, id):
    stream = open('Data/'+id+'.yml')
    docs = yaml.load_all(stream)
    questions = []
    for intents in docs:
        for intent in intents['utterances']:
            if query in intent:
                questions.append(intent)
    return {"questions":questions}