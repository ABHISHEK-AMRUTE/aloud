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
        @self.app.route('/openai', methods=['POST'])
        def openai_api():
            response = openai.ChatCompletion.create(
                engine="dorkupinetreeGPT35",
                messages=[
                    {"role": "system", "content": "You are an analyzer system that takes the following input : \n" +
                                                  "1. Details : I'm a product manager and I've run a new A/B experiment on my e-commerce platform. I'm showing different delivery dates to different users and I want to check the impact on behaviour of my users.\n" +
                                                  "2.Objective : There are three variants that I'm testing. Control group to which I show same delivery date as the platform, test-1 for which I've reduced 1 delivery day and for test-2 I've reduced 2 delivery dates. But what is constant is the actual delivery date. Now I want to understand how does changing perception of delivery date impact the users' buying behaviour.\n" +
                                                  "3. metrics : [{\"ObyVi\" : \"This means total users who've placed an order divided by (total users who visited the platform)},{\"AOV\":\"This is the average sale made by users on the platform\"},{\"Cancellation\" : \"Users who cancel an order\"},{\"Return rate\" : \"Users who've returned an order\"},{\"Seller_exp\" : \"Bad seller experience\"},{\"First time app open date\" : \"When did the user first came to the platform?\"}]"},
                    {"role": "user",
                     "content": "json output in below structure for the only metrics that will be closely impacted for the given details and objective from list of metrics provided\n" +
                                "metrics : [\n" +
                                "{\n" +
                                "\t\"metric_name\" : \"\",\n" +
                                "\t\"metric domain\" : \"\", //allowed values : product, technical, bussiness\n" +
                                "\t\"sql_query\" : \"\"\n" +
                                "}\n" +
                                "] . Also provide set of minimum 5 very very simple questions that must be asked to the customer of my e-commerce platform. The questions that I want to ask should just be around the details and objective that I've mentioned above (and nothing generic) Remember that my customers are extremely not tech savvy. PLease make simple questions that are easy for the user but important for me "},

                ],
                temperature=0.5,
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
