from model import Entity
import csv
import cPickle
import ahocorasick

# build inverted index list for entity names/classes/relations
entity_path = 'data/dictionary/name.tsv'
class_path = 'data/dictionary/de.tsv'
relation_path = 'data/dictionary/dr.tsv'
rule_path = 'data/dictionary/rule.tsv'

entity_dic_path = 'data/object/entity_dic.pkl'
invert_entity_path = 'data/object/invert_entity.pkl'

class_dic_path = 'data/object/class_dic.pkl'
invert_class_path = 'data/object/invert_class.pkl'

relation_dic_path = 'data/object/relation_dic.pkl'
invert_relation_path = 'data/object/invert_relation.pkl'

rule_list_path = 'data/object/rule_list.pkl'
rule_dic_path = 'data/object/rule_dic.pkl'
# result
invert_index = {}
# pre process
entity_dic = ahocorasick.Automaton()


def pre_process(path, dict_path):
    with open(path) as f:
        reader = csv.reader(f, delimiter='	')
        line_count = 0
        for row in reader:
            if line_count > 0:
                synonyms = row[2].split("$")
                for word in synonyms:
                    if word in entity_dic:
                        e = entity_dic.get(word)
                        e.entity.append(row[1])
                    else:
                        e = Entity(word, [row[1]])
                        entity_dic.add_word(word, e)
            line_count += 1
    entity_dic.make_automaton()
    cPickle.dump(entity_dic, open(dict_path, "wb"))


def build_inverted_list(path):
    pre_process(path)
    add_invert_index()


def add_invert_index():
    for item in entity_dic:
        e = entity_dic[item]
        for i in range(len(e.word) - 1):
            token = e.word[i] + e.word[i + 1]
            if token in invert_index:
                invert_index[token].append(e.id)
            else:
                invert_index[token] = [e.id]
    cPickle.dump(invert_index, open(invert_relation_path, "wb"))


def read_rule(path):
    with open(path) as f:
        reader = csv.reader(f, delimiter='	')
        rules = []
        for row in reader:
            rules.append(row[0])
    cPickle.dump(rules, open(rule_list_path, "wb"))


if __name__ == '__main__':
    # build_inverted_list(relation_path)
    # invert_relations = cPickle.load(open(invert_relation_path, "rb"))
    # for ir in invert_relations:
    #     print invert_relations[ir]
    # pre_process(entity_path,entity_dic_path)
    pre_process(entity_path, entity_dic_path)
