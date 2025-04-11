import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK resources (only once)
nltk.download('stopwords')
nltk.download('wordnet')

# Read CSV file
try:
    data = pd.read_csv('dataset.csv')
    print("✅ CSV file loaded successfully!")
except FileNotFoundError:
    print("❌ Error: CSV file not found. Please check the file path.")

# Display first 5 rows
print("\nFirst 5 rows:")
print(data.head())

# Print shape and columns
print(f"\nDataset contains {data.shape[0]} rows and {data.shape[1]} columns.")
print("\nColumn names:", data.columns.tolist())

# Check missing values and duplicates
print("\nMissing values in each column:")
print(data.isnull().sum())
duplicates = data.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicates}")
if duplicates > 0:
    data = data.drop_duplicates()
    print(f"\nDuplicates removed. New shape: {data.shape}")

# Class distribution
print("\nClass distribution:")
print(data['label'].value_counts())

# =======================
# Text Preprocessing Step
# =======================

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# Apply preprocessing
data['cleaned_text'] = data['text'].apply(preprocess_text)
print("\nSample cleaned text:")
print(data[['text','cleaned_text']].head())

# =======================
# Feature Extraction Step
# =======================
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data['cleaned_text'])
print(f"\nTF-IDF feature matrix shape: {X.shape}")

# Labels
y = data['label']

# =======================
# Train-Test Split & Model Training
# =======================
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTraining data shape: {X_train.shape}, Test data shape: {X_test.shape}")

from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# =======================
# Evaluation
# =======================
from sklearn.metrics import accuracy_score, classification_report
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# =======================
# Save Model and Vectorizer
# =======================
import pickle
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)
print("\nModel and vectorizer saved to disk.")
