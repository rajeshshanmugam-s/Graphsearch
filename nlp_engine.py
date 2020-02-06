from snips_nlu import SnipsNLUEngine
from snips_nlu.dataset import Dataset

engine = SnipsNLUEngine()

def intents_generator(query, id):
    intents = Dataset.from_yaml_files('en', ['Data/'+id+'.yml'])
    # Fixme: Should not be fitted for each request
    engine.fit(intents.json)
    input_data = engine.parse(query)
    intents = engine.get_intents(query)
    column_name = intents[0]['intentName']
    return input_data, intents, column_name


# intents_generator("what are the age in data")
