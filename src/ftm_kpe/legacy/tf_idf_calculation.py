import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import operator

def run_tf_idf():
    path_in = "datas\\phishing\\legit\\"
    path_out = "datas\\phishing\\legit_out_tf-idf\\"
    documents = []
    doc_names = []

    dir_in = os.listdir(path_in)
    for file in dir_in:
        text = open(path_in + file, 'r', errors='backslashreplace').read()
        documents.append(text)
        doc_names.append(file)

    documents = [preprocess(document) for document in documents]
    vectorizer = TfidfVectorizer()
    tfidf_model = vectorizer.fit_transform(documents)
    attributes = list(vectorizer.vocabulary_.keys())
    matrix = tfidf_model.toarray()

    for i in range(0, len(matrix)):
        dic = {}
        for j in range(0, len(matrix[i])):
            value = matrix[i][j]
            if value != 0.0:
                key = attributes[j]
                dic.update({key: value})
        sorted_dic = dict(sorted(dic.items(), key=operator.itemgetter(1), reverse=True))
        top = 5
        key_phrases = []
        for key in sorted_dic:
            key_phrases.append(key)
            top -= 1
            if top == 0:
                break
        file_out = open(path_out + doc_names[i], 'w')
        file_out.write(",".join(key_phrases))
        file_out.close()

    print("DONE")


def preprocess(document):
    'changes document to lower case and removes stopwords'
    # change sentence to lower case
    document = document.lower()
    # tokenize into words
    words = word_tokenize(document)
    # remove stop words
    words = [word for word in words if word not in stopwords.words("english")]

    # join words to make sentence
    document = " ".join(words)
    print("Another document with length "+str(len(document))+" processed!")

    return document
