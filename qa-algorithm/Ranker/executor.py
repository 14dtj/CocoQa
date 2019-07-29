import sys

sys.path.append("/mnt/sdb/cjm/Match-LSTM")
import requests
import json
import pickle
import matching

from nltk.corpus import wordnet as wn
from utils.mrc_input import mrc
from stanfordcorenlp import StanfordCoreNLP

pre_url = "http://localhost:8983/solr/coco/select?q=context:"
punctuation = """!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""
translator = str.maketrans('', '', punctuation)
se_keywords = pickle.load(open('data/se_keywords.pkl', "rb"))
m = mrc()
useful_pos = ['NN', 'NNS', 'JJ', 'JJS']
nlp = StanfordCoreNLP('http://localhost', port=9000)


def execute(question):
    paragraphs = find_related_context(question)
    if paragraphs is not None:
        
        answer_array = m.mrcqa_batch(paragraphs, question)
        # make response
        data = []
        if answer_array:
            answers = answer_array[0]
            for i in range(len(answers)):
                answer = answers[i]
                context = paragraphs[i]
                start_index = get_start(context, answer)
                entity = matching.match(answer)
                json_object = {
                    'context': context,
                    'answer_start': start_index[0],
                    'answer_end': start_index[0] + start_index[1],
                    'entity': [entity]
                }
                data.append(json_object)
        print(data)
        return data


def find_related_context(question):
    question = question.translate(translator)
    keywords = None
    keyword_arr = []
    pos = nlp.pos_tag(question)
    for p in pos:
        if p[1] in useful_pos:
            keyword_arr.append(p[0])
            keywords = p[0] if keywords is None else keywords + '+' + p[0]
    if keywords is None:
        return
    url = pre_url + keywords + '~%20OR%20title:' + keywords + '~&fl=context'
    r = json.loads(requests.get(url).content)
    if r['responseHeader']['status'] == 0:
        paragraphs = r['response']['docs']
        re_paragraphs = []
        for p in paragraphs:
            is_valid = True
            p_1 = p['context'][0].lower()
            for key in keyword_arr:
                key = key.lower()
                if key not in p_1:
                    is_valid = False
            if is_valid:
                re_paragraphs.append(p['context'][0])
        return re_paragraphs


def get_start(context, answer):
    context = context.lower()
    question = answer.lower()
    matrix = [[0 for i in range(len(question) + 1)] for j in range(len(context) + 1)]
    max_len = 0
    p = 0
    for i in range(len(context)):
        for j in range(len(answer)):
            if context[i] == answer[j]:
                matrix[i + 1][j + 1] = matrix[i][j] + 1
                if matrix[i + 1][j + 1] > max_len:
                    max_len = matrix[i + 1][j + 1]
                    p = i + 1

    return [p - max_len - 1, max_len]


def is_similar(str1, str2):
    if str1.lower() == str2.lower():
        return True
    arr_1 = wn.synsets(str1)
    arr_2 = wn.synsets(str2)
    if arr_1 and len(arr_1) > 0 and arr_2 and len(arr_2) > 0:
        word_1 = arr_1[0]
        word_2 = arr_2[0]
        sim = word_1.wup_similarity(word_2)
        if sim and sim > 0.9:
            return True
    return False


if __name__ == '__main__':
    execute('how should do type conversions?')

