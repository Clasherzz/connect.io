from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from transformers import AutoTokenizer, AutoModel
import torch
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import requests

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

GEMINI_API_URL = "https://api.google.com/gemini/embedding"
HEADERS = {
    "Authorization": "Bearer YOUR_GEMINI_API_KEY",
    "Content-Type": "application/json"
}

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    text = extract_text_from_pdf(file)
    embeddings = embed_text(text)
    filename = file.filename
    store_embeddings(filename, embeddings)
    return jsonify({"status": "success"})

@app.route('/query', methods=['POST'])
def query():
    query_text = request.json['query']
    query_embedding = embed_text(query_text, single=True)
    results = query_embeddings(query_embedding)
    response = generate_response(results, query_text)
    return jsonify({"result": response})

if __name__ == '__main__':
    app.run(debug=True)
