import os
import re
import json
from typing import Any


DOCS_PATH: str= "test/autogen_docs/docs_test/"
DOCS_PATTERN: str= DOCS_PATH.replace('/', r"\/")
DOCS_REGEXP: re.Pattern= re.compile(DOCS_PATTERN)
OUTPUT_FN: str= "output.md"
EX_PATTERN: str= r"[Ee]xercise\s?[0-9]+\.[0-9]+"
EX_REGEXP: re.Pattern= re.compile(EX_PATTERN)
EX_README_PATTERN: str= fr"{EX_PATTERN}\/README\.md$"
EX_README_REGEXP: re.Pattern= re.compile(EX_README_PATTERN)
SECTION_PATTERN: str= r"[Ss]ection\s?[0-9]+\.[0-9]+(\.[0-9]+)*"
SECTION_REGEXP: re.Pattern= re.compile(SECTION_PATTERN)
CHAPTER_PATTERN: str= r"[Cc]hapter\s?[0-9]+"
CHAPTER_REGEXP: re.Pattern= re.compile(CHAPTER_PATTERN)


def ch_relative_path(path: str) -> str:
    """
    Create the chapter relative path
    """
    return re.sub(fr"{DOCS_PATH}{CHAPTER_PATTERN}\/", "./", path)


def extract_erm_content(path: str) -> tuple[str, str, str]:
    """
    Extract the exercise README content
    """
    content: str | None = ""
    title: str | None = None
    section_title: str | None = None

    with open(path, "r") as readme:
        read_mode: bool = False
        for line in readme:
            if read_mode:
                content += line
            elif SECTION_REGEXP.search(line.strip()):
                section_title = re.sub("^#+", '', line).strip()
            elif match := EX_REGEXP.search(line.strip()):
                title = match[0]
                read_mode = True
                content += line

    return content, title, section_title


def generate_section(path: str, data: dict[str, Any]) -> None:
    with open(path, "w") as file:
        file.write(f"# {data['title']}\n")
        for i, content in enumerate(data["contents"]):
            file.write(f"{content}\n")
            if i < len(data["contents"]) - 1:
                file.write("\n\n")


def generate_chapter(path: str, data: dict[str, Any]) -> None:
    def generate_section_table(file, data):
        pass
    pass


def main():
    title: str | None = None
    chapter_data: dict[str, Any] = {
        "title": None,
        "sections": []
    }
    current_chapter: str | None = None
    section_data: dict[str, Any] = {
        "title": None,
        "contents": []
    }
    current_section: str | None = None

    def clear_data(data: dict[str, Any]):
        data["title"] = None
        data["contents"].clear()

    for root, subdirs, files in os.walk(DOCS_PATH):
        subdirs.sort()
        # print(root)
        if match := re.search(f"{CHAPTER_PATTERN}$", root):
            current_chapter = match[0]
            with open(f"{root}/README.md", "r") as readme:
                chapter_data["title"] = readme.readline().strip()
                print(chapter_data["title"])

        elif match := re.search(f"{SECTION_PATTERN}$", root):
            if current_section and current_section != match[0]:
                generate_section(f"{root}/README.md", section_data)
                clear_data(section_data)
            current_section = match[0]
            chapter_data["sections"].append({})
            chapter_data["sections"][len(chapter_data["sections"]) - 1]["relative_link"] = ch_relative_path(root)

        for file in files:
            full_path = os.path.join(root, file)
            if EX_README_REGEXP.search(full_path):
                content, title, stitle = extract_erm_content(full_path)

                # Set section data
                if not section_data["title"]: section_data["title"] = stitle
                section_data["contents"].append(content)

                # Set chapter data
                recent_chapter_data = chapter_data["sections"][len(chapter_data["sections"]) - 1]
                recent_chapter_data["title"] = stitle
                if not recent_chapter_data.get("exercises"):
                    recent_chapter_data["exercises"] = []
                recent_chapter_data["exercises"].append({
                    "title": title,
                    "relative_link": ch_relative_path(root)
                })
        
    print(json.dumps(chapter_data, indent=2))
        

if __name__ == "__main__":
    main()