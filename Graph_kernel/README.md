## GTED as graph kernel

The files in this directory are for using GTED as graph kernel.

Some of the benchmark datasets used for evaluating graph kernels are available in `dataset` directory. Available datasets are: MUTAG, ENZYMES, NCI1.

convert.py can be used to make the input graphs Eulerian using chinese postman algorithm. The final graphs will be in sgf format. (details in the paper)

#### Usage

To convert MUTAG dataset in `dataset/MUTAG/`, 

```{python}
python convert.py dataset/MUTAG/ converted/MUTAG/ --graphml --log --summary
```

It creates eularian graph files in `converted/MUTAG/` directory. The option --graphml is used because the input graphs are in graphml format. If the input graphs are already in the sgf format --graphml options must be removed. The other two options are optional (details in the paper)

Once the input graphs are ready (in sgf format and Eulerian), graphKernel.py can be used to generate the matrix of pairwise distances of all the graphs in a directory. For this script to work, the gurobi lp solver has be set correctly, and the neccessary changes has to be made to the vars_then_optimizer.sh file to reflect the direction of the licence, library, and optimizer. Free academic license is provided in gurobi website:

https://www.gurobi.com/downloads/end-user-license-agreement-academic/


```{python}
python graphKernel.py converted/MUTAG/ mutag_kernel.csv --summary --log
```

The --log and --summary are optional.

#### Dependencies
The versions have to match:

networkx==1.7
pygraphml==2.2


### References:
If you use this tool or parts of that please cite the corresponding papers:

[1] Boroojeny, A. E., Shrestha, A., Sharifi-Zarchi, A., Gallagher, S. R., Sahinalp, S. C., & Chitsaz, H. (2018, April). GTED: Graph traversal edit distance. In International Conference on Research in Computational Molecular Biology (pp. 37-53). Springer, Cham. 

[2] Ebrahimpour Boroojeny, A. (2019). Theory of Graph Traversal Edit Distance, Extensions, and Applications (Doctoral dissertation, Colorado State University. Libraries).

[3] Ebrahimpour Boroojeny, A., Shrestha, A., Sharifi-Zarchi, A., Gallagher, S. R., Sahinalp, S. C., & Chitsaz, H. (2020). Graph traversal edit distance and extensions. Journal of Computational Biology, 27(3), 317-329.

[4] Ebrahimpour Boroojeny, A., Shrestha, A., Sharifi-zarchi, A., Gallagher, S. R., Sahinalp, S. C., & Chitsaz, H. (2020). PyGTED: Python application for computing graph traversal edit distance. Journal of Computational Biology, 27(3), 436-439.
