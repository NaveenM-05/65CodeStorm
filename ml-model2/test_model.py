import pickle
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the vectorizer and model
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Create a pipeline manually
from sklearn.pipeline import make_pipeline
pipeline = make_pipeline(vectorizer, model)

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Prediction function
def predict_dept_cat(message):
    cleaned = clean_text(message)
    combined_label = pipeline.predict([cleaned])[0]  # ✅ fixed
    if ' | ' in combined_label:
        department, category = combined_label.split(' | ')
    else:
        department, category = combined_label, 'Unknown'
    return department, category

# Test message
if __name__ == "__main__":
    msg = "my bike is not charging properly"
    dept, cat = predict_dept_cat(msg)
    print(f"Department: {dept}")
    print(f"Category: {cat}")
