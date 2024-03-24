from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from S3_bucket import get_file_from_s3
from gemini import generate_content
from OpenAI import generate_content_from_documents
from auth import authenticate

app = Flask(__name__)
CORS(app)

host = "https://devhack-genai.onrender.com"


@app.route('/')
def index():
    return render_template('index.html', host=host)


@app.route('/api/get_healthcare_data', methods=['POST'])
def get_healthcare_data():
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization']
        is_authenticated = authenticate(auth_token)
        if not is_authenticated:
            return jsonify({'message': 'Please Give Correct API Key'}), 401
        else:
            zip_code = request.form.get('zip')
            state = request.form.get('state')
            city = request.form.get('city')
            if not zip_code and not state and not city:
                return jsonify({'message': 'Please Give Correct Location'}), 400
            prompt = f"Find healthcare providers near the location {city},{state},{zip_code}"
            response = generate_content(prompt)
            return jsonify({'response': response}), 200
    else:
        return jsonify({'message': 'Please Give API Key'}), 401


@app.route('/api/analyze_risk_profile', methods=['POST'])
def analyze_risk_profile():
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization']
        is_authenticated = authenticate(auth_token)
        if not is_authenticated:
            return jsonify({'message': 'Please Give Correct API Key'}), 401
        industry = request.form.get('industry') or "any"
        zip_code = request.form.get('zip')
        state = request.form.get('state')
        city = request.form.get('city')
        age = request.form.get('age') or "any"
        if not zip_code and not state and not city:
            return jsonify({'message': 'Please Give Correct Location'}), 400
        prompt = (f"Analyze the risk profile for {industry} industry for the location of {city},{state},{zip_code}"
                  f" and the people of age {age}. Give me the risk factors and the risk score. ")
        response = generate_content(prompt)
        return jsonify({'response': response}), 200

    else:
        return jsonify({'message': 'Please Give API Key'}, 401)


@app.route('/api/generate_genai_data', methods=['POST'])
def get_safety_tips():
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization']
        is_authenticated = authenticate(auth_token)
        if not is_authenticated:
            return jsonify({'message': 'Please Give Correct API Key'}), 401
        category = request.form.get('category')
        industry = request.form.get('industry') or "any"
        state = request.form.get('state')
        if category == "safety":
            prompt = f"Give me the safety tips for {industry} industry for {state}"
            response = generate_content_from_documents(prompt, prefix="safety/")
            if not response:
                return jsonify({'message': 'Unable to find matching results'}), 400
            return jsonify({'response': response}), 200
        elif category == "regulations":
            prompt = f"Give me the regulations for {industry} industry for {state}"
            response = generate_content_from_documents(prompt, prefix="regulations/")
            if not response:
                return jsonify({'message': 'Unable to find matching results'}), 400
            return jsonify({'response': response}), 200
        elif category == "vicinity":
            prompt = f"Give me the vicinity details for {industry} industry for {state}"
            response = generate_content_from_documents(prompt, prefix="vicinity/")
            if not response:
                return jsonify({'message': 'Unable to find matching results'}), 400
            return jsonify({'response': response}), 200
        else:
            return jsonify({'message': 'Please Give Correct Category'}), 400
    else:
        return jsonify({'message': 'Please Give an API Key'}, 401)


@app.route('/api/get_genai_data', methods=['POST'])
def get_genai_data():
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization']
        is_authenticated = authenticate(auth_token)
        if not is_authenticated:
            return jsonify({'message': 'Please Give Correct API Key'}), 401
        category = request.form.get('category')
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
