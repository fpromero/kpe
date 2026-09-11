import operator


def get_best_topics(top, phrases, topics):
    best_topics = []
    top = int(top * len(topics))
    ranked_topics = topic_rank(phrases, topics)
    in_sort = dict(sorted(ranked_topics.items(), key=operator.itemgetter(1), reverse=True))
    # for ind in in_sort:
    #     print(str(ind) + "---" + str(in_sort[ind]))
    for index in in_sort:
        best_topics.append(topics[int(index)])
        top -= 1
        if top == 0:
            return best_topics


def topic_rank(phrases, topics):
    edge_eval = edge_evaluation(phrases, topics)
    ranked_topics = {}
    for i in range(0, len(topics)):
        ranked_topics.update({i: 1.0})

    it = 0
    topic_len = len(topics)
    previous_iter = []
    this_iter = []
    mse = 100
    while mse > 0.5:
        previous_iter = this_iter
        this_iter = []

        for i in range(0, topic_len):
            temp = 0.0
            temp1 = 0.0
            for j in range(0, topic_len):
                if i != j:
                    for k in range(0, topic_len):
                        if j != k:
                            if j < k:
                                key = str(j) + "-" + str(k)
                            else:
                                key = str(k) + "-" + str(j)
                            temp1 += edge_eval[key]
                    if i < j:
                        key = str(i) + "-" + str(j)
                    else:
                        key = str(j) + "-" + str(i)
                    temp += edge_eval[key] * ranked_topics[j] / temp1
            w = round(1 - 0.85 + 0.85 * temp, 2)
            ranked_topics.update({i: w})
            this_iter.append(w)
        if it > 0:
            mse = medium_square_error(previous_iter, this_iter)
        it += 1

    return ranked_topics

def medium_square_error(previous_iter, this_iter):
    mse = 0.0
    length = len(previous_iter)

    for i in range(0, length):
        mse += previous_iter[i] - this_iter[i]

    return mse/length

def edge_evaluation(phrases, topics):

    edge_eval = {}
    for i in range(0, len(topics)-1):
        topic1 = topics[i]
        for j in range(i+1, len(topics)):
            topic2 = topics[j]
            key = str(i) + "-" + str(j)
            value = distance(topic1, topic2, phrases)
            edge_eval.update({key: value})
    return edge_eval

def distance(topic1, topic2, phrases):
    dist = 0.0
    for phrase1 in topic1:
        for phrase2 in topic2:
            dist += 1/abs(phrases.index(phrase1) - phrases.index(phrase2))
    return dist
