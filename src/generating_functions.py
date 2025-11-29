from util import markdown_to_html_node, extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as file1:
        markdown_file = file1.read()
    with open(template_path, encoding="utf-8") as file2:
        template_file = file2.read()

    html_node = markdown_to_html_node(markdown_file)
    html_string = html_node.to_html()
    title = extract_title(markdown_file)

    html_with_title = template_file.replace("{{ Title }}", title)
    final_html = html_with_title.replace("{{ Content }}", html_string)

    if not os.path.exists(os.path.dirname(dest_path)):
        print(f"creating dir '{os.path.dirname(dest_path)}'")
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(final_html)
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.isdir(dir_path_content):
        raise Exception("Provided content path is not a directory")
    entries_in_content_dir = os.listdir(dir_path_content)
    for entry in entries_in_content_dir:
        entry_path = os.path.join(dir_path_content, entry)
        entry_dest_path = os.path.join(dest_dir_path, entry)
        if not os.path.isfile(entry_path):
            generate_pages_recursive(entry_path, template_path, entry_dest_path)
        else:
            entry_dest_path_html = entry_dest_path.replace(".md",".html")
            if not os.path.exists(os.path.dirname(entry_dest_path)):
                os.makedirs(os.path.dirname(entry_dest_path))
            generate_page(entry_path, template_path, entry_dest_path_html)
    return