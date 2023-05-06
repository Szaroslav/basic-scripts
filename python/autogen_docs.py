import os
import re
import json
from typing import Any, Iterator

#
# Script constants
#
DOCS_PATH: str                  = "test/autogen_docs/docs_test/"
DOCS_PATTERN: str               = DOCS_PATH.replace('/', r"\/")
DOCS_REGEXP: re.Pattern         = re.compile(DOCS_PATTERN)
DOC_FN: str                     ="README.md"
OUTPUT_FN: str                  = "output.md"
EX_PATTERN: str                 = r"[Ee]xercise\s?[0-9]+\.[0-9]+"
EX_REGEXP: re.Pattern           = re.compile(EX_PATTERN)
EX_README_PATTERN: str          = fr"{EX_PATTERN}\/README\.md$"
EX_README_REGEXP: re.Pattern    = re.compile(EX_README_PATTERN)
SECTION_PATTERN: str            = r"[Ss]ection\s?[0-9]+\.[0-9]+(\.[0-9]+)*"
SECTION_REGEXP: re.Pattern      = re.compile(SECTION_PATTERN)
CHAPTER_PATTERN: str            = r"[Cc]hapter\s?[0-9]+"
CHAPTER_REGEXP: re.Pattern      = re.compile(CHAPTER_PATTERN)


def ch_relative_path(path: str) -> str:
    """
    Create the chapter relative path
    """
    return re.sub(fr"{DOCS_PATH}{CHAPTER_PATTERN}\/", "./", path)


def parse_md_heading(text: str) -> str:
    """
    Parse markdown heading to normal text
    """
    return re.sub("^#+", '', text).strip()


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
                section_title = parse_md_heading(line)
            elif match := EX_REGEXP.search(line.strip()):
                title = match[0]
                read_mode = True
                content += line

    return content, title, section_title


def generate_section(path: str, data: dict[str, Any]) -> None:
    with open(path, "w") as file:
        file.write(f"# {data['title']}{2 * os.linesep}")
        for i, content in enumerate(data["contents"]):
            file.write(f"{content}{os.linesep}")

            # Write new lines between solutions
            if i < len(data["contents"]) - 1:
                file.write(2 * os.linesep)


def generate_chapter(path: str, data: list[tuple[str, str]]) -> None:
    def generate_section_table(file, data):
        def format_cell(text: str, width: int) -> str:
            return f"{text}{(width - len(text)) * ' '}"
        
        SECTION_HEADING, TITLE_HEADING = "Section", "Title"
        section_width, title_width = len(SECTION_HEADING), len(TITLE_HEADING)
        for section, title_link in data:
            section_width = max(section_width, len(section))
            title_width = max(title_width, len(title_link))

        file.write(f"| {format_cell(SECTION_HEADING, section_width)} | {format_cell(TITLE_HEADING, title_width)} |{os.linesep}")
        file.write(f"| {section_width * '-'} | {title_width * '-'} |{os.linesep}")
        for section, title_link in data:
            file.write(f"| {format_cell(section, section_width)} | {format_cell(title_link, title_width)} |{os.linesep}")

    with open(path, "w") as file:
        file.write(f"# {data['title']}{2 * os.linesep}")

        file.write(f"## Sections{2 * os.linesep}")
        sections = []
        for section in data["sections"]:
            if match := SECTION_REGEXP.match(section["title"]):
                sections.append(
                    (match[0], f"[{section['title'].replace(match[0], '').strip()}]({section['relative_link']})")
                )
        
        generate_section_table(file, sections)

        file.write(2 * os.linesep)
        for section in data["sections"]:
            file.write(f"## {section['title']}{os.linesep}")
            for exercise in section["exercises"]:
                file.write(f"- [{exercise['title']}]({exercise['relative_link']}){os.linesep}")
            file.write(os.linesep)


def main():
    title: str | None = None
    chapter_data: dict[str, Any] = {
        "title": None,
        "sections": []
    }
    section_data: dict[str, Any] = {
        "title": None,
        "contents": []
    }

    def clear_data(data: dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, list) or isinstance(value, dict):
                value.clear()
            else:
                data[key] = None

    def only_dirs(path: str) -> Iterator[tuple[str, str]]:
        dirs = list(filter(lambda x: os.path.isdir(os.path.join(path, x)), os.listdir(path)))
        dirs.sort()
        return zip(dirs, map(lambda x: os.path.join(path, x), dirs))

    for chapter, cpath in only_dirs(DOCS_PATH):
        clear_data(chapter_data)
        with open(os.path.join(cpath, DOC_FN), "r") as file:
            for line in file:
                if CHAPTER_REGEXP.search(line):
                    chapter_data["title"] = parse_md_heading(line)
                    break

        for section, spath in only_dirs(cpath):
            clear_data(section_data)
            chapter_data["sections"].append({})
            chapter_data["sections"][len(chapter_data["sections"]) - 1]["relative_link"] = ch_relative_path(spath)

            for exercise, epath in only_dirs(spath):
                if not DOC_FN in os.listdir(epath):
                    continue

                content, title, stitle = extract_erm_content(os.path.join(epath, DOC_FN))

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
                    "relative_link": ch_relative_path(epath)
                })

            generate_section(os.path.join(spath, DOC_FN), section_data)
        generate_chapter(os.path.join(cpath, DOC_FN), chapter_data)
        
    # print(json.dumps(chapter_data, indent=2))
        

if __name__ == "__main__":
    main()
