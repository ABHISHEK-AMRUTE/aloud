from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Configure OpenAI
openai.api_type = "azure"
openai.api_base = "https://hackmee2.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "e20507358b0042cdb8cc04f70b0311ba"


@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json()

    # Extract values from the payload
    domain = payload.get('domain')
    key = payload.get('key')
    type_of_summary = payload.get('type_of_summary')
    cohort = payload.get('cohort')

    # Create the OpenAI chat message array
    messages = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."},
        {"role": "user", "content": "How are you"},
        {"role": "assistant", "content": "As an AI language model, I do not have feelings or emotions. However, I am functioning well and ready to assist you with any queries or tasks you may have. How can I assist you today?"}
    ]

    # Customize the messages based on the payload values
    # For example:
    if domain:
        messages[0]['content'] = f"You are an AI assistant that helps people in the {domain} domain."

    if key:
        messages[1]['content'] = key

    if type_of_summary:
        messages[2]['content'] = f"You asked for a {type_of_summary} summary."

    if cohort:
        messages[2]['content'] = f"You belong to the {cohort} cohort."

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        engine="dorkupinetreeGPT35",
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    return jsonify(response), 200