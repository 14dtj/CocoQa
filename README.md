# code-convention-robot
An auto QA system about code convention and styles based on knowledge base
## Ontology & RDF
We construct a knowledge base called CCBase in the field of coding convention. Ontology folder contains the ontology of CCBase, including subject types, relations and so on, which is in the form of owl. RDF folder contains some entities of our CCBase.
## Plugin
We developed an Intellij Idea plugin. You can download [plugin.jar](https://github.com/14dtj/code-convention-robot/tree/master/plugin) and install it by the [instructions of Idea](https://www.jetbrains.com/help/idea/managing-plugins.html). 
## Algorithm：CCQA
### Introduction
In the algorithm folder is the CCQA system. CCQA can assist programmers to retrieval information about coding conventions in a more natural manner.  
The main algorithm of CCQA is subgraph matching. Inspired by [Hu et al.’s work](https://ieeexplore.ieee.org/abstract/document/8085196), we propose the LE (long entity) Node-First framework to answer coding convention questions by subgraph matching.We first extract semantic relations based on the dependency tree of question sentences to build a semantic query graph *Qu*. A semantic relation is a triple *<rel; arg1; arg2>*, where *rel* is a relation phrase, and *arg1* and *arg2* are its associated node phrases. After that, a SPARQL query statement is generated from *Qu* and then executed to get final answers.
### Install
It is a web application and we developed a graphical interface. After installing the following python packages, you can run FLASK server and experience CCQA.   
**Dependencies**
```
Python 2.7.0
FLASK 1.0.2
SPARQLWrapper 1.8.2
stanfordcorenlp 3.9.1.1
pyahocorasick latest
```
**Run**
```
cd code-convention-robot
FLASK_APP = server.py flask run --host=0.0.0.0 --port=5000
```
Now, you can visit ```localhost:5000/ordinary``` to experience our system!
