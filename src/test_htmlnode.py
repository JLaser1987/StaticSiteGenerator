import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_emptyProps(self):
        try:
            node = HTMLNode()
            node.props_to_html()
        except Exception:
            self.fail("could not convert None props")

    def test_propConversion(self):
        node = HTMLNode(props={"href":"https://www.google.com", "target": "_blank"})
        convertedProps = node.props_to_html()
        expectedResult = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(convertedProps, expectedResult)

    def test_creation(self):
        try:
            HTMLNode()
        except Exception:
            self.fail("failed to create empty HTMLNode")
        try:
            HTMLNode(tag="test")
        except Exception:
            self.fail("failed to create HTMLNode wtih only tag")
        try:
            HTMLNode(value="this is a test node")
        except Exception:
            self.fail("failed to create HTMLNode wtih only value")
        try:
            HTMLNode(children=[HTMLNode()])
        except Exception:
            self.fail("failed to create HTMLNode wtih only children")
        try:
            HTMLNode(props={"href":"https://www.google.com", "target": "_blank"})
        except Exception:
            self.fail("failed to create HTMLNode wtih only value")

if __name__ == "__main__":
    unittest.main()