import os
import re
from typing import Any


DOCS_PATH: str= "test/autogen_docs/docs_test/"
DOCS_PATTERN: str= DOCS_PATH.replace('/', "\/")
DOCS_REGEXP: re.Pattern= re.compile(DOCS_PATTERN)
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


def generate_section(path: str, data: dict[str, Any]) -> None:
    with open(path, "w") as file:
        file.write(f"{data['title']}\n")
        for i, content in enumerate(data["contents"]):
            print(path)
            file.write(f"{content}\n")
            if i < len(data["contents"]) - 1:
                file.write("\n\n")


def main():
    title: str | None = None
    section_data: dict[str, Any] = {
        "title": None,
        "contents": [],
        "links": {},
    }
    current_section: str | None = None

    def clear_data(data: dict[str, Any]):
        data["title"] = None
        data["contents"].clear()
        data["links"].clear()

    for root, subdirs, files in os.walk(DOCS_PATH):
        subdirs.sort()
        print(root)
        if match := re.search(f"{SECTION_PATTERN}$", root):
            if current_section and current_section != match[0]:
                generate_section(f"{root}/README.md", section_data)
                clear_data(section_data)
            current_section = match[0]
        for file in files:
            full_path = os.path.join(root, file)
            # print(EX_README_REGEXP.search(full_path))
            if EX_README_REGEXP.search(full_path):
                content, title = extract_rm_content(full_path)
                if not section_data["title"]: section_data["title"] = title
                section_data["contents"].append(content)
        

if __name__ == "__main__":
    main()