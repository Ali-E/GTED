# Prepare the colored assebmly graph:

We used Hybrid De Novo Assembler (HyDA) to generate the graph. You can download this software here:

[HyDA software](http://chitsazlab.org/software/hyda/)

After installing the software you can use the script.sh to generate colored assebmly graph from 2 fasta files:

```bash
sh script.sh inputFile1.fasta inputFile2.fasta k
```
(k is the k-mer sized to be used in making the assembly graph)

# Gnerating the LP using the assembly graph:

After generating the assembly graph it can be used as input to the src.py code to generate the constituent graphs:

```python
python src.py assembly_graph_file.gted 
```

After generating the constituent assembly graphs they can be used as input to readAssem.py to generate LP:

```python
readAssem.py graphFile1 graphFile2 match_score mismatch_score indel_score
```

The generated LP has the standard format to be directly used as input to Gurobi LP solver. This software can be downloaded here:

[Gurobi Optimizer](http://www.gurobi.com/)


