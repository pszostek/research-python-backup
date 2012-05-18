#!/bin/bash
echo "The program executes several-times knn.py WITH DEFAULT CFG for enumerated dists-matrices and labels'-files"
echo "Four arguments expected: prefix-of-dists-files prefix-of-labels-files number-of-first-label number-of-last-label (=83)"
echo "----------------------------------------"
echo "prefix-of-dists-files:$1"
echo "prefix-of-labels-files:$2"
echo "labels: $3-$4"
echo "----------------------------------------"


for label_no in `seq $3 $4`; do
    date
    echo "Processing label no $label_no" 
    echo " dist file $1$label_no"
    echo " labels file $2$label_no"
    echo "----------------------" 
    python knn.py $1$label_no $2$label_no
    echo "----------------------" 
    cp final_labels.txt final_labels$label_no.txt
    echo "----------------------" 
    python merge_labels_files.py final_labels.txt merged_labels.txt merged_labels.txt
    echo "----------------------------------------"
done;


