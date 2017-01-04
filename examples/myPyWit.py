import sys
import requests
import json
from wit import Wit

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]

# Quickstart example
# See https://wit.ai/ar7hur/Quickstart

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    print(response['text'])

def get_geolocation():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    return j

def get_forecast_from_open_weather_map(parameters):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather',params=parameters)
    data = json.loads(r.text)
    return data['weather'][0]['description']

def get_forecast(request):
    context = request['context']
    entities = request['entities']

    loc = first_entity_value(entities, 'location')
    dateTime = first_entity_value(entities,'datetime')

    if dateTime:
        j = get_geolocation()
        latitude = j['latitude']
        longitude = j['longitude']
        parameters = {'lat':latitude,'lon':longitude,'appid':'f12f195956d3533f7a8d78665cd69def'}
        context['futureForecast'] = get_forecast_from_open_weather_map(parameters)
        #context['futureForecast'] = 'windy'

    if loc and dateTime:
        context['futureForecastLoc'] = 'Rainy at Paris'

    if loc:
        parameters = {'q':loc,'appid':'f12f195956d3533f7a8d78665cd69def'}
        context['forecast'] = get_forecast_from_open_weather_map(parameters)
         #context['forecast']= 'sunny'
        if context.get('missingLocation') is not None:
            del context['missingLocation']
    else:
        context['missingLocation'] = True
        if context.get('forecast') is not None:
            del context['forecast']

    return context

actions = {
    'send': send,
    'getForecast': get_forecast,
}

client = Wit(access_token=access_token, actions=actions)
client.interactive()
