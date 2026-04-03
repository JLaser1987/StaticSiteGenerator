import shutil, os
from textnode import (TextNode, TextType)
from markdown_parse import generate_page

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    cleanCopy()

    generate_page("content/index.md", "template.html", "public/index.html")

def cleanCopy():
    shutil.rmtree("./public")
    shutil.copytree("./static", "./public")

main()