import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load dataset
df = pd.read_csv('my_pickup_full_dataset.csv')

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Clean the 'message' column
df['message'] = df['message'].apply(clean_text)

# Prepare features and labels
X = df['message']
y = df['department'] + " | " + df['category']  # Combine labels

# Vectorization
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train the model
model = MultinomialNB()
model.fit(X_vectorized, y)

# Save the vectorizer
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model and vectorizer saved successfully!")
