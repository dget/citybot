# Download the twilio-python library from http://twilio.com/docs/libraries
from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

answer_dict =	{
								"Hi, How Are You": "Thanks for checking out Cheeky City Bot!",
								"Where Am I": "Code for America Office!",
								"Set my alarm": "Sorry, I'm not Siri"
							};

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    rcv_msg = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    resp_msg = "Sorry, I don't have any information!"
    if answer_dict.has_key(rcv_msg) :
    	resp_msg = dict[rcv_msg]

    resp.message(resp_msg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

