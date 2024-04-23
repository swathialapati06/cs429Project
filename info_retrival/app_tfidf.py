from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Load DataFrames and TF-IDF vectorizer
df = pd.read_csv('nytimes_articles.csv')
tfidf_df = pd.read_csv('tfidf_matrix.csv')
with open('tfidf_vectorizer.pkl', 'rb') as f:
    tfidf_vectorizer = pickle.load(f)

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
# Function to preprocess query and compute cosine similarity
def get_top_k_articles(query, k=5):
    # Preprocess query
    processed_query = ' '.join(preprocess_text(query))
    
    # Compute TF-IDF vector for query
    query_tfidf = tfidf_vectorizer.transform([processed_query])
    
    # Compute cosine similarity between query and articles
    cosine_sim = cosine_similarity(query_tfidf, tfidf_df)
    
    # Get indices of top k articles based on similarity scores
    top_indices = cosine_sim.argsort()[0][-k:][::-1]
    print("-----------------------",top_indices)
    # Get top k articles
    top_articles = df.iloc[top_indices]
    
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

from flask import request
import json

@app.route('/result')
def result():
    data = request.args.get('data')
    if data:
        data = json.loads(data)
        return render_template('result.html', data=data)
    else:
        return "No data received"

if __name__ == '__main__':
    app.run(debug=True)