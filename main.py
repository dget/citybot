from flask import Flask, request
import twilio.twiml

app = Flask(__name__)

answer_dict =   {
                    "hi"            :   "Thanks for checking out Cheeky City Bot!",
                    "where am i"    :   "Code for America Office!",
                    "set my alarm"  :   "Sorry, I'm not Siri"
                };

@app.route("/", methods=['GET'])
def respond_to_question():
    """Respond to incoming calls with a simple text message."""

    rcv_msg = request.values.get('Body', None).lower()
    resp = twilio.twiml.Response()
    resp_msg = "Sorry, I don't have any information!"
    if rcv_msg in answer_dict:
        resp_msg = answer_dict[rcv_msg]

    resp.message(resp_msg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
