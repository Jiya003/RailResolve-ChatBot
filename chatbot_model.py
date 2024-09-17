import numpy as np
import random
import json
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

class ChatbotModel:
    def _init_(self, intents_file):
        self.intents_file = intents_file
        self.model = None
        self.words = []
        self.classes = []
        self.intents = self.load_intents()

    def load_intents(self):
        with open(self.intents_file) as file:
            return json.load(file)

    def preprocess_data(self):
        patterns, labels = [], []

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                words = pattern.split()
                self.words.extend(words)
                patterns.append(pattern)
                labels.append(intent['tag'])
            if intent['tag'] not in self.classes:
                self.classes.append(intent['tag'])

        self.words = sorted(set(self.words))
        self.classes = sorted(set(self.classes))

        return patterns, labels

    def train_model(self):
        patterns, labels = self.preprocess_data()

        # Convert text to numerical data
        label_encoder = LabelEncoder()
        labels = label_encoder.fit_transform(labels)

        # Create a simple neural network model
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, input_shape=(len(self.words),), activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(len(self.classes), activation='softmax')
        ])

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.fit(np.array(patterns), np.array(labels), epochs=200, batch_size=8)

    def classify(self, text):
        input_data = [text.split()]
        prediction = self.model.predict(input_data)
        return prediction
