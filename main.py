from flask import Flask, request
import twilio.twiml
from requests import get
from re import match

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
        location = re.match("in\s+(.+)").group(1)
        key = "schmows"
        go_find_taco(location, key)

    resp = twilio.twiml.Response()
    resp_msg = "Sorry, I don't have any information!"
    if rcv_msg in answer_dict:
        resp_msg = answer_dict[rcv_msg]

    resp.message(resp_msg)
    return str(resp)

def go_find_taco(location, key):
    geocode_url =
u"https://maps.googleapis.com/maps/api/geocode/json?&address=%skey=%s&sensor=false" % (location, key)
 
if __name__ == "__main__":
    app.run(debug=True)
