from generating_functions import generate_pages_recursive
from copy_function import copy_static_to_public
def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")
    
main()