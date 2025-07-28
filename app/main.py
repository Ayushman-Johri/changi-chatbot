from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ 1. Yeh line add karo
from .chatbot import get_answer

app = Flask(__name__)
CORS(app)  # ✅ 2. Yeh line add karo (app = Flask... ke theek neeche)

@app.route('/ask', methods=['POST'])
def ask_question():
    json_data = request.get_json()
    if not json_data or 'question' not in json_data:
        return jsonify({"error": "Request body mein 'question' field missing hai."}), 400

    question = json_data['question']
    response = get_answer(question)

    formatted_response = {
        "answer": response.get('result'),
        "source_documents": [doc.to_json() for doc in response.get('source_documents', [])]
    }
    return jsonify(formatted_response)

@app.route("/", methods=['GET'])
def root():
    return jsonify({"message": "Chatbot API is running!"})