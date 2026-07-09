# ==========================================
# Student Performance Prediction System
# Mini Project - Week 6
# ==========================================

# Step 1: Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

print("=" * 50)
print("STUDENT PERFORMANCE PREDICTION SYSTEM")
print("=" * 50)

# Step 2: Load Dataset
print("\nLoading Dataset...")

df = pd.read_csv("dataset/student_data.csv")

print("Dataset Loaded Successfully!")
print("\nFirst 5 Rows:")
print(df.head())

# Step 3: Check Missing Values
print("\nChecking Missing Values...")
print(df.isnull().sum())

# Step 4: Split Features and Target
X = df[["StudyHours", "Attendance", "Assignments"]]
y = df["Pass"]

# Step 5: Split Train and Test Data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# Step 6: Train Logistic Regression Model
print("\nTraining Model...")

model = LogisticRegression()

model.fit(X_train, y_train)

print("Model Trained Successfully!")

# Step 7: Test Model Accuracy
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy : {accuracy*100:.2f}%")

# Step 8: Save Model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/student_model.pkl")

print("Model Saved Successfully!")

# Step 9: Take User Input
print("\n========== Enter Student Details ==========")

study_hours = float(input("Study Hours: "))
attendance = float(input("Attendance (%): "))
assignments = float(input("Assignment Marks: "))

# Step 10: Predict Result
prediction = model.predict([[study_hours, attendance, assignments]])

print("\n========== Prediction ==========")

if prediction[0] == 1:
    print("Result : PASS ✅")
else:
    print("Result : FAIL ❌")