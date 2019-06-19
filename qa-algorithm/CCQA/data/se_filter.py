from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import cPickle
import ahocorasick

db = SPARQLWrapper("http://202.120.40.28:4460/data")
rules = []
se_list = []
se_keys = ahocorasick.Automaton()


def query_rule():
    query = """
    PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
    select ?rule where{
        ?s rdf:Rule ?rule
    }
"""
    db.setQuery(query)
    db.setReturnFormat(JSON)
    results = db.query().convert()
    for result in results["results"]["bindings"]:
        rule = result['rule']['value']
        rule = rule.encode('utf-8')
        rules.append(rule)
    print 'initialize rules success'
    print 'rules size is ' + str(len(rules))


def read_file():
    path = 'raw.txt'
    with open(path) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for word in row:
                word = word.encode('utf-8')
                se_list.append(word)
    print 'initialize se list success'
    print 'se list size is ' + str(len(se_list))


def execute():
    with open("dictionary/se_keywords.tsv") as f:
        for line in f.readlines():
            print line.strip()
            # for rule in rules:
            #     for w in se_list:
            #         words = rule.split(' ')
            #         if w in words:
            #    writer.writerow([{w: rule}])
            se_keys.add_word(line.strip(), line.strip())
    se_keys.make_automaton()
    cPickle.dump(se_keys, open('object/se_keywords.pkl', "wb"))


if __name__ == '__main__':
    query_rule()
    read_file()
    execute()
