import unittest
from util import markdown_to_html_node
from textnode import TextNode, TextTypes
from util import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    extract_title,
    BlockTypes
)

class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.CODE)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("code block", TextTypes.CODE),
                TextNode(" word", TextTypes.TEXT),
            ])
        
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextTypes.ITALIC)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("italic block", TextTypes.ITALIC),
                TextNode(" word", TextTypes.TEXT),
            ])
        
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("bold block", TextTypes.BOLD),
                TextNode(" word", TextTypes.TEXT),
            ])
        
    def test_split_nodes_delimiter_incompatible(self):
        node = TextNode("This is text with a _italic block_ word", TextTypes.TEXT)
        with self.assertRaisesRegex(Exception, "Delimiter '_' and TextTypes.BOLD are incompatible."):
            split_nodes_delimiter([node], "_", TextTypes.BOLD)

    def test_split_nodes_delimiter_not_found(self):
        node = TextNode("This is text with a **bold block** word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextTypes.ITALIC)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a **bold block** word", TextTypes.TEXT)
            ])

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("This is text with a **bold block** word", TextTypes.TEXT)
        node2 = TextNode("This is text with a _italic block_ word", TextTypes.TEXT)
        node_list = [node1, node2]
        new_nodes = split_nodes_delimiter(node_list, "**", TextTypes.BOLD)
        new_nodes2 = split_nodes_delimiter(new_nodes, "_", TextTypes.ITALIC)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("bold block", TextTypes.BOLD),
                TextNode(" word", TextTypes.TEXT),
                TextNode("This is text with a _italic block_ word", TextTypes.TEXT)
            ])
        self.assertEqual(
            new_nodes2, 
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("bold block", TextTypes.BOLD),
                TextNode(" word", TextTypes.TEXT),
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("italic block", TextTypes.ITALIC),
                TextNode(" word", TextTypes.TEXT),
            ])
        
    def test_split_nodes_delimiter_no_closing_delimiter(self):
        node = TextNode("This is text with a _italic block word", TextTypes.TEXT)
        with self.assertRaisesRegex(Exception, "Closing Delimiter '_' not found in Textnode."):
            split_nodes_delimiter([node], "_", TextTypes.ITALIC)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("bolded", TextTypes.BOLD),
                TextNode(" word", TextTypes.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextTypes.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("bolded", TextTypes.BOLD),
                TextNode(" word and ", TextTypes.TEXT),
                TextNode("another", TextTypes.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextTypes.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("bolded word", TextTypes.BOLD),
                TextNode(" and ", TextTypes.TEXT),
                TextNode("another", TextTypes.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextTypes.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.TEXT),
                TextNode("italic", TextTypes.ITALIC),
                TextNode(" word", TextTypes.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextTypes.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextTypes.BOLD),
                TextNode(" and ", TextTypes.TEXT),
                TextNode("italic", TextTypes.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextTypes.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("code block", TextTypes.CODE),
                TextNode(" word", TextTypes.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.TEXT),
                TextNode("image", TextTypes.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextTypes.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.TEXT),
                TextNode("image", TextTypes.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextTypes.TEXT),
                TextNode(
                    "second image", TextTypes.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.TEXT),
                TextNode("link", TextTypes.LINK, "https://boot.dev"),
                TextNode(" and ", TextTypes.TEXT),
                TextNode("another link", TextTypes.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextTypes.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(
            text_nodes,
            [
                TextNode("This is ", TextTypes.TEXT),
                TextNode("text", TextTypes.BOLD),
                TextNode(" with an ", TextTypes.TEXT),
                TextNode("italic", TextTypes.ITALIC),
                TextNode(" word and a ", TextTypes.TEXT),
                TextNode("code block", TextTypes.CODE),
                TextNode(" and an ", TextTypes.TEXT),
                TextNode("obi wan image", TextTypes.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextTypes.TEXT),
                TextNode("link", TextTypes.LINK, "https://boot.dev"),
            ]
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_Markdown_title_extract(self):
        md = """
# This title was extracted.

This is text 
doesnt matter.
"""

        result = extract_title(md)
        self.assertEqual(result, "This title was extracted.")

    def test_Markdown_title_extract_fail(self):
        md = """
This title was not extracted.

This is text 
doesnt matter.
"""
        with self.assertRaisesRegex(Exception, "Provided markdown file does not have a header."):
            extract_title(md)
if __name__ == "__main__":
    unittest.main()