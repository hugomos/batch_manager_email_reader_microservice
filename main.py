# main.py
from flask import Flask, request
from flask_cors import CORS
from app.auth import authenticate
from app.email_reader import fetch_emails

app = Flask(__name__)
CORS(app)

@app.route('/emails', methods=['POST'])
def get_emails():
    input_data = request.get_json()
    email = input_data.get('email')
    password = input_data.get('password')

    if not authenticate(email, password):
        return {"error": "Autenticação falhou."}, 401

    emails = fetch_emails()
    return {"data": emails}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
