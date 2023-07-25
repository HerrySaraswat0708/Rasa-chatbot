from flask import Flask, request, jsonify
from rasa.core.agent import Agent
import asyncio
from flask_cors import CORS

app = Flask(__name__)
CORS(app,origin='https://d10c-203-81-241-102.ngrok-free.app/rasa/webhook')

def load_rasa_model():
    agent = Agent.load('../models/20230722-144221-mean-momentum.tar.gz')
    return agent

agent=load_rasa_model()

def handle_text_synchronously(message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(agent.handle_text(message))
    return response

@app.route("/rasa/webhook", methods=["POST"])
def rasa_webhook():
    try:
        data = request.get_json()
        message = data["message"]
        response = handle_text_synchronously(message)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    html_content="<h1>Hello</h1>"
    return html_content,200,{'Content-Type':'text/html'}

if __name__ == "__main__":
    print('Server is listening at port 80')
    app.run(host='localhost',port=80)
