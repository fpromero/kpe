from . import pre_processing
from . import clustering
import operator
from . import topic_rank


def topics_extraction(text, language, clustering_option, top_topic, quantifier):
    prepro = perform_prepro(text, language)
    text_vector = prepro[1]
    candidate_kp = prepro[2]
    topic_ident = topic_identification(clustering_option, text_vector, text, candidate_kp, quantifier, language)
    topics = topic_ident[0]
    if len(topics) > top_topic:
        best_topics = topic_rank.get_best_topics(top_topic, candidate_kp, topics)
    else:
        best_topics = topics

    return prepro[0], best_topics


def perform_prepro(text, language):
    pp = pre_processing.pre_proces(text, language)
    kp = pp[1]
    text_vector = []
    candidate_key_phrase = []
    for p in kp:
        if len(p) == 1:
            text_vector.append(p[0].text)
            if p[0].text not in candidate_key_phrase:
                candidate_key_phrase.append(p[0].text)
        else:
            ph = ""
            for i in range(0, len(p)):
                if i == (len(p) - 1):
                    ph += p[i].text
                else:
                    ph += p[i].text + " "
            text_vector.append(ph)
            if ph not in candidate_key_phrase:
                candidate_key_phrase.append(ph)

    return pp[0], text_vector, candidate_key_phrase


def topic_identification(clustering_option, text_vector, text, phrases, quantifier, language):

    topics = []
    perform_clust = clustering.perform_clustering(clustering_option, text_vector, text, phrases, quantifier, language)
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
    return topics,silhouette_score


def perform_topicrank(top):
    return


def select_keyphrases(top, text_vector, topics):
    key_phrases = []
    keyps = {}
    keyp_relvance = set_kps_relevances(text_vector, topics)
    for topic in topics:
        relev_tem = 0
        index = 0
        if len(topic) > 1:
            for i in range(0, len(topic)):
                r = keyp_relvance[topic[i]]
                if r > relev_tem:
                    relev_tem = r
                    index = i
            keyps.update({topic[index]: relev_tem})
        else:
            keyps.update({topic[0]: relev_tem})

    keyps_sorted = dict(sorted(keyps.items(), key=operator.itemgetter(1), reverse=True))
    for key in keyps_sorted:
        key_phrases.append(key)
        top -= 1
        if top == 0:
            return key_phrases


    return key_phrases

def set_kps_relevances(text_vector, topics):

    key_relevance = {}
    for topic in topics:
        for phrase in topic:
            key_relevance.update({phrase: kp_relevance(phrase, topic, text_vector)})

    return key_relevance

def kp_relevance(phrase, topic, text_vector):

    frequency = text_vector.count(phrase)
    avg_sim = avg_similarity(phrase, topic)
    first = 0
    if topic[0] == phrase:
        first = 1

    return frequency + avg_sim + first


def avg_similarity(phrase, cluster):
    avg = 0.0

    return avg
