import Queue
import copy
from stanfordcorenlp import StanfordCoreNLP

from entity_linking import ner
from model import Node, Edge

# perform normally under Windows
# nlp = StanfordCoreNLP(r'../stanford-corenlp', memory='4g')
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
nlp = StanfordCoreNLP('http://localhost', port=9000)
wh_tags = ['WP', 'WRB', 'WDT']
nodes = []
question = ''
tokens = []
tree_node_dic = {}
dependency_tree = []
node_indexes = []
index_node_dic = {}


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.neighbours = []
        self.values = [value]

    def __str__(self):
        return str(self.value)


# delete punctuation
def pre_filter():
    # del_set = string.punctuation
    # replace = " " * len(del_set)
    # global question
    # tran_tab = maketrans(del_set, replace)
    # question = question.translate(tran_tab, del_set).lower().strip()
    # question = question.strip().lower()
    del_set = ["?", '"', ",", ".", "'", '/']
    global question
    for punc in del_set:
        if punc in question:
            question = question.replace(punc, ' ')
    question = question.strip().lower()


# extract entity, class, wh-words
def extract_nodes():
    # split words
    global tokens
    tokens = nlp.word_tokenize(question)
    nodes.extend(ner.match_entity(question))
    # use pos to filter wh-words
    pos = nlp.pos_tag(question)
    for i in range(len(pos)):
        p = pos[i]
        if p[1] in wh_tags:
            if not is_repeat(p[0]):
                nodes.append(Node(p[0], 'wh', []))


def is_repeat(word):
    for temp_node in nodes:
        if word in temp_node.word:
            return True
    return False


# merge entity tokens
def merge_tokens():
    token_dic = {}
    update_token_dic(token_dic)
    global question
    for n in nodes:
        split_words = n.word.split(' ')
        if len(split_words) > 1:
            begin = token_dic[split_words[0]]
            end = token_dic[split_words[-1]]
            tokens[begin] = n.word.replace(' ', '')
            del tokens[begin + 1:end + 1]
            update_token_dic(token_dic)
    for n in nodes:
        word = n.word.replace(' ', '')
        if word in tokens:
            n.index = tokens.index(word) + 1
            index_node_dic[n.index] = n
    question = ' '.join(tokens)


def update_token_dic(token_dic):
    for i in range(len(tokens)):
        token_dic[tokens[i]] = i


# build Qu
def build_query_graph():
    global dependency_tree
    dependency_tree = nlp.dependency_parse(question)
    convert_tree()
    edges = []
    # 2-2 find path
    if len(nodes) == 1:
        n = nodes[0]
        pre_attribute = ' '.join(tokens[:n.index - 1])
        edges.append(Edge(pre_attribute, Node('', 'wh', []), n))
        return edges
    for n in nodes:
        node_indexes.append(n.index)
    for i in range(len(node_indexes) - 1):
        n1 = node_indexes[i]
        for j in range(i + 1, len(node_indexes)):
            n2 = node_indexes[j]
            path = find_path(tree_node_dic[n1], tree_node_dic[n2])
            if path:
                word = ""
                for k in range(1, len(path)):
                    for value in tree_node_dic[path[k]].values:
                        word = word + tokens[value - 1] + ' '
                edges.append(Edge(word.strip(), index_node_dic[n1], index_node_dic[n2]))
    return edges


# convert dependency_tree for easy to use
def convert_tree():
    for e in dependency_tree:
        if e[1] not in tree_node_dic.keys():
            current = TreeNode(e[1])
        else:
            current = tree_node_dic[e[1]]
        if e[0] == 'amod':
            # merge two nodes
            current.values.insert(0, e[2])
            tree_node_dic[e[1]] = current
            continue
        if e[2] not in tree_node_dic.keys():
            neighbour = TreeNode(e[2])
        else:
            neighbour = tree_node_dic[e[2]]
        neighbour.neighbours.append(current)
        current.neighbours.append(neighbour)
        tree_node_dic[e[1]] = current
        tree_node_dic[e[2]] = neighbour


# find path between two nodes, from bottom to up
def find_path(begin, end):
    queue = Queue.Queue()
    queue.put(begin)
    # begin node to each node's path
    path = {}
    visited = []
    while not queue.empty():
        tree_node = queue.get()
        if tree_node.value in visited:
            continue
        if tree_node.value in path:
            path[tree_node.value].append(tree_node.value)
        else:
            path[tree_node.value] = [tree_node.value]
        visited.append(tree_node.value)
        for n in tree_node.neighbours:
            path[n.value] = copy.deepcopy(path[tree_node.value])
            if n.value == end.value:
                result = path[n.value]
                # if the path has another entity node
                for i in range(1, len(result)):
                    if result[i] in node_indexes:
                        return False
                return result
            queue.put(n)
    return False


def get_query_graph(q):
    global question
    question = q
    pre_filter()
    extract_nodes()
    merge_tokens()
    result = build_query_graph()
    clear_global_variables()
    return result


def clear_global_variables():
    global nodes
    global question
    global tokens
    global tree_node_dic
    global dependency_tree
    global node_indexes
    global index_node_dic
    nodes = []
    question = ''
    tokens = []
    tree_node_dic = {}
    dependency_tree = []
    node_indexes = []
    index_node_dic = {}


if __name__ == '__main__':
    question = 'What is the naming conventions of Exception classes?'
    re = get_query_graph(question)
