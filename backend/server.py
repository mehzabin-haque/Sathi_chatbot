from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

ASSISTANT_ID = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=os.getenv("API_KEY"))

app = Flask(__name__)
CORS(app)

def get_chat_response(user_input):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ]
    )
    print("Entered to backend")
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print("Running...")
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)
        print(run.status)
        # if(run.status == "failed"):
        #     continue
        
    
    print("Got the response")
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    latest_message = messages[0]
    return latest_message.content[0].text.value

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_input = data.get('message', '')
    response = get_chat_response(user_input)
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
