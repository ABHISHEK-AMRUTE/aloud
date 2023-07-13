from flask import Flask, jsonify
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
        @self.app.route('/openai', methods=['GET'])
        def openai_api():
            response = openai.ChatCompletion.create(
                engine="dorkupinetreeGPT35",
                messages=[
                    {"role": "system", "content": "You are an analyzer and summarizer system that takes the following input : \n" +
                "1. Details : I've run a new A/B experiment on my e-commerce platform. I'm showing different delivery dates to different users and I want to check the impact on buying behaviour of my users.\n" +
                "2.Objective : There are three variants that I'm testing. Control group to which I show same delivery date as the platform, test-1 for which I've reduced 1 delivery day and for test-2 I've reduced 2 delivery dates. But what is constant is the actual delivery date. Now I want to understand  how does changing perception of delivery date impact the users' buying behaviour.\n" +
                "3. metrics : [{\"ObyVi\" : \"This means total users who've placed an order/ (total users who visited the platform)},{\"AOV\":\"This is the average sale made by users on the platform\"},{\"Cancellation\" : \"Users who cancel an order\"},{\"Return rate\" : \"Users who've returned an order\"}]"},
                    {"role": "user", "content": "prepare the 2 responses  in sequence as mentioned based on the problem objective and details: \n" +
                "1) json output as below\n" +
                "metrics : [\n" +
                "{\n" +
                "\t\"metric_name\" : \"\",\n" +
                "\t\"metric domain\" : \"\", //allowed values : product, technical, bussiness\n" +
                "\t\"sql_query\" : \"\"\n" +
                "}\n" +
                "]\n" +
                "\n" +
                "2) set of minimum 5 questions that must be asked to the consumer about the feature to get its insight."},

                ],
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            return response

    def run(self, host='0.0.0.0', port=5039):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    my_app = hello()
    my_app.run()