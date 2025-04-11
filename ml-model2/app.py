from flask import Flask, request, jsonify
import pickle
import re

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Text cleaning function
def clean_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        message = data.get('message', '')

        if not message.strip():
            return jsonify({'error': 'No message provided'}), 400

        # Clean the input message
        cleaned_message = clean_text(message)

        # Vectorize the cleaned message
        vectorized_message = vectorizer.transform([cleaned_message])

        # Predict
        prediction = model.predict(vectorized_message)[0]

        # If you want to split department and category (optional, if format is "Department - Category")
        if ' - ' in prediction:
            department, category = prediction.split(' - ', 1)
            response = {
                'department': department,
                'category': category
            }
        else:
            response = {'prediction': prediction}

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check route (optional, good for testing server is running)
@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'API is running!'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
