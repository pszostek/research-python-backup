#Script testing classifiers based on precomputed distance matrix
#$1 - input file
#$2 - distance matrix

#Perform 10 fold:
echo '----------mlknn-basic----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 5 5 $2 5 mc ut ti ab
#echo '----------mlknn-threshold----------'
#python main_K_fold_distmat.py $1 5 5 mlknn_threshold 5 5 $2 5 mc ut ti ab
#echo '----------mlknn-tensembled----------'
#python main_K_fold_distmat.py $1 5 5 mlknn_tensembled 3,5,8 5 $2 5 mc ut ti ab

#Train hierarchical classifiers:
#echo '----------mlknn-basic-tree----------'
#python main_K_fold_distmat.py $1 5 5 mlknn-basic-tree 5 5 $2 5 mc ut ti ab
#echo '----------mlknn-threshold-tree----------'
#python main_K_fold_distmat.py $1 5 5 mlknn-threshold-tree 5 5 $2 5 mc ut ti ab
#echo '----------mlknn-tensembled-tree----------'
#python main_K_fold_distmat.py $1 5 5 mlknn-tensembled-tree 3,5,8 5 $2 5 mc ut ti ab
