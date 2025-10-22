from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np


def load_model():
    # Deterministic training for reproducibility
    iris = load_iris()
    X, y = iris.data, iris.target
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=200, random_state=42))
    ])
    pipe.fit(X, y)
    return pipe


def predict_proba(model, features):
    arr = np.array(features, dtype=float).reshape(1, -1)
    proba = model.predict_proba(arr)[0]
    label = int(np.argmax(proba))
    return label, proba.tolist()
