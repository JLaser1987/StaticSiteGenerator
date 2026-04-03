import shutil, os
from textnode import (TextNode, TextType)
from markdown_parse import generate_page

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    cleanCopy()

    # generate_page("content/index.md", "template.html", "public/index.html")
    generatePages("content", "template.html", "public")

def generatePages(dir_path_content, template_path, dest_dir_path):
    dirs = os.listdir(dir_path_content)
    for dir in dirs:
        contentPath = os.path.join(dir_path_content, dir)
        destPath = os.path.join(dest_dir_path, dir)
        if os.path.isfile(contentPath):
            destPath = destPath.replace(".md", ".html")
            generate_page(contentPath, template_path, destPath)
        else:
            generatePages(contentPath, template_path, destPath)

def cleanCopy():
    shutil.rmtree("./public")
    shutil.copytree("./static", "./public")

main()