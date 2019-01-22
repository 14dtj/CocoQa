from SPARQLWrapper import SPARQLWrapper, JSON
from model import ScoreResult

sparql = SPARQLWrapper("http://218.193.191.42:4506/newdata")
ft = SPARQLWrapper("http://218.193.191.42:4507/data")

special_dic = {'ProsExample': 'ProsCluster', 'ConsExample': 'ConsCluster',
               'ProsExplanation': 'ProsCluster', 'ConsExplanation': 'ConsCluster',
               'Pros': 'ProsCluster', 'Cons': 'ConsCluster'}

deserted_attributes = ['OntologyType', 'Source', 'SoftwareSpecificationType', 'ExcelId', 'Similar',
                       'RelatedSpecification', 'FatherName']
similar_attributes = ['Similar', 'RelatedSpecification']


def query_rule(name):
    query = """
    PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
    select distinct ?s where{
        {?s rdf:Name "%s"} UNION {?s rdf:FatherName "%s"}
    }
"""
    sparql.setQuery(query % (name, name))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    result_list = []
    for result in results["results"]["bindings"]:
        result_list.append(result['s']['value'])
    return result_list


def test(query, param_set, has_attribute):
    if len(param_set) == 0:
        sparql.setQuery(query)
    else:
        sparql.setQuery(query % tuple(param_set))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except Exception:
        return None
    result_dic = {}
    if has_attribute:
        for result in results["results"]["bindings"]:
            predicate = result['p']['value'].split("#")[1]
            value = result['o']['value']
            result_dic[predicate] = value
            result_dic['Id'] = result['s']['value']
        if len(result_dic) > 0:
            return result_dic
    else:
        for result in results["results"]["bindings"]:
            s_id = result['s']['value']
            predicate = result['p']['value'].split("#")[1]
            value = result['o']['value']
            if s_id not in result_dic:
                result_dic[s_id] = {"Id": s_id}
            if predicate in ('ProsCluster', 'ConsCluster'):
                result_dic[s_id].update(find_cluster('<' + value + '>'))
            if predicate in deserted_attributes:
                continue
            else:
                result_dic[s_id][predicate] = value
        return result_dic.values()
    return -1


def query_special(query, param_set, special_attribute):
    if len(param_set) == 0:
        sparql.setQuery(query)
    else:
        sparql.setQuery(query % tuple(param_set))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except Exception:
        return None
    subject = ""
    cluster = special_dic[special_attribute]
    for result in results["results"]["bindings"]:
        subject = result['s']['value']
        subject = '<' + subject + '>'
    query = """
    PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
    select ?p ?o where{
        BIND(rdf:""" + special_attribute + """ AS ?p) .
       """ + subject + """ rdf:""" + cluster + """ ?cluster .
       ?cluster rdf:""" + special_attribute + """ ?o
    }
"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except Exception:
        return None
    result_dic = {}
    for result in results["results"]["bindings"]:
        predicate = result['p']['value'].split("#")[1]
        value = result['o']['value']
        result_dic[predicate] = value
        result_dic['Id'] = subject
    if len(result_dic) > 0:
        return result_dic
    return -1


def full_text_search(keywords):
    query = ("""
        PREFIX text: <http://jena.apache.org/text#>
        PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
        SELECT  ?s  ?rule ?sc{
            (?s ?sc) text:query  (rdf:Rule '%s')  .
            ?s rdf:Rule ?rule
            }
    """)
    ft.setQuery(query % keywords)
    ft.setReturnFormat(JSON)
    result = []

    res = ft.query().convert()
    for r in res["results"]["bindings"]:
        if float(r["sc"]["value"]) > 4.31:
            result.append(r["rule"]["value"])
    return result


def full_text_pros(keywords):
    query = ("""
        PREFIX text: <http://jena.apache.org/text#>
        PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
        SELECT  ?s ?sc{
            ?s rdf:ProsCluster ?c .
            (?c ?sc) text:query  (rdf:Pros '%s')  .
            }
    """)
    ft.setQuery(query % keywords)
    ft.setReturnFormat(JSON)
    result = []

    res = ft.query().convert()
    for r in res["results"]["bindings"]:
        score = float(r["sc"]["value"])
        if score > 6:
            result.append((score, r["s"]["value"]))
    result.sort(key=lambda x: x[0], reverse=True)
    return [y[1] for y in result]


def advanced_search(name, rule, benefit, weakness, exception):
    param_set = []
    query = """
        PREFIX text: <http://jena.apache.org/text#>
        PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
        SELECT  ?s ?p ?o{
            ?s ?p ?o .
        """
    if is_not_empty(name):
        param_set.append(name)
        query = query + """
            ?s rdf:Name|rdf:FatherName ?n.
            FILTER regex(LCASE(?n),'%s') .
        """
    if is_not_empty(rule):
        param_set.append(rule)
        query = query + """
            (?s) text:query  (rdf:Rule '%s')  .
        """
    if is_not_empty(benefit):
        param_set.append(benefit)
        query = query + """
            ?s rdf:ProsCluster ?pc.
            ?pc text:query (rdf:Pros '%s') .
        """
    if is_not_empty(weakness):
        param_set.append(weakness)
        query = query + """
            ?s rdf:ConsCluster ?cc
            ?cc text:query  (rdf:Cons '%s')  .
        """
    if is_not_empty(exception):
        param_set.append(exception)
        query = query + """
            ?s text:query  (rdf:Exception '%s')  .
        """
    query = query + "}"
    if not param_set:
        return -1
    ft.setQuery(query % tuple(param_set))
    ft.setReturnFormat(JSON)
    result_dic = {}
    res = ft.query().convert()
    for result in res["results"]["bindings"]:
        predicate = result['p']['value'].split("#")[1]
        value = result['o']['value']
        entity = result['s']['value']
        if entity not in result_dic:
            result_dic[entity] = {"Id": entity}
        if predicate in ('ProsCluster', 'ConsCluster'):
            if not value.startswith('<'):
                value = '<' + value + '>'
            result_dic[entity].update(find_cluster(value))
        if predicate in deserted_attributes:
            continue
        else:
            result_dic[entity][predicate] = value
    return result_dic.values()


def search_similar(uri):
    if not is_not_empty(uri):
        return -1
    if not uri.startswith('<'):
        uri = "<" + uri + ">"
    query = """
        PREFIX text: <http://jena.apache.org/text#>
        PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
        SELECT  ?p ?o{
            %s ?p ?o 
        }
        """
    sparql.setQuery(query % uri)
    sparql.setReturnFormat(JSON)
    result_set = []
    res = sparql.query().convert()
    for result in res["results"]["bindings"]:
        predicate = result['p']['value'].split("#")[1]
        value = result['o']['value']
        if predicate == 'Rule':
            result_set.append({'name': value, 'type': '1', 'relation': None})
        elif predicate in similar_attributes:
            if not value.startswith('<'):
                value = '<' + value + '>'
            temp = find_cluster(value)
            if 'Rule' in temp:
                result_set.append({'name': temp['Rule'], 'type': '2', 'relation': 'relatedEntity', 'Id': value})
        elif predicate in ('ProsCluster', 'ConsCluster'):
            if not value.startswith('<'):
                value = '<' + value + '>'
            temp_dict = find_cluster(value)
            for key in temp_dict:
                result_set.append({'name': temp_dict[key], 'type': '3', 'relation': key})
        elif predicate in deserted_attributes:
            continue
        else:
            result_set.append({'name': value, 'type': '3', 'relation': predicate})
    return result_set


def is_not_empty(my_str):
    return my_str is not None and my_str and my_str.strip()


def search_by_url(url):
    query = """
        PREFIX text: <http://jena.apache.org/text#>
        PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
        SELECT  ?p ?o{
            %s ?p ?o 
        }
        """
    sparql.setQuery(query % url)
    sparql.setReturnFormat(JSON)
    res = sparql.query().convert()
    result_dic = {}
    for result in res["results"]["bindings"]:
        value = result['o']['value']
        predicate = result['p']['value'].split("#")[1]
        if predicate in ('ProsCluster', 'ConsCluster'):
            result_dic.update(find_cluster('<' + value + '>'))
        if predicate in deserted_attributes:
            continue
        else:
            result_dic[predicate] = value
    result_dic['Id'] = url
    return result_dic


def find_cluster(cluster_id):
    query = """
        PREFIX text: <http://jena.apache.org/text#>
        PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
        SELECT  ?s ?p ?o{
            %s ?p ?o 
        }
        """
    sparql.setQuery(query % cluster_id)
    sparql.setReturnFormat(JSON)
    res = sparql.query().convert()
    cluster_dic = {}
    for result in res["results"]["bindings"]:
        value = result['o']['value']
        predicate = result['p']['value'].split("#")[1]
        cluster_dic[predicate] = value
    return cluster_dic
