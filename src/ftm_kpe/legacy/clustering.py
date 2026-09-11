import numpy
from nltk.corpus import wordnet
from . import dbscan as dbs
from . import owa
import math
from fcmeans import FCM
from sklearn.cluster import AgglomerativeClustering, DBSCAN, MeanShift, estimate_bandwidth
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cosine
from sklearn.preprocessing import MinMaxScaler
import math
from . import bert_embedding
from kneed import KneeLocator
import numpy as np


def perform_clustering(clustering_option, text_vector, text, phrases, quantifier, language, sentences, bert_model, top_kp):
    print("Filling distance matrix...")
    clusters = []
    for i in range(0, len(phrases)):
        clusters.append(i)
    silhouette_avg = 1
    n_clusters = top_kp
    if len(phrases) > n_clusters:
        distance_matrix, threshold = fill_distance_matrix(phrases, text_vector, text, quantifier, language, sentences, bert_model)
        #distance_matrix, threshold = fill_distance_matrix_light(phrases, text_vector, text, 2, language, sentences, bert_model)

        if clustering_option == "hac":
            print("HAC working...")
            clusters = perform_hac(distance_matrix, threshold)
        elif clustering_option == "dbs":
            print("DBScan working...")
            clusters = perform_dbs(distance_matrix, threshold, min_samples=2)
        elif clustering_option == "fcm":
            print("FCMeans working...")
            clusters = perform_fcmeans(distance_matrix, n_clusters)
        elif clustering_option == "ms":
            print("Mean Shift working...")
            clusters = perform_ms(distance_matrix)

        # unique_labels = set(clusters)
        #
        # if len(unique_labels) > 1:
        #     silhouette_avg = silhouette_score(distance_matrix, clusters, metric="precomputed")

    return clusters, silhouette_avg


def perform_absolute_clustering(clustering_option, phrases, distance_matrix, threshold, n_clusters):
    clusters = []

    if clustering_option == "hac":
        print("HAC working...")
        clusters = perform_hac(distance_matrix, threshold)
    elif clustering_option == "dbs":
        print("DBScan working...")
        clusters = perform_dbs(distance_matrix, threshold, min_samples=2)
    elif clustering_option == "fcm":
        if len(phrases) > n_clusters:
            print("FCMeans working...")
            clusters = perform_fcmeans(distance_matrix, n_clusters)
        else:
            for i in range(0, len(phrases)):
                clusters.append(i)

    unique_labels = set(clusters)
    silhouette_avg = 1
    # if len(unique_labels) > 1 and len(phrases) > n_clusters:
    #     silhouette_avg = silhouette_score(distance_matrix, clusters, metric="precomputed")

    return clusters, silhouette_avg

def fill_distance_matrix_light(phrases, text_vector, text, similarity_option, language, sentences, bert_model):
    matrix = numpy.zeros(shape=(len(phrases), len(phrases)))
    total_dist = 0.0
    pairs = 0
    if similarity_option == 6:
        words_embeddings = bert_embedding.get_embedding(bert_model, sentences)

    for i in range(0, len(phrases) - 1):
        phrase1 = phrases[i]
        row = []
        for j in range(i + 1, len(phrases)):
            phrase2 = phrases[j]
            similarity = 0
            if similarity_option == 1:
                similarity = word_dist(phrase1, phrase2, text_vector)
            elif similarity_option == 2:
                similarity = syntactic_sim(phrase1, phrase2)
            elif similarity_option == 3:
                similarity = pmi_coocurrence(phrase1, phrase2, text_vector, text)
            elif similarity_option == 4:
                sem = semantic(phrase1, phrase2, language)
                similarity = round(sem[0], 2)
            elif similarity_option == 5:
                sem = semantic(phrase1, phrase2)
                similarity = round(sem[1], 2)
            elif similarity_option == 6:
                similarity = cosine_embedding_sim(words_embeddings, phrase1, phrase2)

            total_dist += similarity
            pairs += 1
            matrix[i][j] = round(similarity, 2)
            #print(str(i) + "--" + str(j))

    threshold = round((total_dist / pairs), 2)
    return matrix, threshold


def fill_distance_matrix(phrases, text_vector, text, quantifier, language, sentences, bert_model):
    words_embeddings = bert_embedding.get_embedding(bert_model, sentences)
    matrix = numpy.zeros(shape=(len(phrases), len(phrases)))
    total_dist = 0.0
    pairs = 0
    for i in range(0, len(phrases) - 1):
        phrase1 = phrases[i]
        row = []
        for j in range(i + 1, len(phrases)):
            phrase2 = phrases[j]
            syntactic = syntactic_sim(phrase1, phrase2)
            dist = word_dist(phrase1, phrase2, text_vector)
            #semantic_sim, relatedness_sem = semantic(phrase1, phrase2, language)
            pmi = pmi_coocurrence(phrase1, phrase2, text_vector, text)
            cosine_embedding = cosine_embedding_sim(words_embeddings, phrase1, phrase2)
            vector = [syntactic, dist, pmi, cosine_embedding]
            owa_agg = owa_aggregation(vector, quantifier)[0]
            total_dist += 1 - owa_agg
            pairs += 1
            matrix[i][j] = round(1-owa_agg, 2)
            #print(str(i) + "--" + str(j))

    threshold = round((total_dist / pairs), 2)
    return matrix, threshold


def owa_aggregation(vector, quantifier):

    return owa.owa_aggregation(vector, quantifier=quantifier, axis=0, keepdims=True)


def cosine_embedding_sim(words_embeddings, phrase1, phrase2):
    cos_dist = 0
    pairs = 0

    for word1 in phrase1.split(" "):
        if word1 in words_embeddings:
            embed1 = words_embeddings[word1]
            if len(embed1) > 0:
                for word2 in phrase2.split(" "):
                    if word2 in words_embeddings:
                        embed2 = words_embeddings[word2]
                        if len(embed2) > 0:
                            cos_dist = 1 - cosine(embed1, embed2)
                            pairs += 1
    return cos_dist


def word_dist(phrase1, phrase2, text_vector):
    dist = 0.0
    ph1_ind = text_vector.index(phrase1)
    ph2_ind = text_vector.index(phrase2)
    if ph1_ind < ph2_ind:
        dist = ph2_ind - ph1_ind
    elif ph1_ind > ph2_ind:
        dist = ph1_ind - ph2_ind

    return 1-dist / len(text_vector)


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = numpy.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )

    return matrix[size_x - 1, size_y - 1]


def syntactic_sim(phrase1, phrase2):
    return round((levenshtein(phrase1, phrase2)/ max(len(phrase1), len(phrase2))),2)


def semantic(phrase1, phrase2, language):
    #return 1, 1
    sem = []
    total_sem = 0
    total_relat = 0
    cant = 0.0
    phr1 = phrase1.split(" ")
    phr2 = phrase2.split(" ")

    for word1 in phr1:
        if language == "es":
            synsets1 = wordnet.synsets(word1, lang="spa")
        else:
            synsets1 = wordnet.synsets(word1)
        if len(synsets1) > 0:
            syn1 = synsets1[0]
            for word2 in phr2:
                if language == "es":
                    synsets2 = wordnet.synsets(word2, lang="spa")
                else:
                    synsets2 = wordnet.synsets(word2)
                if len(synsets2) > 0:
                    syn2 = synsets2[0]
                    sim_sem = []
                    rel_sem = []
                    if syn1.name().split(".")[1] == syn2.name().split(".")[1]:
                        total_sem += syn1.wup_similarity(syn2)
                        #total_relat += syn1.lch_similarity(syn2) / 3.6375861597263857
                        cant += 1
                    '''for syn1 in synsets1:
                        for syn2 in synsets2:
                            if syn1.name().split(".")[1] == syn2.name().split(".")[1]:
                                sim_sem.append(syn1.wup_similarity(syn2))
                                rel_sem.append(syn1.lch_similarity(syn2))

                    if len(sim_sem) > 0 and len(rel_sem) > 0:
                        sort_sim = sorted(sim_sem, reverse=True)[0]
                        sort_rel = sorted(rel_sem, reverse=True)[0]
                        total_sem += sort_sim
                        total_relat += sort_rel / 3.6375861597263857
                        cant += 1'''

    if cant == 0.0:
        sem.append(1)
        sem.append(1)
        return sem

    sem.append(total_sem / cant)
    sem.append(total_relat / cant)

    return sem


def pmi_coocurrence(phrase1, phrase2, text_vector, text):

    coocurrence = 0.0
    sentences = text.split(". ")
    for sent in sentences:
        if phrase1 in sent:
            if phrase2 in sent:
                coocurrence += 1

    if coocurrence == 0.0:
        return 0.0

    return coocurrence / (text_vector.count(phrase1) * text_vector.count(phrase2))


def perform_dbs(matrix, threshold, min_samples):

    return dbs.dbscan(matrix, eps=threshold, min_points=min_samples)


def perform_hac(matrix, threshold):
    clusters = AgglomerativeClustering(metric='precomputed', distance_threshold=threshold,
                                       n_clusters=None, linkage="average")
    clusters.fit_predict(matrix)
    return clusters.labels_


def perform_ms(matrix):
    bandwidth = estimate_bandwidth(matrix, quantile=0.2)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(matrix)
    return ms.labels_


def optimal_epsilon(matrix):
    distances = []
    for vector in matrix:
        for value in vector:
            if value > 0: distances.append(value)
    distances.sort()
    i = np.arange(len(distances))
    knee = KneeLocator(i, distances, S=1, curve='convex', direction='increasing', interp_method='polynomial')
    return distances[knee.knee]


def perform_fcmeans(matrix, n_clusters):

    fcm = FCM(n_clusters=n_clusters)
    fcm.fit(matrix)
    fcm.centers
    clusters = fcm.predict(matrix)

    return clusters
