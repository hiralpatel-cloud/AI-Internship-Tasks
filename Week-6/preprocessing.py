
# Step 1: Import libraries
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

print("="*60)
print("DATA LOADING & PREPROCESSING")
print("="*60)

# Step 2: Load dataset
print("\n1. Loading Iris Dataset...")
iris = load_iris()

# Create DataFrame
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target

print("✅ Dataset loaded!")
print(f"Shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# Step 3: Handle missing values
print("\n2. Handling Missing Values...")
print(f"Missing values:\n{df.isnull().sum()}")
print("✅ No missing values found!")

# Step 4: Encode categorical data
print("\n3. Encoding Categorical Data...")
# Species is already encoded (0, 1, 2) in iris dataset
# But we'll show how to do it
le = LabelEncoder()
df['species_encoded'] = le.fit_transform(df['species'])

print("✅ Categorical data encoded")
print(f"Original: {df['species'].head().tolist()}")
print(f"Encoded: {df['species_encoded'].head().tolist()}")

# Step 5: Split data
print("\n4. Splitting Data...")
X = df.drop(['species', 'species_encoded'], axis=1)  # Features
y = df['species_encoded']  # Target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ Data split complete!")
print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Step 6: Save data
print("\n5. Saving Data...")
X_train.to_csv('data/X_train.csv', index=False)
X_test.to_csv('data/X_test.csv', index=False)
y_train.to_csv('data/y_train.csv', index=False)
y_test.to_csv('data/y_test.csv', index=False)

print("✅ Files saved in 'data' folder!")

# Step 7: Summary
print("\n" + "="*60)
print("✅ PREPROCESSING COMPLETE!")
print("="*60)
print("\nFiles created:")
print("  📊 data/X_train.csv")
print("  📊 data/X_test.csv")
print("  📊 data/y_train.csv")
print("  📊 data/y_test.csv")