# code-convention-robot
An auto QA system about code convention and styles based on knowledge base

## Our QA system：CCQA
CCQA can assist programmers to retrieval information about coding conventions in a more natural manner.  
The main algorithm of CCQA is subgraph matching. Inspired by [Hu et al.’s work](https://ieeexplore.ieee.org/abstract/document/8085196), we propose the LE (long entity) Node-First framework to answer coding convention questions by subgraph matching.We first extract semantic relations based on the dependency tree of question sentences to build a semantic query graph *Qu*. A semantic relation is a triple *<rel; arg1; arg2>*, where *rel* is a relation phrase, and *arg1* and *arg2* are its associated node phrases. After that, a SPARQL query statement is generated from *Qu* and then executed to get final answers.
