#!/bin/bash -l 

export GRB_LICENSE_FILE=/s/chopin/l/grad/aebrahim/gurobi.lic
export LD_LIBRARY_PATH=/s/damavand/f/homes/aebrahim/gted/modified/third-party/gurobi652/linux64/lib/:$LD_LIBRARY_PATH

echo "LD_LIBRARY_PATH:" $LD_LIBRARY_PATH
echo "GRB_LICENSE_FILE:" $GRB_LICENSE_FILE

/s/damavand/f/homes/aebrahim/gted/modified/optimizer_orig_simplex $*
