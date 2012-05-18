#!/bin/bash

echo "The program calculates LSA for ZBL-file."
if [ $1 ] && [ $2 ]
then
  echo "IN: $1"
  echo "OUT: $2"
else  
  echo "Two args expected: input-zbl-file output-zbl-file"
  exit 1
fi
echo "----------------------------------------"
#preprocessing (filtering, stemming):
python zbl_process_file.py -copyfield ti TI < $1 | python zbl_process_file.py -copyfield ut UT | python zbl_process_file.py -copyfield ab AB | python zbl_process_file.py -filter ti,ut,ab | python zbl_process_file.py  -stemming porter ti,ut,ab > /tmp/zbl_filtered_stemmed.zbl.txt
echo "----------------------------------------"
#converting words into ids
python zbl_process_file.py -gensim_dict ti,ut,ab < /tmp/zbl_filtered_stemmed.zbl.txt
echo "----------------------------------------"
python zbl_process_file.py -gensim_map ti,ut,ab < /tmp/zbl_filtered_stemmed.zbl.txt > /tmp/zbl_filtered_stemmed_g0.zbl.txt
echo "----------------------------------------"
#calculating tfidf
python zbl_process_file.py -gensim_tfidf < /tmp/zbl_filtered_stemmed_g0.zbl.txt
echo "----------------------------------------"
python zbl_process_file.py -gensim_tfidfmap < /tmp/zbl_filtered_stemmed_g0.zbl.txt > /tmp/zbl_filtered_stemmed_g1.zbl.txt
echo "----------------------------------------"
#calculating lsa topics
python zbl_process_file.py -gensim_lsa 300 < /tmp/zbl_filtered_stemmed_g1.zbl.txt 
echo "----------------------------------------"
python zbl_process_file.py -gensim_lmap < /tmp/zbl_filtered_stemmed_g1.zbl.txt > $2
echo "----------------------------------------"

