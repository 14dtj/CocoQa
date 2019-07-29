from nltk.corpus import wordnet as wn

arr_1 = wn.synset('global.s.01')
arr_2 = wn.synset('iodine.n.01')

print(arr_1.wup_similarity(arr_2))

