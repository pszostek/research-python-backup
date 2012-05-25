#!/bin/bash

echo "The program calculates LSA for ZBL-file."
if [ $1 ] && [ $2 ] && [ $3 ]
then
  echo "IN: $1"
  echo "OUT: $2"
  echo "NUM TOPICS: $3"
else  
  echo "Three args expected: input-zbl-file output-zbl-file num-topics"
  exit 1
fi

echo "----------------------------------------"
mkdir models_lsa$3
echo "----------------------------------------"
#converting words into ids
python zbl_process_file.py -gensim_dict ti,ut,ab < $1
echo "----------------------------------------"
python zbl_process_file.py -gensim_map ti,ut,ab < $1 > /tmp/zbl_filtered_stemmed_g0.zbl.txt
echo "----------------------------------------"
#calculating tfidf
python zbl_process_file.py -gensim_tfidf < /tmp/zbl_filtered_stemmed_g0.zbl.txt
echo "----------------------------------------"
python zbl_process_file.py -gensim_tfidfmap < /tmp/zbl_filtered_stemmed_g0.zbl.txt > /tmp/zbl_filtered_stemmed_g1.zbl.txt
echo "----------------------------------------"
#calculating lsa topics
python zbl_process_file.py -gensim_lsa $3 < /tmp/zbl_filtered_stemmed_g1.zbl.txt 
echo "----------------------------------------"
python zbl_process_file.py -gensim_lmap < /tmp/zbl_filtered_stemmed_g1.zbl.txt > $2
echo "----------------------------------------"
cp /tmp/*.pickle models_lsa$3
cp /tmp/gensim_semantic_model_topics.txt models_lsa$3
echo "----------------------------------------"

