from flask import Flask, jsonify, request, json
import openai

class hello:
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
        @self.app.route('/openai', methods=['POST'])
        def openai_api():
            data = json.loads(request.data)
            print(data['requests']['objective'])

            response = openai.ChatCompletion.create(
                engine="dorkupinetreeGPT35",
                messages=[
                    {"role": "system",
                     "content": "You are an analyzer and summarizer system that takes the following input : \n" +
                                "1. Details : " + data['requests']['objective'] + "\n" +
                                "2.Objective : " + data['requests']['details'] + "\n" +
                                "3. metrics : [{\"ObyVi\" : \"This means total users who've placed an order divided by (total users who visited the platform)},{\"AOV\":\"This is the average sale made by users on the platform\"},{\"Cancellation\" : \"Users who cancel an order\"},{\"Return rate\" : \"Users who've returned an order\"},{\"Seller_exp\" : \"Bad seller experience\"},{\"First time app open date\" : \"When did the user first came to the platform?\"}]"},
                    {"role": "user",
                     "content": "provide the only metrics that will be closely impacted for the given details and objective from list of metrics provided. Also provide set of minimum 5 very very simple questions that must be asked to the customer of my e-commerce platform. The questions that I want to ask should just be around the details and objective that I've mentioned above (and nothing generic) Remember that my customers are extremely not tech savvy. PLease make simple questions that are easy for the user but important for me. Adapt the response in below format and add questions in key lod_deeds of response format. The response should be strictly in format"
                     "{\"Response\": \n"
                                " {\n" +
                                "    \"metrics\": [\n" +
                                "        {\n" +
                                "            \"name\": \"\",\n" +
                                "            \"domain\": \"\"\n" +
                                "            \"sql_query\": \"\"\n" +
                                "        }\n" +
                                "    ],\n" +
                                "    \"lod_deeds\": [\n" +
                                "        \"\"\n" +
                                "    ],\n" +
                                "    \"key\": \"\"\n" +
                                "} "},

                ],
                temperature=0.2,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            print(response)
            ct = response.choices[0].message.content
            return ct

    def run(self, host='0.0.0.0', port=5031):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    my_app = hello()
    my_app.run()