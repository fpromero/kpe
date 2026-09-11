import csv
import os
from nltk.corpus import wordnet
import extract_msg


def clean_keyphrases():

   path_in = "datas\\phishing\\phish_out\\"
   path_out = "datas\\phishing\\phish_out.1\\"
   directory = os.listdir(path_in)

   for file in directory:
      if file.endswith(".txt"):
         text = open(path_in + file, 'r').read().split(",")
         keyphrases = []

         for ph in text:
            synsets1 = wordnet.synsets(ph.split(" ")[0])
            if len(synsets1) > 0:
               keyphrases.append(ph)

         file_out = open(path_out + file, 'w')
         kps = ",".join(keyphrases)
         file_out.write(kps)
         file_out.close()

   return


def create_ref_file():
   path_in = "datas\\Nus\\keys\\"
   dir_in = os.listdir(path_in)
   file_out = open("datas\\Nus\\ref.1.txt", 'w')

   for fl in dir_in:
      file = open(path_in + fl, 'r', encoding="utf-8").readlines()
      vector = []
      for line in file:
          vector.append(line.replace("\n", ""))
          ln = fl.replace("key", "txt") + "||" + "; ".join(vector)
      file_out.write(str(ln.encode('utf-8')).replace("b'","").replace("'\n", "\n") + "\n")
   return

def multi_doc_to_single():
   path_in = "datas\\summarization\\multiling2015(sp)\\test\\"
   dir_in = os.listdir(path_in)
   path_out = "datas\\summarization\\multiling2015(sp)\\test1\\"

   for fl in dir_in:
      file_out = open(path_out + fl + ".txt", 'w')
      file = os.listdir(path_in + fl)
      for txt in file:
         file1 = open(path_in + fl + "\\" + txt, 'r', encoding="utf-8")
         for line in file1:
            print(txt + "--" + line)
            if line != "\n":
               file_out.write(str(line.encode('utf-8')).replace("b'", "").replace("\n'", "") + "\n")
   file_out.close()

def preproces_phishing_CSV():
   f = open("datas\\phishing\\dataset_listo_v2.csv", errors='backslashreplace')
   reader = csv.reader(f)
   for row in reader:
      id = row[0]
      text = row[2] + "\n" + row[3]
      label = row[4]
      path = ""

      if label == 'legit':
         path = "datas\\phishing\\legit\\" + id + ".txt"
      else:
         path = "datas\\phishing\\phish\\" + id + ".txt"

      leg = open(path, 'w')
      leg.write(text)
      leg.close()

   print("DONE")

def process_phishing_out():
   #legit_dir = "datas\\phishing\\legit_out_kpe\\"
   phish_dir = "datas\\phishing\\final_eng\\emails_kps\\"

   all_attributes = []
   dic_leg = {}
   dic_psh = {}
   # dir = os.listdir(legit_dir)
   # for fl in dir:
   #    file = open(legit_dir + fl, 'r')
   #    for ln in file:
   #        vec = ln.split(",")
   #        if "" in vec:
   #           vec.remove("")
   #        vec.pop(0)
   #        dic_leg.update({fl: vec})
   #        all_attributes = all_attributes+vec

   dir = os.listdir(phish_dir)
   for fl in dir:
      file = open(phish_dir + fl, 'r')
      for ln in file:
         vec = ln.split(",")
         if "" in vec:
            vec.remove("")
         vec.pop(0)
         dic_psh.update({fl: vec})
         all_attributes = all_attributes + vec

   all_attributes = list(set(all_attributes))
   temp_att = []
   for att in all_attributes:
      if "0x" not in att:
         if len(att) < 15:
            temp_att.append(att)
   all_attributes = temp_att

   out = open("datas\\phishing\\final_eng\\all_attributes_kpe.txt", 'w')
   out.write(",".join(all_attributes))
   out.close()
   out = open("datas\\phishing\\final_eng\\datas_features_kpe.csv", 'w')
   heading = ["id"] + all_attributes + ["class"]
   out.write(",".join(heading) + "\n")
   #out.close()
   vector_len = len(all_attributes) + 2
   #out = open("datas\\phishing\\dataset.txt", 'w')

   for fl in dic_leg:
      vector = ["0"] * vector_len
      vector [0] = fl.replace(".txt", "")
      vector[vector_len-1] = "0"
      values = dic_leg[fl]
      for v in values:
         if v in all_attributes:
            index = all_attributes.index(v) + 1
            vector[index] = "1"
      out.write(",".join(vector) + "\n")

   for fl in dic_psh:
      vector = ["0"] * vector_len
      vector[0] = fl.replace(".txt", "")
      vector[vector_len - 1] = "1"
      values = dic_psh[fl]
      for v in values:
         if v in all_attributes:
            index = all_attributes.index(v) + 1
            vector[index] = "1"
      out.write(",".join(vector) + "\n")

   out.close()

   print("DONE")

def clean_papers():

   path_in = "datas\\Nus\\docsutf8\\"
   dir_in = os.listdir(path_in)
   path_out = "datas\\Nus\\docsutf8_clean\\"

   for file in dir_in:
      print(file)
      file_in = open(path_in + file, 'r', errors='backslashreplace').readlines()
      file_out = open(path_out + file, 'w')
      write = False
      text = ""
      for line in file_in:
         lower_ln = line.lower().replace("\n", "")
         if lower_ln == "abstract":
            write = True
         #elif len(lower_ln.split(" ")) > 1 and lower_ln.split(" ")[1] == "introduction":
         elif lower_ln == "introduction":
            write = True
         elif "categories and subject descriptors" in lower_ln:
            text += "\n"
            write = False
         #elif len(lower_ln.split(" ")) > 1 and lower_ln.split(" ")[0] == "2.":
         elif len(line) > 4 and line.isupper():
            break
         if write == True:
            text += lower_ln + " "

      file_out.write(text.replace("abstract ", "").replace("introduction ", ""))
      file_out.close()

   print("DONE")


def load_emails_files():

   dir = os.listdir("datas\\phishing\\emails\\")
   for file in dir:
      f = r"datas\\phishing\\emails\\" + file
      file_out = open("datas\\phishing\\emails\\" +file+".txt", 'w')
      msg = extract_msg.Message(f)
      # print('Sender: {}'.format(msg.sender))
      # print date
      # print('Sent On: {}'.format(msg.date))
      # print subject
      print('Subject: {}'.format(msg.subject))
      file_out.write(msg.subject + '\n')
      # print body
      print('Body: {}'.format(msg.body))
      file_out.write(msg.body + '\n')
      file_out.close()

   print("DONE")
