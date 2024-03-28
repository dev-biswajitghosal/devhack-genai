from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from S3_bucket import get_file_from_s3, upload_file_to_s3
from llm_model import generate_content_from_documents,generate_content
from weatherAPI import get_weather_alerts
from auth import authenticate

app = Flask(__name__)
CORS(app)

host = "https://devhack-genai.onrender.com"


@app.route('/')
def index():
    return render_template('index.html', host=host)


@app.route('/api/analyze_risk_profile', methods=['POST'])
def analyze_risk_profile():
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization']
        is_authenticated = authenticate(auth_token)
        if not is_authenticated:
            return jsonify({'message': 'Please Give Correct API Key'}), 401
        category = request.form.get('category')
        industry = request.form.get('industry') or "any"
        zip_code = request.form.get('zip')
        state = request.form.get('state')
        age = request.form.get('age') or "any"
        policy_number = request.form.get('policyNumber')
        claims_data = request.form.get('claimsdata')
        if category in ["safety", "regulations", "vicinity"]:
            if category == "vicinity":
                weather_data = get_weather_alerts()
                if weather_data is None:
                    return jsonify({'message': 'Unable to fetch the Vicinity data.'}), 400
                prompt = (f"Summarise the headlines,description ,instruction of the following data {weather_data} in "
                          f"50 words .")
                response = generate_content(prompt)
                upload_file_to_s3(data=response, category=category, industry=industry, state=state)
                return jsonify({'response': response}), 200
            else:
                response = generate_content_from_documents(category=category, industry=industry, state=state, age=age,
                                                           zip_code=zip_code, policy_number=policy_number,
                                                           claims_data=claims_data)
                if response is not None:
                    return response, 200
                else:
                    return jsonify({'message': f'NO {category} for today.'}), 400
        else:
            return jsonify({'message': 'Please Give Correct Category'}), 400
    else:
        return jsonify({'message': 'Please Give API Key'}, 401)


@app.route('/api/get_genai_data', methods=['POST'])
def get_genai_data():
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization']
        is_authenticated = authenticate(auth_token)
        if not is_authenticated:
            return jsonify({'message': 'Please Give Correct API Key'}), 401
        # get body data
        category = request.get_json().get('category')
        if category == "safety":
            response = get_file_from_s3("safety/")
            return jsonify({'data': response}), 200
        elif category == "regulations":
            response = get_file_from_s3("regulations/")
            return jsonify({'data': response}), 200
        elif category == "vicinity":
            response = get_file_from_s3("vicinity/")
            return jsonify({'data': response}), 200
        else:
            return jsonify({'message': 'Please Give Correct Category'}), 400
    else:
        return jsonify({'message': 'Please Give an API Key'}, 401)


if __name__ == '__main__':
    app.run(debug=True)
