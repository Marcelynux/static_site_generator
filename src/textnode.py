from enum import Enum
from htmlnode import LeafNode

class TextTypes(Enum):
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, comparing_node):
        if (
                self.text == comparing_node.text and
                self.text_type == comparing_node.text_type and
                self.url == comparing_node.url
            ):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(textnode: TextNode):
    if textnode.text_type not in TextTypes:
        raise Exception("Invalid Texttype of Textnode. Given Texttype not inside Textype Enum.")
    else:
        if textnode.text_type == TextTypes.TEXT:
            return LeafNode( None, textnode.text)
        elif textnode.text_type == TextTypes.BOLD:
            return LeafNode( "b", textnode.text)
        elif textnode.text_type == TextTypes.ITALIC:
            return LeafNode( "i", textnode.text)
        elif textnode.text_type == TextTypes.CODE:
            return LeafNode( "code", textnode.text)
        elif textnode.text_type == TextTypes.LINK:
            return LeafNode( "a", textnode.text, {"href": textnode.url})
        elif textnode.text_type == TextTypes.IMAGE:
            return LeafNode( "img", "", {"src": textnode.url,"alt": textnode.text})