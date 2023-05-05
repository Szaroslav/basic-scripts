#!/bin/bash

# Global constants and variables
DOCS_PATH="test/autogen_docs/chapter01/"
DOCS_PATTERN=$(echo "$DOCS_PATH" | sed 's/\//\\\//g')
OUTPUT_FN=output.md
EX_PATTERN="[Ee]xercise ?[0-9]+\.[0-9]+"
EX_README_PATTERN="$EX_PATTERN/README.md$"
title=""

parse_path () {
    echo "$1" | sed "s/$DOCS_PATTERN//"
}

resolve_path () {
    PATTERN="chapter01\/(.*)"
    echo "$1 $2"
}



printf "" > $OUTPUT_FN

resolve_path "co" "tam?"

find $DOCS_PATH -print0 | sort -z | while IFS= read -r -d '' file
do
    # echo "$file"
    parse_path $file
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
