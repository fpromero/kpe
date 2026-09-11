from . import pre_processing
from . import clustering
import operator
from . import topic_rank


def key_phrases_extraction(text, language, clustering_option, top_topic, top_kp, quantifier, select_option, bert_model):
    sentences, text_vector, candidate_kp = perform_prepro(text, language)
    topics = topic_identification(False, clustering_option, text_vector, text, candidate_kp,
                                       quantifier, None, None, None, language, sentences, bert_model, top_kp)
    # for tp in topics: print(",".join(tp))
    # print("--------------")
    if len(topics) > 15:
        best_topics = topic_rank.get_best_topics(top_topic, candidate_kp, topics)
    else:
        best_topics = topics
    #for tp in best_topics: print(",".join(tp))
    kp_extraction = select_keyphrases(top_kp, text_vector, best_topics, select_option, candidate_kp, None)
    key_phrases = kp_extraction[0]
    kp_relevance = kp_extraction[1]

    return sentences, best_topics, key_phrases, kp_relevance

def absolute_key_phrases_extraction(text, text_vector, candidate_kp, clustering_option, top_topic, top_kp, quantifier, select_option,
                                distance_matrix, threshold, n_clusters):

    topics = topic_identification(True, clustering_option, text_vector, text, candidate_kp, quantifier,
                                distance_matrix, threshold, n_clusters, None, None, None, top_kp)
    if len(topics) > 10:
        best_topics = topic_rank.get_best_topics(top_topic, candidate_kp, topics)
    else:
        best_topics = topics
    key_phrases = select_keyphrases(top_kp, text_vector, best_topics, select_option, candidate_kp, distance_matrix)

    return key_phrases[0]


def perform_prepro(text, language):
    sentences, kp = pre_processing.pre_proces(text, language)
    text_vector = []
    candidate_key_phrase = []
    for p in kp:
        if len(p) == 1:
            text_vector.append(p[0])
            if p[0] not in candidate_key_phrase:
                candidate_key_phrase.append(p[0])
        else:
            ph = ""
            for i in range(0, len(p)):
                if i == (len(p) - 1):
                    ph += p[i]
                else:
                    ph += p[i] + " "
            text_vector.append(ph)
            if ph not in candidate_key_phrase:
                candidate_key_phrase.append(ph)

    return sentences, text_vector, candidate_key_phrase


def topic_identification(absolute, clustering_option, text_vector, text, phrases, quantifier, distance_matrix,
                         threshold, n_clusters, language, sentences, bert_model, top_kp):

    topics = []
    if absolute:
        perform_clust = clustering.perform_absolute_clustering(clustering_option, phrases, distance_matrix, threshold,
                                                               n_clusters)
    else:
        perform_clust = clustering.perform_clustering(clustering_option, text_vector, text, phrases, quantifier
                                                      , language, sentences, bert_model, top_kp)

    clusters = perform_clust[0]
    silhouette_score = perform_clust[1]
    dict = {}
    alone = 1
    for i in range(0, len(clusters)):
        if clusters[i] is None:
            key = "alone" + str(alone)
            dict.update({key: [phrases[i]]})
            alone += 1
        else:
            key = clusters[i]
            if key in dict:
                value = dict[key]
                value.append(phrases[i])
                dict.update({key: value})
            else:
                value = [phrases[i]]
                dict.update({key: value})

    for cluster in dict.values():
        topics.append(cluster)
    return topics


def perform_topicrank(top):
    return


def select_keyphrases(top, text_vector, topics, select_option, candidate_kp, distance_matrix):
    key_phrases = []
    keyp_relvance = {}

    for topic in topics:
        relev_tem = 0
        index = 0
        if len(topic) > 1:
            if select_option == "1":
                keyp_relvance.update({topic[0]: 1})
            elif select_option == "2":
                freq_kp = frequent_kp(topic, text_vector)
                keyp_relvance.update({freq_kp[0]: freq_kp[1]})
            elif select_option == "3":
                cent_kp = centroid_kp(topic, candidate_kp, distance_matrix)
                keyp_relvance.update({cent_kp[0]: cent_kp[1]})
            else:
                keyp_relvance.update({topic[0]: 1})
                freq_kp = frequent_kp(topic, text_vector)
                keyp_relvance.update({freq_kp[0]: freq_kp[1]})
                cent_kp = centroid_kp(topic, candidate_kp, distance_matrix)
                keyp_relvance.update({cent_kp[0]: freq_kp[1]+cent_kp[1]})
        else:
            keyp_relvance.update({topic[0]: 1})

    keyps_sorted = dict(sorted(keyp_relvance.items(), key=operator.itemgetter(1), reverse=True))
    for key in keyps_sorted:
        key_phrases.append(key)
        top -= 1
        if top == 0:
            return key_phrases, keyp_relvance

    return set(key_phrases), keyp_relvance


def frequent_kp(topic, text_vector):
    frequents = []
    for phrase in topic:
        words = phrase.split(" ")
        freq = 0
        for wd in words:
            freq += text_vector.count(wd)
        frequents.append(freq)

    best = max(frequents)
    return topic[frequents.index(best)], best


def centroid_kp(topic, candidate_kp, distance_matrix):

    centroids = []
    for ph1 in topic:
        sim = 0
        for ph2 in topic:
            if ph1 != ph2:
                ind1 = candidate_kp.index(ph1)
                ind2 = candidate_kp.index(ph2)
                if ind1 < ind2:
                    sim += distance_matrix[ind1][ind2]
                else:
                    sim += distance_matrix[ind2][ind1]
        centroids.append(sim/(len(topic)-1))

    best = max(centroids)
    #print("best score: " + str(best))
    return topic[centroids.index(best)], best
