# from flask import Flask, request, jsonify
# import pickle
# import re

# # Initialize Flask app
# app = Flask(__name__)

# # Load the trained model and vectorizer
# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)

# with open('vectorizer.pkl', 'rb') as f:
#     vectorizer = pickle.load(f)

# # Text cleaning function
# def clean_text(text):
#     text = text.lower()  # Lowercase
#     text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
#     text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
#     return text

# # Define prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json(force=True)
#         message = data.get('message', '')

#         if not message.strip():
#             return jsonify({'error': 'No message provided'}), 400

#         # Clean the input message
#         cleaned_message = clean_text(message)

#         # Vectorize the cleaned message
#         vectorized_message = vectorizer.transform([cleaned_message])

#         # Predict
#         prediction = model.predict(vectorized_message)[0]

#         # If you want to split department and category (optional, if format is "Department - Category")
#         if ' - ' in prediction:
#             department, category = prediction.split(' - ', 1)
#             response = {
#                 'department': department,
#                 'category': category
#             }
#         else:
#             response = {'prediction': prediction}

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Health check route (optional, good for testing server is running)
# @app.route('/', methods=['GET'])
# def health():
#     return jsonify({'status': 'API is running!'})

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import pickle
import re

app = Flask(__name__)
# Enable CORS for all routes; optionally, specify the allowed origins.
CORS(app, origins=["http://127.0.0.1:3000"])

# Load your trained model and vectorizer (if applicable)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def clean_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        message = data.get('message', '')

        if not message.strip():
            return jsonify({'error': 'No message provided'}), 400

        cleaned_message = clean_text(message)
        vectorized_message = vectorizer.transform([cleaned_message])
        prediction = model.predict(vectorized_message)[0]

        if ' - ' in prediction:
            department, category = prediction.split(' - ', 1)
            response = {'department': department, 'category': category}
        else:
            response = {'prediction': prediction}

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-log', methods=['GET'])
def get_log():
    try:
        # Assume service_request.log is at the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file_path = os.path.join(base_dir, "service_request.log")
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                log_data = f.read()
            return Response(log_data, mimetype="text/plain")
        else:
            return jsonify({"error": "Log file not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'API is running!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
