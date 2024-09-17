import json
import numpy as np
import pickle as pk
import tensorflow as tf # type: ignore
from nltk.stem import WordNetLemmatizer
import nltk
import string
import random

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
nltk.download("punkt")
nltk.download("wordnet")

import pickle as pk
from sklearn.feature_extraction.text import CountVectorizer

#importing the json file
data_file=open('intents.json').read()
data=json.loads(data_file)

#the dataset has objects known as intents
#intents are having their own tags showing context,patterns and responese
#these intents will help us to reply to those statements.

# vectorizer
vectorizer = CountVectorizer()

# Save the vectorizer
#with open('vectorizer.pkl', 'wb') as f:
   # pk.dump(vectorizer, f)


#Creating data_X and data_Y
#using NLTK's WordNetLemmatizer(). This function will help
#us to reduce the words and convert it into their root words

words=[] #For Row model/ vocabulary for patterns
classes=[] #For Row model/vocalbulary for tags
data_X=[] #For storing each pattern
data_Y=[] #For storing tag corresponding to each pattern in data_X

#Iterating all intents in intents.json

for intent in data["intents"]:
  for pattern in intent["patterns"]:
    tokens=nltk.word_tokenize(pattern) #tokenizing each pattern
    words.extend(tokens) #appending tokens into words
    data_X.append(pattern) #appending pattern to data_X
    data_Y.append(intent["tag"]) #appending the associated tag to each pattern

  if intent["tag"] not in classes: #appending the tag if it is not present
    classes.append(intent["tag"])

lemmatizer=WordNetLemmatizer()
#lemmatizer to get the root of words
#turning everything into lowercase and removing all punctuations

words=[lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
#Sorting the vocabulary and classes into aplhabetical order
#checking if there are no duplicate orders

words=sorted(set(words))
classes=sorted(set(classes))

with open('vocab.pkl', 'wb') as f:
    pk.dump(words, f)

with open('classes.pkl', 'wb') as f:
    pk.dump(classes, f)

#Data TRAINING

#We are converting our text into numbers using BOW model(Bag of words)
#words and classes act as a vocabulary for patterns and tags respectively

#1 if the word is present in the pattern/tag being read(from data_X)
#0 if absent.

#Data will be converted into numbers
#stored into two arrays: train_X and train_Y respectively.


training=[]
out_empty=[0]*len(classes) #intializing

#Using BAG of model
for idx,doc in enumerate(data_X):
  bow=[]
  text=lemmatizer.lemmatize(doc.lower())
  for word in words:
    bow.append(1) if word in text else bow.append(0)


  output_row=list(out_empty)
  output_row[classes.index(data_Y[idx])]=1

  #adding the one hot encoded BOW and associated classes to traininhg

  training.append([bow, output_row])

#shuffling the data and converting it to an array

random.shuffle(training)
training=np.array(training,dtype=object)

#spliting the features and target_labels
train_X=np.array(list(training[:,0]))
train_Y=np.array(list(training[:,1]))


import tensorflow as tf
from tensorflow.keras.models import Sequential, save_model
from tensorflow.keras.layers import Dense, Dropout

# Defining the model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_X[0]),), activation='relu'))  
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_Y[0]), activation='softmax'))

# Defining the optimizer
adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)

# Compiling the model
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=['accuracy'])

# Printing the model summary
#debugging
print(model.summary())

# Training the model
model.fit(x=train_X, y=train_Y, epochs=150, verbose=1)

# Saving the model
save_model(model, 'my_model.keras')

# Loading the intents data
with open('intents.json','r',encoding='utf-8') as file:
    intents = json.load(file)

# Loading the model and vectorizer
model = tf.keras.models.load_model('my_model.keras')  # Load the neural network model
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pk.load(f)

lemmatizer = WordNetLemmatizer()

# Loading the vocabulary and classes
with open('vocab.pkl', 'rb') as f:
    words = pk.load(f)
with open('classes.pkl', 'rb') as f:
    classes = pk.load(f)

#preprocessing the text
def preprocess_input(text):
    """ Transform the input text into features using the vectorizer. """
    return vectorizer.transform([text])

#cleaning the text
def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = (lemmatizer.lemmatize(word.lower()) for word in tokens)
    return tokens

def bag_of_words(text, vocab):
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    return np.array(bow)

def pred_class(text, vocab, labels):
    bow = bag_of_words(text, vocab)
    result = model.predict(np.array([bow]))[0]  # Extracting the probabilities

    thresh = 0.5
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)
    
    return_list = [labels[r[0]] for r in y_pred]
    return return_list
def load_intents(filename='intents.json'):
    with open(filename, 'r') as file:
        return json.load(file)

intents_json = load_intents()
def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        return "Sorry! I didn't understand."
    tag = intents_list[0]
    for i in intents_json["intents"]:
        if i["tag"] == tag:
            return random.choice(i["responses"])
    return "Sorry! I didn't understand."
    
