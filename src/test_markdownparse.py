import unittest

from textnode import TextNode, TextType
from markdown_parse import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, splitText, markdownToBlocks, blockToBlockType, BlockType


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        linkURL = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        matches = extract_markdown_links(
            f"This is text with a [link for]({linkURL})"
        )
        self.assertListEqual([("link for", linkURL)], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_full_split(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        newNodes = splitText(text)
        expected = [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
        self.assertListEqual(expected, newNodes)

    def test_full_split_nested(self):
        text = 'This is **text with an _italic_ word** and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        newNodes = splitText(text)
        expected = [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text with an ", TextType.BOLD),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word", TextType.BOLD),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
        self.assertListEqual(expected, newNodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdownToBlocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blockTypes(self):
        md = """
This is **bolded** paragraph

####This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This line
1. is mismatched
> and should
be a 
- paragraph

- This is a list
- with items

1. this is an
2. ordered
3. list

```
This is a code block
that is spanning
multiple lines
```

>this is
>a quote
>block
"""
        blocks = markdownToBlocks(md)
        blockTypes = []
        for block in blocks:
            blockTypes.append(blockToBlockType(block))
        self.assertEqual(
            blockTypes,
            [
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.CODE,
                BlockType.QUOTE,
            ],
        )


if __name__ == "__main__":
    unittest.main()