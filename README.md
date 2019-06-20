# CocoQa
An auto QA system about code convention and styles based on knowledge base
## Ontology & RDF
We construct a knowledge base called CCBase in the field of coding convention. Ontology folder contains the ontology of CCBase, including subject types, relations and so on, which is in the form of owl. RDF folder contains some entities of our CCBase.
## Plugin
We developed an Intellij Idea plugin. You can download [plugin.zip](https://github.com/14dtj/CocoQa/blob/master/plugin/plugin.jar) and install it by the [instructions of Idea](https://www.jetbrains.com/help/idea/managing-plugins.html). 

## Introduction

![Design of CCQA](https://github.com/14dtj/CocoQa/blob/master/arc.png)


CocoQa is a QA system for coding conventions. CocoQa combines the advantages of the KB- and the corpus-based QA systems: it stores in a knowledge base coding conventions collected from online resources; it builds CCBase, a knowledge graph introduced in [3], for modeling coding conventions; and it answers questions about coding conventions by querying the graph.

As the above figure shows, the CocoQa tool consists of four components: (1) a coding convention knowledge graph constructed from online resources, (2) a subgraph matcher that understands natural language questions and performs SPARQL queries over the knowledge graph, (3) a machine comprehenser that employs a deep neural network model to answer questions. The comprehenser searches answers from all textual paragraphs attached to the knowledge graph, and (4) a ranker that ranks answers retrieved by the subgraph matcher and the machine comprehenser via a logistic regression classifier.
In the algorithm folder is the CCQA system. CCQA can assist programmers to retrieval information about coding conventions in a more natural manner.  

The subgraph matcher generates answers to a question by querying entities and their relations in CCBase. Given a question, it casts the question into a SPARQL query followed by querying CCBase. The procedure and a running example is available [here]().

We also integrate an end-to-end machine comprehension approach that applies a deep neural network to answer the query on textual paragraphs attached in CCBase. The introduction and procedure to run machine comprehension QA could be found [here](https://github.com/14dtj/CocoQa/blob/master/qa-algorithm/MRCQA/README.md) .
A logistic regression classifier is trained to merge and rank the answers, and retrieve the top ones.
## Install
It is a web application and we developed a graphical interface. After installing the following python packages, you can run FLASK server and experience CCQA.  
**Dependencies**  
First of all, you should download [Stanford CoreNLP toolkit](https://stanfordnlp.github.io/CoreNLP/) and run the server.
```
cd stanford-corenlp-full-${version}
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```
Then, Stanford CoreNLP server will listen on port 9000 for requests.  
After that, the following python packages have to be installed.
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
Now, you can visit ```localhost:5000/ordinary``` to experience our system!
