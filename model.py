# entity and class
class Entity:
    def __init__(self, word, entity):
        self.word = word
        self.entity = entity

    def __str__(self):
        return self.entity + "," + self.word


# Node in sub-graph
class Node:
    def __init__(self, word, w_type, candidates):
        self.word = word
        # entity or wh-words
        self.type = w_type
        # class or entity candidates
        self.candidates = candidates
        self.index = 0
        self.edges = []

    def __str__(self):
        return 'word: %s, candidates: %s, type: %s' % (self.word, str(self.candidates), self.type)


class Edge:
    def __init__(self, word, start, end):
        self.word = word
        self.start = start
        self.end = end
        self.candidates = []

    def __str__(self):
        return 'word: %s, start: %s, end: %s' % (self.word, self.start.word, self.end.word)


class ScoreResult:
    def __init__(self, result, score):
        self.result = result
        self.score = score

    def __str__(self):
        return 'result: %s, score: %f' % (self.result, self.score)
