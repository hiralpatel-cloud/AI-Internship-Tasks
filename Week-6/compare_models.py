import pandas as pd
import matplotlib.pyplot as plt

print("="*60)
print("MODEL COMPARISON")
print("="*60)

# Load model comparison results
results = pd.read_csv("results/model_comparison.csv")

print("\nModel Results:")
print(results)

# Create graph
plt.figure(figsize=(8,5))

plt.bar(results["Model"], results["Accuracy"])

plt.title("Model Accuracy Comparison")
plt.xlabel("Models")
plt.ylabel("Accuracy")
plt.ylim(0,1.1)

# Save graph
plt.savefig("results/model_accuracy_comparison.png")

# Display graph
plt.show()

print("\nGraph saved successfully!")