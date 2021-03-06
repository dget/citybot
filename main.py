from flask import Flask, request
import twilio.twiml
from requests import get
from re import match
import cgi
import os
import json
import random
from fuzzywuzzy import process

app = Flask(__name__)

answer_dict = json.load(open('questions.json'))
random_answers = ["What the what?", "Nerds!", "Blerg!"]

FUZZ_THRESHOLD = 80

@app.route("/", methods=['GET', 'POST'])
def respond_to_question():
    """Respond to text questions with an answer."""
    rcv_msg = request.values.get('Body', None).lower()
    if "taco" in rcv_msg and "near" in rcv_msg:
        location = match(r".+near\s+(.+)", rcv_msg).group(1)
        resp_msg = go_find_taco(location)
    else:
        random_index = random.randint(0,len(random_answers) - 1)
        resp_msg = random_answers[random_index]

        # Fuzzily match against questions
        top_question, top_score = process.extractOne(rcv_msg, answer_dict.keys())

        if top_score > FUZZ_THRESHOLD:
            resp_msg_arr = answer_dict[top_question]
            index = random.randint(0,len(resp_msg_arr) - 1)
            resp_msg = resp_msg_arr[index]

    resp = twilio.twiml.Response()
    resp.message(resp_msg)
    return str(resp)

def go_find_taco(location):
    location = cgi.escape(location)
    geocode_url = u"https://maps.googleapis.com/maps/api/geocode/json?address=%s, San Francisco, CA&key=%s&sensor=false&region=us" % (location, os.environ["GOOGLE_MAPS_KEY"])
    resp_json = get(geocode_url).json()

    coords = resp_json['results'][0]['geometry']['location']
    lat = coords['lat']
    lng = coords['lng']

    restaurant_url = u"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&rankby=distance&types=food&keyword=taco&sensor=false&key=%s" % (lat, lng, os.environ["GOOGLE_PLACES_KEY"])
    restaurant_json = get(restaurant_url).json()

    restaurants = restaurant_json['results'][0]
    restaurant_name = restaurant_json['results'][0]['name'];
    vicinity = restaurant_json['results'][0]['vicinity'];

    return "Here's where I go on hungry nights: " + restaurant_name + " @ " + vicinity
    
 
if __name__ == "__main__":
    app.run(debug=True)
