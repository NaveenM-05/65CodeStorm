import pandas as pd

# Read CSV file
try:
    data = pd.read_csv('dataset.csv')
    print("✅ CSV file loaded successfully!")
except FileNotFoundError:
    print("❌ Error: CSV file not found. Please check the file path.")

# Display first 5 rows
print("\nFirst 5 rows:")
print(data.head())

# Print shape of the data
print(f"\nDataset contains {data.shape[0]} rows and {data.shape[1]} columns.")

# Print column names
print("\nColumn names:", data.columns.tolist())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Check for duplicates
duplicates = data.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicates}")

# Drop duplicates (optional, recommended)
if duplicates > 0:
    data = data.drop_duplicates()
    print(f"\nDuplicates removed. New shape: {data.shape}")

# Check class distribution (important for classification)
print("\nClass distribution:")
print(data['label'].value_counts())
