#!/bin/bash    
echo "Script counts fields occurrence in ZBL files."
cat $1 | cut -d' ' -f1 | sort | uniq -c

