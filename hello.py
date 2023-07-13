from flask import Flask, jsonify
import openai

class AutoPrompt:
    def __init__(self):
        self.app = Flask(__name__)

        # Set OpenAI API credentials
        openai.api_key = 'e20507358b0042cdb8cc04f70b0311ba'
        openai.api_type = "azure"
        openai.api_base = "https://hackmee2.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"

        # Route for health API
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'OK'})

        # Route for OpenAI API integration
        @self.app.route('/openai', methods=['GET'])
        def openai_api():
            response = openai.ChatCompletion.create(
                engine="dorkupinetreeGPT35",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that helps people find information."},
                    {"role": "user", "content": "How are you"},
                    {"role": "assistant",
                     "content": "As an AI language model, I do not have feelings or emotions. However, I am functioning well and ready to assist you with any queries or tasks you may have. How can I assist you today?"}
                ],
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            return response

    def run(self, host='0.0.0.0', port=5011):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    my_app = AutoPrompt()
    my_app.run()