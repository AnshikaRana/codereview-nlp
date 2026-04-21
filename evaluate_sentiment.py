import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from sklearn.model_selection import train_test_split
from transformers import pipeline

# -------------------------
# Load Sentiment Model
# -------------------------
pipe = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("sentiment_test.csv", quotechar='"')

# Dev/Test Split
dev_df, test_df = train_test_split(
    df,
    test_size=0.6,
    stratify=df["label"],
    random_state=42
)

# -------------------------
# Predict on Test Set
# -------------------------
predictions = []

for text in test_df["comment"]:
    pred = pipe(text)[0]["label"]
    predictions.append(label_map[pred])

true_labels = test_df["label"].tolist()

# -------------------------
# Metrics
# -------------------------
acc = accuracy_score(true_labels, predictions)
report = classification_report(true_labels, predictions)
cm = confusion_matrix(true_labels, predictions, labels=["negative","neutral","positive"])

print("="*50)
print("FINAL SENTIMENT MODEL EVALUATION")
print("="*50)
print(f"Accuracy: {acc:.2f}\n")
print(report)
print("Confusion Matrix:")
print(cm)

# -------------------------
# Save Text Report
# -------------------------
with open("evaluation_report.txt", "w") as f:
    f.write("FINAL SENTIMENT MODEL EVALUATION\n")
    f.write("="*50 + "\n")
    f.write(f"Accuracy: {acc:.2f}\n\n")
    f.write(report)
    f.write("\nConfusion Matrix:\n")
    f.write(str(cm))

# -------------------------
# Plot Confusion Matrix
# -------------------------
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["negative","neutral","positive"]
)

disp.plot()
plt.title("Sentiment Confusion Matrix")
plt.savefig("confusion_matrix.png")
plt.show()

# -------------------------
# Bar Chart
# -------------------------
scores = classification_report(
    true_labels,
    predictions,
    output_dict=True
)

classes = ["negative","neutral","positive"]
f1_scores = [scores[c]["f1-score"] for c in classes]

plt.figure(figsize=(8,5))
plt.bar(classes, f1_scores)
plt.title("F1 Score by Class")
plt.ylim(0,1)
plt.savefig("f1_scores.png")
plt.show()

print("\nFiles Generated:")
print("evaluation_report.txt")
print("confusion_matrix.png")
print("f1_scores.png")