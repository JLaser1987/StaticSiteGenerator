import shutil, os, sys
from textnode import (TextNode, TextType)
from markdown_parse import generate_page

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    # cleanCopy()

    basePath = sys.argv[1] if len(sys.argv) > 1 else  "/"
    generatePages("content", "template.html", "docs", basePath)

def generatePages(dir_path_content, template_path, dest_dir_path, basePath):
    dirs = os.listdir(dir_path_content)
    for dir in dirs:
        contentPath = os.path.join(dir_path_content, dir)
        destPath = os.path.join(dest_dir_path, dir)
        if os.path.isfile(contentPath):
            destPath = destPath.replace(".md", ".html")
            generate_page(contentPath, template_path, destPath, basePath)
        else:
            generatePages(contentPath, template_path, destPath, basePath)

def cleanCopy():
    shutil.rmtree("./public")
    shutil.copytree("./static", "./public")

main()