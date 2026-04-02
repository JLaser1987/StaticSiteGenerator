import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_notEq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        node3 = TextNode("This is a second text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)

    def test_validEnum(self):
        try:
            TextNode("This is a text node", TextType.TEXT)
        except Exception:
            self.fail("TextType failed on TextType.TEXT")
        try:
            TextNode("This is a text node", TextType.BOLD)
        except Exception:
            self.fail("TextType failed on TextType.BOLD")
        try:
            TextNode("This is a text node", TextType.ITALIC)
        except Exception:
            self.fail("TextType failed on TextType.ITALIC")
        try:
            TextNode("This is a text node", TextType.CODE)
        except Exception:
            self.fail("TextType failed on TextType.CODE")
        try:
            TextNode("This is a text node", TextType.LINK)
        except Exception:
            self.fail("TextType failed on TextType.LINK")
        try:
            TextNode("This is a text node", TextType.IMAGE)
        except Exception:
            self.fail("TextType failed on TextType.IMAGE")

    def test_invalidEnum(self):
        with self.assertRaises(AttributeError):
            TextNode("This is a text node", TextType.blob)

    def test_urlNone(self):
        TextNode("This is a text node", TextType.LINK, None)

    def test_plainText(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.toHtmlNode()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a plain text node")

    def test_boldText(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.toHtmlNode()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italicText(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = node.toHtmlNode()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_codeText(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = node.toHtmlNode()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_linkText(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = node.toHtmlNode()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node.value, 'This is a link text node')

    def test_plainText(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png")
        html_node = node.toHtmlNode()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png", "alt": "This is an image text node"})
            


if __name__ == "__main__":
    unittest.main()