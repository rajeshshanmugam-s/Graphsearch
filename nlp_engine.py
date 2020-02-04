from snips_nlu import SnipsNLUEngine
from snips_nlu.dataset import Dataset

engine = SnipsNLUEngine()
intents = Dataset.from_yaml_files('en', ['data/summa.yml'])
engine.fit(intents.json)


def intents_generator(query):
    input_data = engine.parse(query)
    intents = engine.get_intents(query)
    column_name = intents[0]['intentName']
    print(column_name)
    print(input_data)
    print(intents)
    return input_data, intents, column_name


intents_generator("what are the age in data")
