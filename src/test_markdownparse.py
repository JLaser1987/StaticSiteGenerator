import unittest

from textnode import TextNode, TextType
from markdown_parse import split_nodes_delimiter


class TestMarkdownParse(unittest.TestCase):
    def test_textParse(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.TEXT)
        expectedNew = [
                        TextNode("This is plain text", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes, expectedNew)
    
    def test_boldParse(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expectedNew = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("bold", TextType.BOLD),
                        TextNode(" word", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes, expectedNew)

    def test_codeParse(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expectedNew = [
                        TextNode("This is text with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes, expectedNew)

    def test_codeParse(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expectedNew = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" word", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes, expectedNew)


if __name__ == "__main__":
    unittest.main()