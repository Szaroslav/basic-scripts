import re


DOCS_PATH = "test/autogen_docs/docs_test/"
DOCS_PATTERN = re.compile(DOCS_PATH.replace('/', "\/"))
OUTPUT_FN = "output.md"
EX_PATTERN = re.compile("[Ee]xercise\s?[0-9]+\.[0-9]+")
EX_README_PATTERN = re.compile("$EX_PATTERN/README.md$")
SECTION_PATTERN = re.compile("[Ss]ection\s?[0-9]+\.[0-9]+(\.[0-9]+)*")
CHAPTER_PATTERN = re.compile("[Cc]hapter\s?[0-9]+")
