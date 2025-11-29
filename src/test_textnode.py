import unittest

from textnode import TextNode, TextTypes, text_node_to_html_node
from util import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextTypes.BOLD)
        node2 = TextNode("This is a text node", TextTypes.BOLD)
        node3 = TextNode("Another testnode.", TextTypes.CODE)
        node4 = TextNode("URL Node", TextTypes.LINK, "www.wikipedia.de")
        node5 = TextNode("URL Node", TextTypes.LINK, "www.wikipedia.de")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node4)
        self.assertEqual(node4, node5)

    def test_eq2(self):
        node = TextNode("This is a text node", TextTypes.TEXT)
        node2 = TextNode("This is a text node", TextTypes.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextTypes.TEXT)
        node2 = TextNode("This is a text node", TextTypes.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextTypes.TEXT)
        node2 = TextNode("This is a text node2", TextTypes.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextTypes.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextTypes.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextTypes.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, plain text, https://www.boot.dev)", repr(node)
        )

    def test_text_to_leaf(self):
        node = TextNode("This is a text node", TextTypes.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image_to_leaf(self):
        node = TextNode("This is an image", TextTypes.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold_to_leaf(self):
        node = TextNode("This is bold", TextTypes.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_link_to_leaf(self):
        node = TextNode("This is an image", TextTypes.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is an image")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.boot.dev"},
        )

if __name__ == "__main__":
    unittest.main()