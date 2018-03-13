## GTED as graph kernel

The files in this directory are for using GTED as graph kernel.

Some of the benchmark datasets used for evaluating graph kernels are available in `dataset` directory. Available datasets are: MUTAG, ENZYMES, NCI1.

It converts graph in `graphml` format to the format understood by LP writer.

#### Usage

To convert MUTAG dataset in `dataset/MUTAG/`, 

```{python}
python convert.py dataset/MUTAG/ converted/MUTAG/
```

It creates eularian graph files in `converted/MUTAG/` directory.

#### Dependencies
networkx==1.7
pygraphml==2.2

