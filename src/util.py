from textnode import TextNode, TextTypes, BlockTypes, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextTypes.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextTypes.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextTypes.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextTypes.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type !=TextTypes.TEXT:
            new_nodes.append(node)
            continue

        elif delimiter not in node.text:
            new_nodes.append(node)
            continue
        
        elif len(node.text.split(delimiter)) % 2 == 0:
            raise Exception(f"Closing Delimiter '{delimiter}' not found in Textnode.")
        else:
            new_split_nodes = []
            if (delimiter == "**" and text_type == TextTypes.BOLD or
                delimiter == "_" and text_type == TextTypes.ITALIC or
                delimiter == "`" and text_type == TextTypes.CODE):
                split_nodes = node.text.split(delimiter)
                for i in range(0, len(split_nodes)):
                    if split_nodes[i] == "":
                        continue
                    if i % 2 == 0:
                        new_split_nodes.append(TextNode(split_nodes[i], TextTypes.TEXT))

                    else:
                        new_split_nodes.append(TextNode(split_nodes[i], text_type))

                new_nodes.extend(new_split_nodes)

            else:
                raise Exception(f"Delimiter '{delimiter}' and {text_type} are incompatible.")
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type !=TextTypes.TEXT:
            new_nodes.append(node)
            continue

        else:
            new_split_nodes = []
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            split_nodes = re.split(r"!\[[^\[\]]*\]\([^\(\)]*\)", node.text)
            image_index = 0
            #Überprüfen, ob letztes Element ein leerer String ist
            if not split_nodes[-1]:
                split_nodes = split_nodes[:-1]
            #Extrahierte Image-Tupel alternierend in den gesplitteten Text einfügen
            for i in range(0, len(images) + len(split_nodes)):
                if i % 2 != 0:
                    split_nodes.insert(i,images[image_index])
                    image_index += 1
            for i in range(0, len(split_nodes)):
                if split_nodes[i] == "":
                    continue
                if i % 2 == 0:
                    new_split_nodes.append(TextNode(split_nodes[i], TextTypes.TEXT))

                else:
                    new_split_nodes.append(TextNode(split_nodes[i][0], TextTypes.IMAGE, split_nodes[i][1]))

            new_nodes.extend(new_split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type !=TextTypes.TEXT:
            new_nodes.append(node)
            continue

        else:
            new_split_nodes = []
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
                continue
            split_nodes = re.split(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", node.text)
            link_index = 0
            #Überprüfen, ob letztes Element ein leerer String ist
            if not split_nodes[-1]:
                split_nodes = split_nodes[:-1]
            #Extrahierte Link-Tupel alternierend in den gesplitteten Text einfügen
            for i in range(0, len(links) + len(split_nodes)):
                if i % 2 != 0:
                    split_nodes.insert(i,links[link_index])
                    link_index += 1
            
            for i in range(0, len(split_nodes)):
                if split_nodes[i] == "":
                    continue
                if i % 2 == 0:
                    new_split_nodes.append(TextNode(split_nodes[i], TextTypes.TEXT))

                else:
                    new_split_nodes.append(TextNode(split_nodes[i][0], TextTypes.LINK, split_nodes[i][1]))

            new_nodes.extend(new_split_nodes)
    return new_nodes

def extract_markdown_images(text):
    img_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return img_list

def extract_markdown_links(text):
    links_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return links_list

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("Provided markdown file does not have a header.")

def markdown_to_blocks(markdown):
    md_blocks = []
    split_md = markdown.split("\n\n")
    for block in split_md:
        if block:
            md_blocks.append(block.strip())
    return md_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockTypes.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockTypes.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockTypes.PARAGRAPH
        return BlockTypes.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockTypes.PARAGRAPH
        return BlockTypes.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockTypes.PARAGRAPH
            i += 1
        return BlockTypes.ORDERED_LIST
    return BlockTypes.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockTypes.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockTypes.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockTypes.CODE:
        return code_to_html_node(block)
    if block_type == BlockTypes.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockTypes.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockTypes.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextTypes.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
    
