from flask import Flask, request
import twilio.twiml
from requests import get
from re import match
import cgi
import os

app = Flask(__name__)

answer_dict =   {
                    "hi"            :   "Thanks for checking out Cheeky City Bot!",
                    "where am i"    :   "Code for America Office!",
                    "set my alarm"  :   "Sorry, I'm not Siri"
                };

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
    geocode_url = u"https://maps.googleapis.com/maps/api/geocode/json?&address=%s&key=%s&sensor=false" % (location, os.environ["GOOGLE_MAPS_KEY"])
    resp_json = get(geocode_url).json()

    coords = resp_json['results'][0]['geometry']['location']
    lat = coords['lat']
    lng = coords['lng']

    # Get specific food options based on coordinates
    # geocode_url

    return resp_json
    
 
if __name__ == "__main__":
    app.run(debug=True)
