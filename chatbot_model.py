import json
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

lemmatizer = WordNetLemmatizer()

# Load intents
with open('intents.json') as file:
    data = json.load(file)

intents = data['intents']
classes = [intent['tag'] for intent in intents]
patterns = []
responses = {}

# Process intents
for intent in intents:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        responses[pattern] = intent['responses']

# Create training data
X_train = patterns
y_train = [intent['tag'] for intent in intents for _ in intent['patterns']]

# Vectorize text
vectorizer = CountVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)

# Train model
model = MultinomialNB()
model.fit(X_train_vectors, y_train)

def classify_intent(text):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)[0]
    return prediction

def respond_to_intent(text):
    intent = classify_intent(text)
    return responses.get(text, ["I'm not sure how to respond to that."])
