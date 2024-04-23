from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import gensim.downloader as api
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')


app = Flask(__name__)

# Load DataFrames and TF-IDF vectorizer
df = pd.read_csv('nytimes_articles.csv')
with open('embeddings_vec.pkl', 'rb') as f:
    embeddings_vec = pickle.load(f)

model = api.load("word2vec-google-news-300")

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())  # Convert to lowercase and tokenize

    # Stopword removal
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    return stemmed_tokens

def generate_word_embeddings(words):
    embeddings = []
    model = api.load("word2vec-google-news-300")
    for word in words:
        try:
            embeddings.append(model[word])
        except KeyError:
            # If word not in vocabulary, ignore or handle accordingly
            pass
    return embeddings

def calculate_average_embedding(embeddings):
    if not embeddings:
        # If no embeddings found, return None or zeros
        return np.zeros(model.vector_size)
    return np.mean(embeddings, axis=0)

# Function to preprocess query and compute cosine similarity
def get_top_k_articles(query, k=5):
    # Preprocess query
    processed_query = preprocess_text(query)
    
    query_embeddings = generate_word_embeddings(processed_query)
    avg_query_embeddings = calculate_average_embedding(query_embeddings)
    
    similarities = cosine_similarity(avg_query_embeddings.reshape(1, -1), embeddings_vec.tolist())
    top_indices =  similarities.argsort()[0][-k:][::-1]
    top_articles = df.iloc[top_indices][['headline', 'article']]
    return top_articles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    top_k = int(request.args.get('top', 5))
    top_articles = get_top_k_articles(query, top_k)
    top_articles = top_articles[['headline', 'article']]
    # print(top_articles.to_dict(orient='records'))
    return top_articles.to_dict(orient='records') #render_template('result.html', top_articles=top_articles.to_dict(orient='records'))

# from flask import request
# import json

# @app.route('/result')
# def result():
#     data = request.args.get('data')
#     if data:
#         data = json.loads(data)
#         return render_template('result.html', data=data)
#     else:
#         return "No data received"

if __name__ == '__main__':
    app.run(debug=True)