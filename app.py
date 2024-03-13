from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini import generate_content

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/get_healthcare_data', methods=['POST'])
def api():
    zip_code = request.form.get('zip')
    prompt = f"Find healthcare providers near {zip_code}"
    print(prompt)
    response = generate_content(prompt)
    print(response)
    return jsonify({'response': response})


@app.route('/api/analyze_risk_profile', methods=['POST'])
def generate():
    name = request.form.get('name')
    industry = request.form.get('industry')
    location = request.form.get('location')
    age = request.form.get('age')
    prompt = f"Analyze the risk profile for {name} in the {industry} industry in {location} at the age of {age}"
    response = generate_content(prompt)
    print(prompt)
    print(response)
    return jsonify({'response': response})


@app.route('/api/auth', methods=['POST'])
def auth():
    if 'Authorization' in request.headers:
        auth_token = request.headers['Authorization']
        print("Authorization token:", auth_token)
    else:
        return jsonify({'message': 'Authorization token not found.'}, 401)


if __name__ == '__main__':
    app.run(debug=True)
