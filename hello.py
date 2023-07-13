from flask import Flask, jsonify, request, json
import openai
import sqlite3

class hello:
    def __init__(self):
        self.app = Flask(__name__)
        self.initialise_DB()
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

        @self.app.route('/summarizer', methods=['POST'])
        def summarizer_api():

            business_feature = "give your feature"

            data = json.loads(request.data)
            type_of_summary = data['requests']['type_of_summary'];
            cohort = data['requests']['cohort'];

            con = sqlite3.connect("tutorial.db")
            cur = con.cursor()
            res = cur.execute("SELECT Q1,Q2,Q3,Q4,Q5,Q6,Q7 FROM qna WHERE ")
            query = res.fetchall()

            summaries = []

            for i in query:
                message = [
                    {"role": "system", "content": business_feature},
                    {"role": "assistant", "content": Q1},
                    {"role": "user", "content": i[0]},
                    {"role": "assistant", "content": Q2},
                    {"role": "user", "content": i[1]},
                    {"role": "assistant", "content": Q3},
                    {"role": "user", "content": i[2]},
                    {"role": "assistant", "content": Q4},
                    {"role": "user", "content": i[3]},
                    {"role": "assistant", "content": Q5},
                    {"role": "user", "content": i[4]},
                    {"role": "assistant", "content": Q6},
                    {"role": "user", "content": i[5]},
                    {"role": "assistant", "content": Q7},
                    {"role": "user", "content": i[6]},
                    {"role": "system", "content": "Summarize"}
                ]

                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    engine="dorkupinetreeGPT35",
                    messages=messages,
                    temperature=0.2,
                    max_tokens=1200,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )

                summaries = summaries + [response.choices[0]["message"]["content"]]

            combined_summary = ""

            for s in summaries:
                combined_summary = combined_summary + s + "\n"

            response = openai.ChatCompletion.create(
                engine="dorkupinetreeGPT35",
                messages=[
                    {"role": "system",
                     "content": "There are three variants that I'm testing. Control group to which I show same delivery date as the platform, test-1 for which I've reduced 1 delivery day and for test-2 I've reduced 2 delivery dates. But what is constant is the actual delivery date. Now I want to understand  how does changing perception of delivery date impact the users' buying behaviour."},
                    {"role": "user", "content": combined_summary},
                    {"role": "system",
                     "content": "Summarize the above conversation between assistant and user with respect to the content provided earlier to the system. Also provide a separate section of recomendataion on what can be improved in the feature"}
                ],
                temperature=0,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None)

            return response


    def run(self, host='0.0.0.0', port=5039):
        self.app.run(host=host, port=port)


    def initialise_DB(self):
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE qna (User_ID,Gender,Tier,Legacy,User Type,App Opens,Orders placed,Dispatched,Delivered,Returned,GMV,Q1,Q2,Q3,Q4,Q5,Q6,Q7)")

        cur.execute("""
                INSERT INTO qna VALUES (1, 'Male', 'Gold', 'No', 'New User', 12, 4, 4, 4, 0, 50, 'Yes', 'No', 4, 5, 'I prefer faster delivery as it affects my decision to purchase.', 'No, I don''t return the order even if it''s delivered late.', 'No, I don''t cancel my orders if the delivery date is high for me. I wait for the delivery.'),
        (2, 'Female', 'Silver', 'No', 'Returning User', 20, 8, 8, 7, 1, 120.5, 'Yes', 'Yes', 3, 4, 'Delivery date plays a minor role in my buying decision.', 'Yes, if the order is significantly delayed, I might consider returning it.', 'No, I rarely cancel orders based on delivery date.'),
        (3, 'Male', 'Bronze', 'Yes', 'New User', 5, 2, 1, 1, 0, 15.2, 'No', 'No', 2, 3, 'Delivery date doesn''t matter much to me.', 'No, I usually keep the order even if it''s late.', 'Yes, I cancel my orders if the delivery date is too high for me.'),
        (4, 'Female', 'Gold', 'No', 'Returning User', 32, 12, 12, 12, 0, 200.8, 'Yes', 'No', 5, 5, 'Delivery date is crucial for my purchasing decisions.', 'No, I don''t return the order even if it''s delivered late.', 'No, I don''t cancel my orders based on delivery date.'),
        (5, 'Male', 'Silver', 'Yes', 'New User', 8, 3, 3, 3, 0, 40, 'Yes', 'No', 4, 4, 'Delivery date has some influence on my buying behavior.', 'No, I don''t return the order even if it''s delivered late.', 'No, I rarely cancel orders due to delivery date.'),
        (6, 'Male', 'Bronze', 'No', 'New User', 10, 5, 4, 4, 1, 60.75, 'Yes', 'Yes', 3, 3, 'Delivery date doesn''t affect my buying decisions much.', 'Yes, if the order is significantly delayed, I might consider returning it.', 'No, I rarely cancel orders based on delivery date.'),
        (7, 'Female', 'Gold', 'No', 'Returning User', 28, 10, 10, 10, 0, 180.9, 'Yes', 'No', 5, 5, 'Delivery date is essential for me to make a purchase.', 'No, I don''t return the order even if it''s delivered late.', 'No, I don''t cancel my orders based on delivery date.'),
        (8, 'Male', 'Silver', 'Yes', 'New User', 15, 6, 6, 6, 0, 95.5, 'Yes', 'No', 4, 4, 'Delivery date plays a moderate role in my buying decision.', 'No, I don''t return the order even if it''s delivered late.', 'No, I rarely cancel orders based on delivery date.'),
        (9, 'Female', 'Bronze', 'Yes', 'Returning User', 18, 9, 9, 9, 1, 110.25, 'Yes', 'Yes', 3, 4, 'Delivery date slightly influences my purchasing decisions.', 'Yes, if the order is significantly delayed, I might consider returning it.', 'No, I rarely cancel orders due to delivery date.'),
        (10, 'Male', 'Gold', 'No', 'New User', 25, 11, 11, 11, 0, 160, 'Yes', 'No', 5, 5, 'Delivery date is a critical factor in my buying behavior.', 'No, I don''t return the order even if it''s delivered late.', 'No, I don''t cancel my orders based on delivery date.')
                """)


    def run(self, host='0.0.0.0', port=5031):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    my_app = hello()
    my_app.run()