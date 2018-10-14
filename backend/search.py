import nltk
from nltk.corpus import stopwords
import re
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
from gensim.models import KeyedVectors
from gensim.test.utils import datapath


def setup():
    nltk.download('stopwords')
    nltk.download('punkt')

def tokenize_a_sentence(sentence):
    stop_words = set(stopwords.words('english'))
    
    sentence = sentence.strip()
    
    line_tokens = re.split(' |_|\n',sentence) 
    line_tokens = list(filter(lambda a: a != '', line_tokens))
    
    filtered= []
    for i in range(len(line_tokens)):
        token = line_tokens[i]
        
        if(token not in stop_words):
            
            for j in reversed(range(len(token))):
                if(token[j].isalpha() ):
                    token = token[:j+1]
                    break
            filtered.append(token)
    return filtered
    

def tokenize(docs):

    all_doc_tokens = []
    index = 0
    for doc in docs:
        tokens = []
        sentences = doc.lower().split(". |, |; |\n")
        tokens = []
        for i in range(len(sentences)):
            tokens += tokenize_a_sentence(sentences[i])
        
        all_doc_tokens.append([index,tokens])
        index+=1


    return all_doc_tokens

def prepare_search(query):
    token_list = tokenize_a_sentence(query)
    return token_list
    

def predict(piazza_data, ids, query, model):
    list_of_lines = tokenize(piazza_data)
    corpus = []
    for text in list_of_lines:
        corpus.append(' '.join([l.rstrip().lower().translate(str.maketrans('','',string.punctuation)) for l in text[1]]))
    
    tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english', min_df=1, max_df=0.8)
    tfs = tfidf.fit_transform(corpus)
        
    similarity = lambda u, v: 1-cosine(u, v)
        
    token_list = prepare_search(query)

    similar_keys = {}
    substring_keys = {}
    vocab = tfidf.vocabulary_

    for k in vocab.keys():
        for t in token_list:
            if(t in k):
                if(k not in substring_keys):
                    substring_keys[k] = 1
                    token_list.append(k)
            if(k in model and k not in model):
                if (t in model and similarity(model[k],model[t]) > 0.6 ):
                    similar_keys[k] = 1
            
    
    search = ' '.join(token_list+list(similar_keys.keys()))
    print(search)

    search_tf = tfidf.transform([search])

    cids = []
    sims = []

    for i, sim in enumerate(cosine_similarity(tfs, search_tf)):
        if(sim[0] > 0.1):
            cids.append(ids[i])
            sims.append(sim[0])
    cids = np.asarray(cids)
    sims = np.asarray(sims)
    print("before_return")
    return cids[np.argsort(sims)]