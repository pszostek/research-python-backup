#!/bin/bash    
echo "Script takes similarity matrix and reconstructs single level of data hierarchy."
echo "Higher level similarity matrix is also generated."
echo "Arguments: input-matrix-path lablels'-prefix-length output-matrix-path"      
echo "GENERATING CLUSTERS ======================================================"
octave genClusters.m $1 $2
echo "GENERATING DESCRIPTORS ==================================================="
python ../gen_clusters_descriptor.py $1 $2
echo "GENERATING STATISTICS ===================================================="
python ../gen_clusters_stats.py $1 $2
echo "GENERATING HIGHER-LEVEL MATRIX ==========================================="
python ../gen_clusters_sim_matrix.py $1 $2 $3
echo "=========================================================================="
