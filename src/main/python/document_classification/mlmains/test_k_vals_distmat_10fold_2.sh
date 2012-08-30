#Script testing classifiers based on precomputed distance matrix
#$1 - input file
#$2 - distance matrix

echo '----------mlknn-threshold k=5----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 5 5 $2 5 mc ut ti ab
echo '----------mlknn-threshold k=6----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 6 5 $2 5 mc ut ti ab
echo '----------mlknn-threshold k=7----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 7 5 $2 5 mc ut ti ab
echo '----------mlknn-threshold k=8----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 8 5 $2 5 mc ut ti ab
echo '----------mlknn-threshold k=9----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 9 5 $2 5 mc ut ti ab
echo '----------mlknn-threshold k=10----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 10 5 $2 5 mc ut ti ab
echo '----------mlknn-threshold k=11----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 11 5 $2 5 mc ut ti ab
echo '----------mlknn-threshold k=12----------'
python main_K_fold_distmat.py $1 5 5 mlknn_threshold 12 5 $2 5 mc ut ti ab
