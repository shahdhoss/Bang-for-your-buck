import pandas as pd
import joblib
from .text_cleaning import cleaned_text

def load(message,file):
    cleaned_x=cleaned_text(message)
    vectorizer=joblib.load("vectorizer.joblib")
    x = vectorizer.transform(cleaned_x).toarray()
    loaded_clf = joblib.load(file)
    prediction = loaded_clf.predict(x)
    return prediction

def predicts(product1,product2):
    x = pd.DataFrame({
        'product1': [product1],
        'product2': [product2]
    })
    prediction = load(x,'bangfybuck.joblib')
    return prediction
