import unittest

from textnode import BlockTypes
from util import (
    markdown_to_blocks,
    block_to_block_type
)


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockTypes.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockTypes.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockTypes.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockTypes.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockTypes.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockTypes.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()