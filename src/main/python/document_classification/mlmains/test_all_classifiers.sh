#Script testing KNN classifiers 
#$1 - input file
#$2 - distance type
#$3 - id for all pckl

#Generate test and train sets:
echo '----------splitting data----------'
python split_train_test_highest.py $1 5 5 save_train$3.pckl save_test$3.pckl save_labels$3.pckl save_elemcnt$3.pckl mc ut ti ab

#Train classifiers:
echo '----------training random classifier----------'
python main_train_random.py save_train$3.pckl save_labels$3.pckl save_elemcnt$3.pckl save_randclassif$3.pckl
echo '----------training random weighted classifier----------'
python main_train_weighted_random.py save_train$3.pckl save_labels$3.pckl save_elemcnt$3.pckl save_weighted_randclassif$3.pckl
echo '----------training mlknn classifier----------'
python main_train_mlknn.py save_train$3.pckl save_labels$3.pckl save_elemcnt$3.pckl save_mlknn$3.pckl 5 5 5 $2
echo '----------training mlknn fractional classifier----------'
python main_train_mlknn_fractional.py save_train$3.pckl save_labels$3.pckl save_elemcnt$3.pckl save_mlknn_fractional$3.pckl 5 5 $2
echo '----------training mlknn ensembled fractional classifier----------'
python main_train_mlknn_ensembled_fractional.py save_train$3.pckl save_labels$3.pckl save_elemcnt$3.pckl save_mlknn_ensembled_fractional$3.pckl 5 $2 3 5 7 9 15 21

#Test classifiers:
echo '----------random classifier----------'
python main_test_ml.py save_randclassif$3.pckl  save_test$3.pckl save_labels$3.pckl classify
echo '----------random weighted classifier----------'
python main_test_ml.py save_weighted_randclassif$3.pckl  save_test$3.pckl save_labels$3.pckl classify
echo '----------mlknn classifier----------'
python main_test_ml.py save_mlknn$3.pckl  save_test$3.pckl save_labels$3.pckl classify
echo '----------mlknn stupid classifier----------'
python main_test_ml.py save_mlknn$3.pckl  save_test$3.pckl save_labels$3.pckl classify_stupid
echo '----------mlknn fractional classifier----------'
python main_test_ml.py save_mlknn_fractional$3.pckl  save_test$3.pckl save_labels$3.pckl classify
echo '----------mlknn ensembled fractional classifier----------'
python main_test_ml.py save_mlknn_ensembled_fractional$3.pckl  save_test$3.pckl save_labels$3.pckl classify

echo '----------training hierarchical mlknn classifier----------'
python main_train_hiermlknn.py save_train$3.pckl save_labels$3.pckl save_elemcnt$3.pckl save_hiermlknn$3.pckl 5 5 5 save_test$3.pckl $2

echo '----------training hierarchical fractional mlknn classifier----------'
python main_train_hiermlknn_fractional.py save_train$3.pckl save_labels$3.pckl save_elemcnt$3.pckl save_hiermlknn_fractional$3.pckl 5 5 save_test$3.pckl $2
