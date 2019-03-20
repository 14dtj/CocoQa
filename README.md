# code-convention-robot
An auto QA system about code convention and styles based on knowledge base
## Ontology & RDF
We construct a knowledge base called CCBase in the field of coding convention. Ontology folder contains the ontology of CCBase, including subject types, relations and so on, which is in the form of owl. RDF folder contains some entities of our CCBase.
## plugin

## algorithm：CCQA
### introduction
In the algorithm folder is the CCQA system. CCQA can assist programmers to retrieval information about coding conventions in a more natural manner.  
The main algorithm of CCQA is subgraph matching. Inspired by [Hu et al.’s work](https://ieeexplore.ieee.org/abstract/document/8085196), we propose the LE (long entity) Node-First framework to answer coding convention questions by subgraph matching.We first extract semantic relations based on the dependency tree of question sentences to build a semantic query graph *Qu*. A semantic relation is a triple *<rel; arg1; arg2>*, where *rel* is a relation phrase, and *arg1* and *arg2* are its associated node phrases. After that, a SPARQL query statement is generated from *Qu* and then executed to get final answers.
### usage
