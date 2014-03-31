# Download the twilio-python library from http://twilio.com/docs/libraries
from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

answer_dict =	{
                    "hi"            :   "Thanks for checking out Cheeky City Bot!",
                    "where am i"    :   "Code for America Office!",
					"set my alarm"  :   "Sorry, I'm not Siri"
				};

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    rcv_msg = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    resp_msg = "Sorry, I don't have any information!"
    if rcv_msg.lower() in answer_dict:
    	resp_msg = answer_dict[rcv_msg]

    resp.message(resp_msg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

