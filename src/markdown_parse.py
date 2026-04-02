import re
from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == "" or delimiter is None:
        return old_nodes
    newNodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            nodeFragments = node.text.split(delimiter)
            if len(nodeFragments) % 2 != 1:
                raise Exception("invalid markdown: missing closing delimiter")
            tagged = False
            for fragment in nodeFragments:
                if not tagged:
                    newNodes.append(TextNode(fragment, node.textType, node.url))
                else:
                    newNodes.append(TextNode(fragment, text_type))
                tagged = not tagged
        else:
            newNodes.append(node)
    return newNodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    newNodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                newNodes.append(node)
                continue
            textFragments = re.split(r"!\[(?:.*?)\]\((.*?)\)", node.text)
            currentImage = 0
            flagged = False
            for fragment in textFragments:
                if fragment == "":
                    continue
                if not flagged or currentImage >= len(images):
                    newNodes.append(TextNode(fragment, node.textType, node.url))
                else:
                    newNodes.append(TextNode(images[currentImage][0], TextType.IMAGE, images[currentImage][1]))
                    currentImage += 1
                flagged = not flagged
        else:
            newNodes.append(node)
    return newNodes

def split_nodes_link(old_nodes):
    newNodes = []
    for node in old_nodes:
        if isinstance(node, TextNode):
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                newNodes.append(node)
                continue
            textFragments = re.split(r"\[(?:.*?)\]\((.*?)\)", node.text)
            currentLink = 0
            flagged = False
            for fragment in textFragments:
                if fragment == "":
                    continue
                if not flagged or currentLink >= len(links):
                    newNodes.append(TextNode(fragment, node.textType, node.url))
                else:
                    newNodes.append(TextNode(links[currentLink][0], TextType.LINK, links[currentLink][1]))
                    currentLink += 1
                flagged = not flagged
        else:
            newNodes.append(node)
    return newNodes

def splitText(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdownToBlocks(markdown):
    blocks = markdown.split("\n\n")
    finalBlocks = []
    for block in blocks:
        stripped= block.strip()
        if stripped != "":
            finalBlocks.append(stripped)
    return finalBlocks

def blockToBlockType(block):
    if block.startswith('#'):
         return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    type = BlockType.PARAGRAPH
    for i in range(len(lines)):
        if lines[i].startswith('>') and (type == BlockType.PARAGRAPH or type == BlockType.QUOTE):
            type = BlockType.QUOTE
        elif lines[i].startswith("- ") and (type == BlockType.PARAGRAPH or type == BlockType.UNORDERED_LIST):
            type = BlockType.UNORDERED_LIST
        elif lines[i].startswith(f"{i+1}. ") and (type == BlockType.PARAGRAPH or type == BlockType.ORDERED_LIST):
            type = BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    return type
