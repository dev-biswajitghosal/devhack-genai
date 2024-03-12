from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini import generate_content

app = Flask(__name__)
CORS(app)


@app.route('/api/auth', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        if 'Authorization' in request.headers:
            auth_token = request.headers['Authorization']
            print("Authorization token:", auth_token)
        else:
            return jsonify({'message': 'Authorization token not found.'}), 401
        request_data = request.get_json()
        prompt = request_data.get('prompt')
        print(prompt)
        response = generate_content(prompt)
        print(response)
        return jsonify({'response': response})
    else:
        return jsonify({"message": 'Please Provide Auth Key'})


if __name__ == '__main__':
    app.run(debug=True)
