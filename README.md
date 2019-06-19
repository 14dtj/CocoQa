# CocoQa
An auto QA system about code convention and styles based on knowledge base
## Ontology & RDF
We construct a knowledge base called CCBase in the field of coding convention. Ontology folder contains the ontology of CCBase, including subject types, relations and so on, which is in the form of owl. RDF folder contains some entities of our CCBase.
## Plugin
We developed an Intellij Idea plugin. You can download [plugin.zip](https://github.com/14dtj/CocoQa/blob/master/plugin/plugin.jar) and install it by the [instructions of Idea](https://www.jetbrains.com/help/idea/managing-plugins.html). 

## Introduction

![Design of CCQA](https://github.com/14dtj/CocoQa/blob/master/arc.png)


In the algorithm folder is the CCQA system. CCQA can assist programmers to retrieval information about coding conventions in a more natural manner.  
One of the algorithm of CCQA is subgraph matching. Inspired by [Hu et al.’s work](https://ieeexplore.ieee.org/abstract/document/8085196), we propose the LE (long entity) Node-First framework to answer coding convention questions by subgraph matching.We first extract semantic relations based on the dependency tree of question sentences to build a semantic query graph *Qu*. A semantic relation is a triple *<rel; arg1; arg2>*, where *rel* is a relation phrase, and *arg1* and *arg2* are its associated node phrases. After that, a SPARQL query statement is generated from *Qu* and then executed to get final answers.

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