import sparql
from model import Node
from pre_process import *

# pre process result
invert_entity = cPickle.load(open(invert_entity_path, "rb"))
entity_dic = cPickle.load(open(entity_dic_path, "rb"))

invert_class = cPickle.load(open(invert_class_path, "rb"))
class_dic = cPickle.load(open(class_dic_path, "rb"))

invert_relation = cPickle.load(open(invert_relation_path, "rb"))
relation_dic = cPickle.load(open(relation_dic_path, "rb"))

rules = cPickle.load(open(rule_list_path, "rb"))
rule_dic = cPickle.load(open(rule_dic_path, "rb"))

se_keywords = cPickle.load(open('data/object/se_keywords.pkl', "rb"))

wh_phrases = ['is there any', 'tell me something about', 'give me some examples about', 'are there any examples about',
              'when']
# for edit distance
beta = 2
# q-gram
q = 2
# for Jaccard similarity
jac = 0.6


def get_ids(sub_str, invert):
    ids = []
    for i in range(len(sub_str) - 1):
        token = sub_str[i] + sub_str[i + 1]
        if token in invert:
            # TODO
            ids.extend(invert[token])
    return ids


def is_similar(e, sub_str, count):
    threshold_ed = max(len(e.word), len(sub_str)) - beta * q
    threshold_jc = (len(e.word) + len(sub_str)) * jac / (1 + jac)
    return round(count - threshold_ed + count - threshold_jc, 4)


# find candidates
def match(sub_str, dic, invert):
    sub_str = sub_str.lower()
    ids = sorted(get_ids(sub_str, invert))
    result_set = {}
    if len(ids):
        last_element = ids[0]
        count = 0
        for i in range(0, len(ids)):
            if ids[i] == last_element:
                count += 1
                if i == len(ids) - 1:
                    e = dic[last_element]
                    score = is_similar(e, sub_str, count)
                    if score > -2:
                        result_set[e.entity] = score
            else:
                e = dic[last_element]
                score = is_similar(e, sub_str, count)
                if score > -2:
                    result_set[e.entity] = score
                count = 0
                last_element = ids[i]
    return result_set


def match_relation(sub_str):
    return match(sub_str, relation_dic, invert_relation)


# find all classes and entities
def match_entity(sentence):
    result = []
    for wh_phrase in wh_phrases:
        if sentence.startswith(wh_phrase):
            result.append(Node(wh_phrase, 'wh', []))
            sentence = sentence[len(wh_phrase) + 1:]
    keywords = ''
    is_start = False
    start_index = -1
    for end_index, w in se_keywords.iter(sentence):
        keywords = keywords + ' ' + w
        if not is_start:
            start_index = end_index - len(w) + 1
            is_start = True
    if start_index != -1:
        word = sentence[start_index:len(sentence)]
        rule_candidates = sparql.full_text_search(word)
        if rule_candidates:
            result.append(Node(word, 'Rule', rule_candidates))
    for i, w in entity_dic.iter(sentence):
        if not is_repeat(result, w.word):
            result.append(Node(w.word, 'Name', w.entity))
    for i, w in class_dic.iter(sentence):
        if not is_repeat(result, w.word):
            result.append(Node(w.word, 'OntologyType', [w.entity]))
    return result


# find all subject entities
def match_subject_entity(sentence):
    result = []
    for i, w in entity_dic.iter(sentence):
        if not is_repeat(result, w.word):
            result.append(Node(w.word, 'Name', w.entity))
    return result


def is_repeat(result, word):
    word = word.lower()
    for temp_node in result:
        if word in temp_node.word.lower() or temp_node.word.lower() in word:
            return True
    return False


def match_name(sentence):
    sentence = sentence.lower()
    for wh_phrase in wh_phrases:
        if sentence.startswith(wh_phrase):
            sentence = sentence[len(wh_phrase) + 1:]
    for i, w in entity_dic.iter(sentence):
        return w.entity


if __name__ == '__main__':
    print entity_dic
    # match_entity('Is there any benefits to declare variables in the smallest scope possible')
# nodes = match_entity('What is the rule of layout?')
# for n in nodes:
#     print n.candidates
# match_rule('Is there any benefits to declare variables in the smallest scope possible')
