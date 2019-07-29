# Subgraph Matcher
## Introduction
The subgraph matcher generates answers to a question by querying entities and their relations in CCBase. Given a question, it casts the question into a SPARQL query3 followed by querying CCBase. Figure below illustrates how a question “Q1. what are the effects of using goto?” is transformed into a query.

![Illustration of Subgraph Matcher](https://github.com/14dtj/CocoQa/blob/master/kbqa_example.png)

Given a question, the subgraph matcher takes a subgraph matching algorithm [5] to extract entities and relations inside and mapping the question into a SPARQL query: (1) the matcher extracts nodes (including entities and wh-words) from the question. For example, in Figure above, “what” (a wh-word) and “using goto” are identified as two nodes for Q1. Here Jena Full Text Search4 is employed to identify entities in a question; (2) the matcher generates a dependency tree for Q1; (3) the matcher builds a graph Qu: for each pair of nodes (vi , vj ), if there is a path between them in the dependency tree, an edge is introduced in Qu; the label is set as the concatenation of words along the path between vi and vj in the dependency tree. Qu can be mapped to a subgraph of CCBase, containing only the nodes and edges w.r.t. the question; and (4) the matcher generates SPARQL queries from Qu and finds candidate relations in CCBase for the edges in Qu.
## Install

**Dependencies**  
- MRCQA
- Ranker

The following python packages have to be installed.
```
Python 2.7.0
Flask==1.0.2
Flask-Cors==3.0.7
gunicorn==19.9.0
pyahocorasick==lattest
SPARQLWrapper==1.8.2
stanfordcorenlp==3.9.1.1
```
**Run**
```
cd code-convention-robot
gunicorn -b 0.0.0.0:${port} server:app
```
Now, you can visit ```localhost:${port}/ordinary``` to experience our system!
