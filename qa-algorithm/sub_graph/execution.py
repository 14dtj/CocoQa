from sub_graph import construction
from entity_linking import ner
import sparql

special_attributes = ['ProsExample', 'ConsExample', 'ProsExplanation', 'ConsExplanation', 'Pros', 'Cons']
attribute_dict = {'why': 'Pros', 'when': 'Exception'}


def execute(question):
    # find candidates for edges
    node_set = set()
    edges = construction.get_query_graph(question)
    sql = """PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
    select distinct"""
    has_attribute = False
    special_attribute = False
    for e in edges:
        if e.word != '':
            node_set.add(e.start)
            node_set.add(e.end)
            e.candidates.extend(ner.match_relation(e.word))
        else:
            if e.start.word in attribute_dict and e.start.type == 'wh':
                node_set.add(e.end)
                e.candidates.extend([attribute_dict[e.start.word]])
            elif e.end.word in attribute_dict and e.end.type == 'wh':
                node_set.add(e.start)
                e.candidates.extend([attribute_dict[e.end.word]])
            else:
                node_set.add(e.start)
                node_set.add(e.end)
        if e.candidates:
            has_attribute = True
            if e.candidates[0] in special_attributes:
                special_attribute = e.candidates[0]
                sql = sql + """?s where {
                """
            else:
                sql = sql + """?s ?p ?o where{
                    BIND(rdf:""" + e.candidates[0] + """ AS ?p).
                    ?s ?p ?o ."""
    query_nodes = []
    for n in node_set:
        # find all attributes
        if n.type != 'wh':
            query_nodes.append(n)
        else:
            if not has_attribute:
                sql = sql + """
                    ?s ?p ?o where{
                    ?s ?p ?o . """

    for n1 in node_set:
        if n1.type != 'wh' and 'where' in sql:
            sql = sql + """
                    ?s rdf:""" + n1.type + """ "%s" ."""
        elif n1.type != 'wh' and 'where' not in sql:
            sql = sql + """
                    ?s ?p ?o where{
                    ?s ?p ?o .
                    ?s rdf:""" + n1.type + """ "%s" ."""

    sql = sql + """}"""
    result_set = []
    if len(query_nodes) == 1:
        for c in query_nodes[0].candidates:
            param_set = [c]
            if special_attribute:
                temp_result = sparql.query_special(sql, param_set, special_attribute)
            else:
                temp_result = sparql.test(sql, param_set, has_attribute)
            if temp_result != -1 and temp_result is not None:
                if isinstance(temp_result, list):
                    result_set.extend(temp_result)
                else:
                    result_set.append(temp_result)
    if len(query_nodes) == 2:
        for c1 in query_nodes[0].candidates:
            for c2 in query_nodes[1].candidates:
                param_set = [c1, c2]
                if special_attribute:
                    temp_result = sparql.query_special(sql, param_set, special_attribute)
                else:
                    temp_result = sparql.test(sql, param_set, has_attribute)
                if temp_result != -1 and temp_result is not None:
                    if isinstance(temp_result, list):
                        result_set.extend(temp_result)
                    else:
                        result_set.append(temp_result)
    return result_set


def query_name(question):
    name = ner.match_name(question)
    return sparql.query_rule(name)


if __name__ == '__main__':
    print('when could I use break and continue in loops?')
