import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Diseases_and_Symptoms_dataset.csv")

print("Loading dataset from:", DATA_PATH)

# Load dataset
df = pd.read_csv(DATA_PATH)
df = df.drop_duplicates()

X = df.drop("diseases", axis=1)
y = df["diseases"]

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.3, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print("Accuracy:", acc)

# Save model & encoder
joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
joblib.dump(le, os.path.join(BASE_DIR, "label_encoder.pkl"))

print("model.pkl and label_encoder.pkl saved successfully")











