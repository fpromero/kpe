import os,spacy


def creat_correlation_data():
    path_root = "datas\\inspec\\"
    path_data = path_root + "processed\\fcm\\pasi\\2\\"
    path_sources = path_root + "docsutf8\\"
    path_out = "datas\\Correlation-Datas\\inspec\\"
    file_ref = open(path_root + "ref.txt", 'r').readlines()
    nlp = spacy.load('es_core_news_sm')

    print("Loading references...")
    ref_dict = {}
    for line in file_ref:
        ln = line.split("||")
        key = ln[0]
        value = ln[1].split("; ")
        ref_dict.update({key: value})

    dir_data = os.listdir(path_data)
    for file in dir_data:
        if file in ref_dict:
            ref = ref_dict[file]
            kps = open(path_data + file, 'r').read().split(",")
            extracted = len(kps)
            cant = len(ref)
            kps.remove(kps[0])
            kps_temp = kps.copy()
            correct_kp = 0
            unmatcher = []

            print("Computing metrics...")
            for kp in kps_temp:
                ref_temp = ref.copy()
                correct = False
                for rf in ref_temp:
                    if kp in rf or rf in kp:
                        ref_temp.remove(rf)
                        correct_kp += 1
                        correct = True
                if correct:
                    kps_temp.remove(kp)
                else:
                    unmatcher.append(kp)

            if correct_kp > 0:
                p = correct_kp / (correct_kp + ((extracted - len(unmatcher)) - (correct_kp * 0.70))) * 100
                # p = correct_kp / (correct_kp + (extracted - correct_kp)) * 100
                r = correct_kp / (correct_kp + (cant - correct_kp)) * 100
                f1 = (2 * p * r) / (p + r)

                # count tokens
                print("Computing text length...")
                source_file = open(path_sources + file, 'r', errors='backslashreplace').read()
                doc = nlp(source_file)
                cant_tokens = len(doc)
                # vector to print [precision, recall, f-score, tokens len]
                vector = [str(round(p, 2)), str(round(r, 2)), str(round(f1, 2)), str(cant_tokens)]
                out_file = open(path_out + file, 'w')
                out_file.write(','.join(vector))
                out_file.close()

    print("DONE")
