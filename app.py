from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from gemini import generate_content
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
            prompt = f"Find healthcare providers near the location {zip_code},{state},{city}"
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
        else:
            industry = request.form.get('industry')
            zip_code = request.form.get('zip')
            state = request.form.get('state')
            city = request.form.get('city')
            age = request.form.get('age')
            prompt = (f"Analyze the risk profile for {industry} industry for the location of {zip_code},{state},{city}"
                      f" and the people of age {age}.")
            response = generate_content(prompt)
            return jsonify({'response': response}), 200
    else:
        return jsonify({'message': 'Please Give API Key'}, 401)


if __name__ == '__main__':
    app.run(debug=True)
