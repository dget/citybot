# Download the twilio-python library from http://twilio.com/docs/libraries
from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    rcvmsg = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    resp.message(rcvmsg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

