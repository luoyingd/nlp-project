from pycorenlp import StanfordCoreNLP
import json
import random
from tqdm import tqdm

stanford = StanfordCoreNLP('http://localhost:9000')


def get_emotion(sentence):
    res = stanford.annotate(sentence,
                            properties={
                                'annotators': 'sentiment',
                                'outputFormat': 'json',
                                'timeout': '50000'
                            })
    emotion = 'None'
    for s in res["sentences"]:
        emotion = s["sentiment"]
    return emotion


with open("/Users/dongluoying/downloads/rumour.json", 'r') as load_f:
    rumour_dic = json.load(load_f)

with open("/Users/dongluoying/downloads/non_rumour.json", 'r') as load_f:
    non_rumour_dic = json.load(load_f)


rumour_records = random.sample(list(rumour_dic.values()), 100)
non_rumour_records = random.sample(list(non_rumour_dic.values()), 100)

rumour_emotions = []
non_rumour_emotions = []
for text in tqdm(rumour_records):
    tmp = []
    for sen in text:
        tmp.append(get_emotion(sen))
    rumour_emotions.append(tmp)
for text in tqdm(non_rumour_records):
    tmp = []
    for sen in text:
        tmp.append(get_emotion(sen))
    non_rumour_emotions.append(tmp)


rumour_neg = []
rumour_pos = []
non_rumour_neg = []
non_rumour_pos = []
for item in rumour_emotions:
    if item[0] == "Negative":
        rumour_neg.append(item)
    elif item[0] == "Positive":
        rumour_pos.append(item)

print(len(rumour_neg) / len(rumour_records))
print(len(rumour_pos) / len(rumour_records))

for item in non_rumour_emotions:
    if item[0] == "Negative":
        non_rumour_neg.append(item)
    elif item[0] == "Positive":
        non_rumour_pos.append(item)

print(len(non_rumour_pos) / len(non_rumour_records))
print(len(non_rumour_neg) / len(non_rumour_records))



def check_ratio(list):
    pos_count = 0
    neg_count = 0
    sum = 0
    for item in list:
        sum += len(item)
        for reply in item[1:]:
            if reply == "Positive":
                pos_count += 1
            elif reply == "Negative":
                neg_count += 1
    return pos_count / sum, neg_count / sum


print(check_ratio(rumour_neg))
print(check_ratio(rumour_pos))
print(check_ratio(non_rumour_neg))
print(check_ratio(non_rumour_pos))
