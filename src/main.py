from generating_functions import generate_pages_recursive
from copy_function import copy_static_to_public
import sys
def main():
    copy_static_to_public()
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
main()