import os
import re


DOCS_PATH: str= "test/autogen_docs/docs_test/"
DOCS_PATTERN: str= re.compile(DOCS_PATH.replace('/', "\/"))
OUTPUT_FN: str= "output.md"
EX_PATTERN: str= "[Ee]xercise\s?[0-9]+\.[0-9]+"
EX_REGEXP: re.Pattern= re.compile(EX_PATTERN)
EX_README_PATTERN: str= f"{EX_PATTERN}\/README\.md$"
EX_README_REGEXP: re.Pattern= re.compile(EX_README_PATTERN)
SECTION_PATTERN: str= "[Ss]ection\s?[0-9]+\.[0-9]+(\.[0-9]+)*"
SECTION_REGEXP: re.Pattern= re.compile(SECTION_PATTERN)
CHAPTER_PATTERN: str= "[Cc]hapter\s?[0-9]+"
CHAPTER_REGEXP: re.Pattern= re.compile(CHAPTER_PATTERN)


def extract_rm_content(path: str) -> tuple[str, str]:
    content: str | None = ""
    section_title: str | None = None

    with open(path, "r") as readme:
        read_mode: bool = False
        for line in readme:
            if read_mode:
                content += line
            elif SECTION_REGEXP.search(line.strip()):
                section_title = line
            elif EX_REGEXP.search(line.strip()):
                read_mode = True
                content += line

    return content, section_title



def main():
    title: str | None = None
    data = {
        "links": {},
        "links_lengths": {}
    }
    current_section: str | None = None

    for root, subdirs, files in os.walk(DOCS_PATH):
        subdirs.sort()
        # print(root)
        if match := SECTION_REGEXP.search(root):
            if current_section and current_section != match[0]:
                pass
            current_section = match[0]
        for file in files:
            full_path = os.path.join(root, file)
            # print(EX_README_REGEXP.search(full_path))
            if EX_README_REGEXP.search(full_path):
                print(extract_rm_content(full_path))



    # printf "" > $OUTPUT_FN

    # # resolve_path "section1.2/exercise1.05/README.md" "section1.2/exercise1.05/README.md"

    # find $DOCS_PATH -print0 | sort -z | while IFS= read -r -d '' path
    # do
    #     # echo "$path"
    #     # parse_path $file
    #     if [ ! -d $path ]; then
    #         if [[ $path =~ $EX_README_PATTERN ]] && [[ $title != $(sed '1q;d' $path) ]]; then
    #             title=$(sed '1q;d' $path)
    #             echo -e "$title\n" >> $OUTPUT_FN
    #         fi
            
    #         if [[ $path =~ README.md$ ]]; then
    #             write=false
    #             while IFS= read -r line
    #             do
    #                 if [[ $line =~ $EX_PATTERN ]]; then
    #                     write=true
    #                 fi
    #                 if $write; then
    #                     # echo $line
    #                     echo $line >> $OUTPUT_FN
    #                 fi
    #             done < $path
    #         fi
    #     else
    #         pattern="$EX_PATTERN\$"
    #         if [[ $path =~ $pattern ]]; then
    #             parsed_path=$(parse_path $path)
    #             section=$(echo "$parsed_path" | sed -E -n "s/.*($SECTION_PATTERN).*/\1/p" | tr '[:upper:]' '[:lower:]')
    #             echo "$section"
    #             if ! [ "${chapter_links_lengths[$section]}" ]; then
    #                 chapter_links_lengths[$section]=1
    #             else
    #                 ((chapter_links_lengths[$section]++))
    #             fi

    #             chapter_links[$section,${chapter_links_lengths[$section]}]=$(resolve_path $parsed_path "" | sed -E "s/$CHAPTER_PATTERN\///")
    #             # echo "$section,${chapter_links_lengths[$section]}"
    #         fi
    #     fi
    #     # echo "${!chapter_links[@]}"
    # done


if __name__ == "__main__":
    main()