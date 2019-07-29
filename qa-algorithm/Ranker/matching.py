from SPARQLWrapper import SPARQLWrapper, JSON
import executor

special_dic = {'ProsExample': 'ProsCluster', 'ConsExample': 'ConsCluster',
               'ProsExplanation': 'ProsCluster', 'ConsExplanation': 'ConsCluster',
               'Pros': 'ProsCluster', 'Cons': 'ConsCluster'}

deserted_attributes = ['OntologyType', 'Source', 'SoftwareSpecificationType', 'ExcelId', 'Similar',
                       'RelatedSpecification', 'FatherName']
sparql = SPARQLWrapper("http://202.120.40.28:4460/data")


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


def match(answer):
    answer = answer.translate(executor.translator)
    ft = SPARQLWrapper("http://218.193.191.42:4507/data")
    query = """
        PREFIX text: <http://jena.apache.org/text#>
        PREFIX j.0: <http://www.w3.org/2018/mycard-rdf/1.0#>
        PREFIX rdf: <http://www.w3.org/2018/mycard-rdf/1.0#>
        SELECT ?s ?p  ?o{
              ?s  text:query '%s' .
              ?s ?p ?o
            }
    """
    ft.setQuery(query % answer)
    ft.setReturnFormat(JSON)
    res = ft.query().convert()
    result_dic = {}
    entity_id = None
    for result in res["results"]["bindings"]:
        value = result['o']['value']
        predicate = result['p']['value'].split("#")[1]
        if entity_id is None:
            entity_id = result['s']['value']
        elif result['s']['value'] != entity_id:
            continue

        if predicate in special_dic.values():
            result_dic.update(find_cluster('<' + value + '>'))
        elif predicate in deserted_attributes:
            continue
        else:
            result_dic[predicate] = value
        result_dic['Id'] = entity_id
    return result_dic

