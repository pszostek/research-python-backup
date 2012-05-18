#Generate test and train sets:
echo '----------splitting data----------'
python split_train_test_highest.py $1 5 5 save_train.pckl save_test.pckl save_labels.pckl save_elemcnt.pckl mc ut ti ab

#Train classifiers:
echo '----------training random classifier----------'
python main_train_random.py save_train.pckl save_labels.pckl save_elemcnt.pckl save_randclassif.pckl
echo '----------training random weighted classifier----------'
python main_train_weighted_random.py save_train.pckl save_labels.pckl save_elemcnt.pckl save_weighted_randclassif.pckl
echo '----------training mlknn classifier----------'
python main_train_mlknn.py save_train.pckl save_labels.pckl save_elemcnt.pckl save_mlknn.pckl 5 5 5
#echo '----------training hierarchical mlknn classifier----------'
#python main_train_hiermlknn.py save_train.pckl save_labels.pckl save_elemcnt.pckl save_hiermlknn.pckl 5 5 5

#Test classifiers:
echo '----------random classifier----------'
python main_test_ml.py save_randclassif.pckl  save_test.pckl save_labels.pckl classify
echo '----------random weighted classifier----------'
python main_test_ml.py save_weighted_randclassif.pckl  save_test.pckl save_labels.pckl classify
echo '----------mlknn classifier----------'
python main_test_ml.py save_mlknn.pckl  save_test.pckl save_labels.pckl classify
echo '----------mlknn stupid classifier----------'
python main_test_ml.py save_mlknn.pckl  save_test.pckl save_labels.pckl classify_stupid
#echo '----------mlknn hierarchical classifier----------'
#python main_test_ml.py save_hiermlknn.pckl  save_test.pckl save_labels.pckl classify
