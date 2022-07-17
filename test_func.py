import spacy
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL")

WEATHER_API_URL = f"{WEATHER_API_BASE_URL}/current.json?key={WEATHER_API_KEY}&aqi=no"


nlp = spacy.load('en_core_web_md')

known_intents = [
    {
        "intent": 'greet',
        "possibles": ['Hello', 'Hi', 'Good morning',
                      "How's it going?", "How are you doing?"]
    },
    {
        "intent": 'get_weather',
        "possibles": ["How's the weather like in Rome?", "What is the weather in London?",
                      "How's the weather in Bangkok?", "What's the weather like in Los Angeles?", "Weather in city", "weather boston", "weather new york", "city", "London", "Dublin", "Boston", "Boston weather"]
    }
]


def get_and_format_weather(query):
    res = requests.get(f"{WEATHER_API_URL}&q={query}")
    # print(res.text)
    weather_data = json.loads(res.text)

    country = weather_data['location']['country']
    city = weather_data['location']['name']
    cur_condition_text = weather_data['current']['condition']['text']
    cur_temp_c = weather_data['current']['temp_c']
    cur_temp_f = weather_data['current']['temp_f']

    return f"{cur_condition_text} @ {cur_temp_c}°C ({cur_temp_f}°F) in {city}, {country}"
    # return json.loads(res.text)


last_petition = ''


def chatbot(inputStr, expected=""):
    global last_petition
    # TODO: Add previous messages to memory
    # TODO: Automatically check if there is a GPE in the statement, if there is, automatically get the weather for it

    min_similarity = 0.7

    statement = nlp(inputStr)

    result = ''
    max_similarity = 0
    similar_to = ""

    print(len(statement.ents))

    if(len(statement.ents)):
        for ent in statement.ents:
            # TODO: Add check for previous weather petition without city
            # if ent.label_ == 'GPE' and last_petition == 'weather_without_city':
            if ent.label_ == 'GPE':
                # last_petition = ''
                return get_and_format_weather(ent)

    for intentObj in known_intents:
        for possibility in intentObj['possibles']:
            if statement.similarity(nlp(possibility)) > max_similarity:
                max_similarity = statement.similarity(nlp(possibility))
                similar_to = possibility
                if statement.similarity(nlp(possibility)) > min_similarity:
                    result = intentObj['intent']

    result = "I didn't understand that. Can you rephrase it?" if len(
        result) == 0 else result

    if result == 'greet':
        return 'Hello to you!'

    if result == 'get_weather':
        if not len(statement.ents):
            return "You'll need to specify a city"

        for ent in statement.ents:
            if ent.label_ == 'GPE':
                return get_and_format_weather(ent)
            else:
                # last_petition = 'weather_without_city'
                return "You'll need to specify a city"

    return "I didn't quite get that. Could you try and rephrase it?"


# print(chatbot('Hi', 'greet'))
# print(chatbot('Ahoy', 'greet'))
# print(chatbot('Weather in Venice', 'get_weather'))
# print(chatbot('Current weather in LA', 'get_weather'))
# print(chatbot('weather china', 'get_weather'))
# print(chatbot('weather Beijing', 'get_weather'))
# print(chatbot('weather Michigan', 'get_weather'))
# print(chatbot('Michigan', 'get_weather'))
# print(chatbot("What's up?", 'greet'))
# print(chatbot("How's the weather like?", 'get_weather'))
print(chatbot("What about Sydney?", 'get_weather'))

# TODO: Add more functions, news?
# i.e.: "Latest news about trump"
# Recognize "Latest", "news", "trump"
# Get via NewsAPI with query "trump" ordered by latest
# i.e.: "Blockchain news"
# Recognize "Blockchain", "news"
# Get relevant news with query "blockchain"
# and so on...
