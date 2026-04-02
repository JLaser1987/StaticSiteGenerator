import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_noValue(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()    
    
    def test_empty(self):
        with self.assertRaises(Exception):
            LeafNode()

    def test_noTag(self):
        node = LeafNode(None, "I am untagged!")
        self.assertEqual(node.to_html(), "I am untagged!")

if __name__ == "__main__":
    unittest.main()