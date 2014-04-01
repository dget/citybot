from flask import Flask, request
import twilio.twiml
from requests import get
from re import match
import cgi
import os
import json

app = Flask(__name__)

answer_dict = json.load(open('questions.json'))

@app.route("/", methods=['GET', 'POST'])
def respond_to_question():
    """Respond to text questions with an answer."""
    rcv_msg = request.values.get('Body', None).lower()
    if "where" in rcv_msg and "taco" in rcv_msg:
        location = match(r".+in\s+(.+)", rcv_msg).group(1)
        resp_msg = go_find_taco(location)
    else:
        resp_msg = "Sorry, I don't have any information!"
        if rcv_msg in answer_dict:
            resp_msg = answer_dict[rcv_msg]

    resp = twilio.twiml.Response()
    resp.message(resp_msg)
    return str(resp)

def go_find_taco(location):
    location = cgi.escape(location)
    geocode_url = u"https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s&sensor=false" % (location, os.environ["GOOGLE_MAPS_KEY"])
    resp_json = get(geocode_url).json()

    coords = resp_json['results'][0]['geometry']['location']
    lat = coords['lat']
    lng = coords['lng']

    # Get specific food options based on coordinates
    # geocode_url

    restaurant_url = u"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=500000&types=food&name=taco&sensor=false&key=%s" % (lat, lng, os.environ["GOOGLE_PLACES_KEY"])
    restaurant_json = get(restaurant_url).json()

    restaurant_name = restaurant_json['results'][0]['name'];
    vicinity = restaurant_json['results'][0]['vicinity'];

    return "go to here: " + restaurant_name + " " + vicinity
    
 
if __name__ == "__main__":
    app.run(debug=True)
