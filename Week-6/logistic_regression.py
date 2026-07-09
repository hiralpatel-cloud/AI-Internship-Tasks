import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

print("="*60)
print("MODEL TRAINING & EVALUATION")
print("="*60)

# Step 2: Load preprocessed data
print("\n1. Loading Preprocessed Data...")
print("-"*40)

# Load training data
X_train = pd.read_csv('data/X_train.csv')
X_test = pd.read_csv('data/X_test.csv')
y_train = pd.read_csv('data/y_train.csv').values.ravel()
y_test = pd.read_csv('data/y_test.csv').values.ravel()

print(f" Data loaded successfully!")
print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Step 3: Train Logistic Regression
print("\n2. Training Logistic Regression...")
print("-"*40)

# Create Logistic Regression model
logreg = LogisticRegression(max_iter=1000, random_state=42)

# Train the model
logreg.fit(X_train, y_train)

# Make predictions
y_pred_logreg = logreg.predict(X_test)

# Calculate accuracy
accuracy_logreg = accuracy_score(y_test, y_pred_logreg)

print(f"✅ Logistic Regression trained!")
print(f"Accuracy: {accuracy_logreg:.4f}")

# Save the model
joblib.dump(logreg, 'models/logistic_regression_model.pkl')
print("✅ Model saved to 'models/logistic_regression_model.pkl'")

# Step 4: Train Decision Tree
print("\n3. Training Decision Tree...")
print("-"*40)

# Create Decision Tree model
dt = DecisionTreeClassifier(random_state=42, max_depth=5)

# Train the model
dt.fit(X_train, y_train)

# Make predictions
y_pred_dt = dt.predict(X_test)

# Calculate accuracy
accuracy_dt = accuracy_score(y_test, y_pred_dt)

print(f"✅ Decision Tree trained!")
print(f"Accuracy: {accuracy_dt:.4f}")

# Save the model
joblib.dump(dt, 'models/decision_tree_model.pkl')
print("✅ Model saved to 'models/decision_tree_model.pkl'")

# Step 5: Compare Models
print("\n4. Model Comparison...")
print("-"*40)

print("Accuracy Comparison:")
print(f"Logistic Regression: {accuracy_logreg:.4f}")
print(f"Decision Tree:      {accuracy_dt:.4f}")

if accuracy_logreg > accuracy_dt:
    print(f"\n🏆 Best Model: Logistic Regression with {accuracy_logreg:.4f} accuracy")
else:
    print(f"\n🏆 Best Model: Decision Tree with {accuracy_dt:.4f} accuracy")

# Step 6: Detailed Reports
print("\n5. Classification Reports...")
print("-"*40)

print("\nLogistic Regression Report:")
print(classification_report(y_test, y_pred_logreg, 
                          target_names=['setosa', 'versicolor', 'virginica']))

print("\nDecision Tree Report:")
print(classification_report(y_test, y_pred_dt, 
                          target_names=['setosa', 'versicolor', 'virginica']))

# Step 7: Save Results
print("\n6. Saving Results...")
print("-"*40)

# Save comparison results
results = pd.DataFrame({
    'Model': ['Logistic Regression', 'Decision Tree'],
    'Accuracy': [accuracy_logreg, accuracy_dt]
})
results.to_csv('results/model_comparison.csv', index=False)
print("✅ Results saved to 'results/model_comparison.csv'")

# Save detailed report
with open('results/model_results.txt', 'w') as f:
    f.write("MODEL EVALUATION RESULTS\n")
    f.write("="*50 + "\n\n")
    
    f.write("Logistic Regression:\n")
    f.write(f"  Accuracy: {accuracy_logreg:.4f}\n")
    f.write("  Classification Report:\n")
    f.write(classification_report(y_test, y_pred_logreg))
    f.write("\n" + "-"*40 + "\n")
    
    f.write("Decision Tree:\n")
    f.write(f"  Accuracy: {accuracy_dt:.4f}\n")
    f.write("  Classification Report:\n")
    f.write(classification_report(y_test, y_pred_dt))

print("✅ Detailed results saved to 'results/model_results.txt'")

# Step 8: Confusion Matrices
print("\n7. Confusion Matrices...")
print("-"*40)

print("Logistic Regression Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_logreg))

print("\nDecision Tree Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_dt))
