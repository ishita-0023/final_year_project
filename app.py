# app.py
from flask import Flask, render_template, request, jsonify
import gensim.downloader as api
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string
import nltk

app = Flask(__name__)

# Download required NLTK data

# Load Word2Vec model
w2v_model = api.load('word2vec-google-news-300')

# Recreate your model's architecture
def construct_model():
    model = Sequential()
    model.add(LSTM(300, dropout=0.4, recurrent_dropout=0.4, input_shape=(1, 300), return_sequences=True))
    model.add(LSTM(64, recurrent_dropout=0.4))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='relu'))
    return model

# Construct the model
model = construct_model()

# Load weights into the model
model.load_weights('my_model.h5')

# Compile the model after loading weights
model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mae'])

# Clean and preprocess the text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'$$.*?$$', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

def clean_stopwords(text):
    words = word_tokenize(text)
    return [word for word in words if word not in stopwords.words('english') and word.isalpha()]

def get_feature_vector(words, model, num_features=300):
    feature_vector = np.zeros((num_features,), dtype='float32')
    num_words = 0.
    index2word_set = set(model.index_to_key)

    for word in words:
        if word in index2word_set:
            num_words += 1
            feature_vector = np.add(feature_vector, model[word])

    if num_words > 0:
        feature_vector = np.divide(feature_vector, num_words)

    return feature_vector

def preprocess_essay(essay_text):
    cleaned_essay = clean_text(essay_text)
    cleaned_words = clean_stopwords(cleaned_essay)
    return get_feature_vector(cleaned_words, w2v_model).reshape(1, 1, 300)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grade', methods=['POST'])
def grade_essay():
    essay_text = request.form['essay']
    # For now, just return a dummy grade
    return jsonify({'grade': 5.0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)