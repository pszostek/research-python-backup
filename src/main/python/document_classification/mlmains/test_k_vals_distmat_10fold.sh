#Script testing classifiers based on precomputed distance matrix
#$1 - input file
#$2 - distance matrix

#Perform 10 fold:
echo '----------mlknn-basic k=5----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 5 5 $2 5 mc ut ti ab
echo '----------mlknn-basic k=6----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 6 5 $2 5 mc ut ti ab
echo '----------mlknn-basic k=7----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 7 5 $2 5 mc ut ti ab
echo '----------mlknn-basic k=8----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 8 5 $2 5 mc ut ti ab
echo '----------mlknn-basic k=9----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 9 5 $2 5 mc ut ti ab
echo '----------mlknn-basic k=10----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 10 5 $2 5 mc ut ti ab
echo '----------mlknn-basic k=11----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 11 5 $2 5 mc ut ti ab
echo '----------mlknn-basic k=12----------'
python main_K_fold_distmat.py $1 5 5 mlknn_basic 12 5 $2 5 mc ut ti ab
