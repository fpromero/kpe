# Original research-prototype batch runner.

from . import kpe_control
from . import summarization_control as sm_ctrl
from . import cosine_similarity as cos_sim
import operator
import os
from transformers import BertModel
import docx2txt

def perform_kpe(texts, kpes, top):

    bert_model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True, )
    #bert_model = ""
    path_in = texts#"datas\\500-KP\\documents\\"
    path_out = kpes#"datas\\500-KP\\\processed_noowa\\embedding(300)\\"
    files = os.listdir(path_in)
    files_out = os.listdir(path_out)
    if len(files_out) > 0:
        temp = []
        for f in files:
            if f.split(".")[0]+".txt" not in files_out:
                temp.append(f)
        files = temp
    silhouette_score = 0
    for file in files:
        print(file)
        #text = open(path_in + file, 'r', encoding="utf-8").read()
        text = docx2txt.process(path_in + file)#open(path_in + file, 'r', errors='backslashreplace').read()
        #langs = detect_langs(text)
        #text = re.sub(r'\W+', ' ', text)
        sentences, best_topics, key_phrases, kp_relevance = kpe_control.key_phrases_extraction(text, language="es",
                                                clustering_option="fcm", top_topic=0.75, top_kp=top, quantifier="pasi",
                                                select_option="2", bert_model=bert_model)
        #print(",".join(key_phrases))
        file = file.replace("docx","txt")
        file_out = open(path_out + file, 'w', errors='backslashreplace')
        for tps in best_topics:
            file_out.write(",".join(tps) + "\n")
        file_out.write("--------------------\n")
        file_out.write(",".join(key_phrases))
        file_out.close()

    print("DONE")


def summarization():
    path_in = "datas\\summarization\\multiling2015(sp)\\test1\\"
    #path_out = "datas\\summarization\\multiling2015(sp)\\output\\fcm\\pasi\\"
    path_out = "datas\\"
    files = os.listdir(path_in)
    files_out = os.listdir(path_out)
    if len(files_out) > 0:
        temp = []
        for f in files:
            if f not in files_out:
                temp.append(f)
        files = temp

    for file in files:

        #text = open(path_in + file, 'r', encoding='latin1').read()
        text = open(path_in + file, 'r', errors='backslashreplace').read()
        sm = sm_ctrl.topics_extraction(text, language="es", clustering_option="fcm", top_topic=0.75, quantifier="pasi")
        sentences = sm[0]
        topics = []
        for tp in sm[1]:
            for phr in tp:
                topics.append(phr)
        sen_val = {}

        for sen in sentences:
            goal_sim = 0
            for tp in topics:
                goal_sim += cos_sim.get_cosine(sen, tp)

            value = goal_sim / len(topics)
            sen_val.update({sen: value})

        sents_sorted = dict(sorted(sen_val.items(), key=operator.itemgetter(1), reverse=True))
        top_sent = 15
        summary = []
        for key in sents_sorted:
            summary.append(key.replace("\n",""))
            top_sent -= 1
            if top_sent == 0:
                break

        files_out = open(path_out + file, 'w')
        #files_out.write(str('\n'.join(map(str, summary)).encode("latin1")))
        files_out.write('\n'.join(map(str, summary)))
        files_out.close()


    print("DONE")


if __name__ == '__main__':

    perform_kpe('datas\\documents \\', 'datas\\output\\', 15)

    #summarization()
