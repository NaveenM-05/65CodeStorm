# from flask import Flask, request, jsonify
# from flask_cors import CORS  # import this

# app = Flask(__name__)
# CORS(app)  # add this

# # your existing code
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     message = data['message']
#     # prediction logic
#     prediction = predict_category(message)
#     return jsonify({'label': prediction})

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})

# Load your trained model and vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data['message']

    # Preprocess and predict
    vect_message = vectorizer.transform([message])
    prediction = model.predict(vect_message)

    # Return prediction as JSON
    return jsonify({'category': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)

