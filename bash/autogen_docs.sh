#!/bin/bash

OUTPUT_FN=output.md
found_title=false

echo "" > $OUTPUT_FN

find test/autogen_docs/chapter01 -print0 | while IFS= read -r -d '' file
do
    if [ -d "$file" ]; then
        if ! [ $found_title ] && [[ $file =~ exercise[0-9]+\.[0-9]+$ ]]; then
            found_title=true
            echo "$found_title"
        fi
        echo "$file"
    elif [[ $file =~ README.md$ ]]; then
        cat $file >> $OUTPUT_FN
        printf "\n\n" >> $OUTPUT_FN
    fi
done