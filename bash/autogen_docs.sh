#!/bin/bash

# Global constants and variables
DOCS_PATH="test/autogen_docs/docs_test/"
DOCS_PATTERN=$(echo "$DOCS_PATH" | sed 's/\//\\\//g')
OUTPUT_FN=output.md
EX_PATTERN="[Ee]xercise\s?[0-9]+\.[0-9]+"
EX_README_PATTERN="$EX_PATTERN/README.md$"
SECTION_PATTERN="[Ss]ection\s?[0-9]+\.[0-9]+(\.[0-9]+)*"
CHAPTER_PATTERN="[Cc]hapter\s?[0-9]+"

parse_path () {
    echo "$1" | sed "s/$DOCS_PATTERN//"
}

# Resolve 2 relative paths
resolve_path () {
    if [[ $1 == "" ]]; then
        echo "resolve_path: [Error] First argument missing"
        return 1
    fi
    # if [[ $2 == "" ]]; then
    #     echo "resolve_path: [Error] Second argument missing"
    #     return 2
    # fi

    local splitted_path1=(${1//// })
    local splitted_path2=(${2//// })
    
    local count=0
    local has_current1=false
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
    local has_current2=false
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

    echo "$resolved_path" # | sed 's/^\.\///'
}

main () {
    local title=""
    declare -gA chapter_links
    declare -A chapter_links_lengths

    printf "" > $OUTPUT_FN

    # resolve_path "section1.2/exercise1.05/README.md" "section1.2/exercise1.05/README.md"

    find $DOCS_PATH -print0 | sort -z | while IFS= read -r -d '' path
    do
        # echo "$path"
        # parse_path $file
        if [ ! -d $path ]; then
            if [[ $path =~ $EX_README_PATTERN ]] && [[ $title != $(sed '1q;d' $path) ]]; then
                title=$(sed '1q;d' $path)
                echo -e "$title\n" >> $OUTPUT_FN
            fi
            
            if [[ $path =~ README.md$ ]]; then
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
                done < $path
            fi
        else
            pattern="$EX_PATTERN\$"
            if [[ $path =~ $pattern ]]; then
                parsed_path=$(parse_path $path)
                section=$(echo "$parsed_path" | sed -E -n "s/.*($SECTION_PATTERN).*/\1/p" | tr '[:upper:]' '[:lower:]')
                echo "$section"
                if ! [ "${chapter_links_lengths[$section]}" ]; then
                    chapter_links_lengths[$section]=1
                else
                    ((chapter_links_lengths[$section]++))
                fi

                chapter_links[$section,${chapter_links_lengths[$section]}]=$(resolve_path $parsed_path "" | sed -E "s/$CHAPTER_PATTERN\///")
                # echo "$section,${chapter_links_lengths[$section]}"
            fi
        fi
        # echo "${!chapter_links[@]}"
    done

    declare -A variable
    variable=([a]=1 [b]=2)
    echo "${!chapter_links[@]}"
    for key in "${!variable[@]}"; do
        echo "yes, sir"
        echo "$key: ${variable[$key]}"
    done
}

main
