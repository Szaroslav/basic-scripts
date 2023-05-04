#!/bin/bash

OUTPUT_FN=output.md
title=""
EX_PATTERN="[Ee]xercise ?[0-9]+\.[0-9]+"
EX_README_PATTERN="$EX_PATTERN/README.md$"

printf "" > $OUTPUT_FN

find test/autogen_docs/chapter01 -print0 | sort -z | while IFS= read -r -d '' file
do
    echo "$file"
    if [ ! -d $file ]; then
        if [[ $file =~ $EX_README_PATTERN ]] && [[ $title != $(sed '1q;d' $file) ]]; then
            title=$(sed '1q;d' $file)
            echo -e "$title\n" >> $OUTPUT_FN
        fi
        
        if [[ $file =~ README.md$ ]]; then
            write=false
            while IFS= read -r line
            do
                if [[ $line =~ $EX_PATTERN ]]; then
                    write=true
                fi
                if $write; then
                    # echo $line
                    echo $line >> $OUTPUT_FN
                fi
            done < $file
        fi
    fi
done
