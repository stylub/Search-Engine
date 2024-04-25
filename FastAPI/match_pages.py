import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from string import punctuation
import re
import json

def process_text(text):
    stemmer = PorterStemmer()
    words = text.split()
    count_paragraph = [stemmer.stem(x.rstrip(punctuation).lower()) for x in words if not re.search(r'[./\[\]()|\'\;\!@#\$%\^&\*\-=]', x)]
    return ' '.join(count_paragraph)

def load_matrix():
    return np.genfromtxt('data/svd_matrix.csv', delimiter=',')

def load_transformer():
    with open('data/transformer.pkl', 'rb') as f:
        transformer = pickle.load(f)
    return transformer

def load_svd():
    with open('data/svd.pkl', 'rb') as f:
        svd = pickle.load(f)
    return svd


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def get_web_info(index):
    data = load_json_file(f'web_jsons/{index}.json')
    return data


def get_match_svd(query, k = 10):
    matrix = load_matrix()

    transformer = load_transformer()
    svd = load_svd()

    query = process_text(query)

    print

    query = transformer.transform([query])
    query = svd.transform(query)

    print(query)

    similarity_scores_new = cosine_similarity(query, matrix)
    top_k_documents_new = np.argsort(similarity_scores_new[0])[-k:][::-1]

    data = []
    for index in top_k_documents_new:
        page = get_web_info(index)
        page['match'] = similarity_scores_new[0][index]
        data.append(page)

    return data
