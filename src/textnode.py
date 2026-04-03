from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, textType, url=""):
        self.text = text
        self.textType = textType
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.textType == other.textType and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.textType.value}, {self.url})"
    
    def to_html(self):
        match self.textType:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})