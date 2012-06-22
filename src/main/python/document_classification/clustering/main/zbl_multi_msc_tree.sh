echo "Program that for every configuration from list-of-arguments-per-iteration file executes building of a tree..."
echo "Four arguments expected: source-zbl-file list-of-arguments-per-iteration output-file errors-output-file"
echo " source-zbl-file = $1" 
echo " list-of-arguments-per-iteration = $2" 
echo " output-file = $3"
echo " errors-output-file = $4"

echo "Processing..."
while read cfg
do
   echo " configuration = $cfg"
   python zbl_build_msc_tree.py $1 $cfg >> $3 2>> $4   
done < $2
