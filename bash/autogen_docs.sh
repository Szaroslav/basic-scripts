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

# Resolve 2 relative paths
resolve_path () {
    if [[ $1 == "" ]]; then
        echo "resolve_path: [Error] First argument missing"
        return 1
    fi
    if [[ $2 == "" ]]; then
        echo "resolve_path: [Error] Second argument missing"
        return 2
    fi

    splitted_path1=(${1//// })
    splitted_path2=(${2//// })
    
    count=0
    has_current1=false
    for i in "${!splitted_path1[@]}"; do
        if [[ ${splitted_path1[i]} == "." ]]; then
            ((count=count+1))
            has_current1=true
        fi
    done
    if [ $count -gt 1 ]; then
        echo "resolve_path: [Error] First argument has more than 1 current directory symbols ('.')"
        return 3
    fi

    count=0
    has_current2=false
    for i in "${!splitted_path2[@]}"; do
        if [[ ${splitted_path2[i]} == "." ]]; then
            ((count=count+1))
            has_current2=true
        fi
    done
    if [ $count -gt 1 ]; then
        echo "resolve_path: [Error] Second argument has more than 1 current directory symbols ('.')"
        return 4
    fi
    # echo "ddd $2"

    resolved_path="."
    for i in "${!splitted_path1[@]}"; do
        resolved_path="$resolved_path/${splitted_path1[i]}"
    done
    for i in "${!splitted_path2[@]}"; do
        resolved_path="$resolved_path/${splitted_path2[i]}"
    done

    echo "$resolved_path" | sed 's/^\.\///'
}



printf "" > $OUTPUT_FN

resolve_path "section1.2/exercise1.05/README.md" "section1.2/exercise1.05/README.md"

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
