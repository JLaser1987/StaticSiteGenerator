import re, os
from enum import Enum
from textnode import TextNode, TextType
from parentnode import ParentNode

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
                    flagged = not flagged
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

def textToChildren(text):
    nodes = splitText(text)
    htmlNodes = []
    for node in nodes:
        htmlNodes.append(node.to_html())
    return htmlNodes

def paragraphNode(block):
    return ParentNode("p", textToChildren(block.replace("\n", " ")))

def headingNode(block):
    count = 0
    blockText = block
    while blockText.startswith("#") and count <= 6:
        count += 1
        blockText = blockText[1:].strip()
    return ParentNode(f"h{count}", textToChildren(blockText))

def codeNode(block):
    blockText = block.replace("```", "").strip()
    node = TextNode(f"{blockText}\n", TextType.CODE)
    return ParentNode("pre", [node.to_html()])

def quoteBlock(block):
    lines = block.split("\n")
    processedLines = []
    for line in lines:
        processedLines.append(line.replace(">", "").strip())
    processedBlock = "\n".join(processedLines)
    return ParentNode("blockquote", textToChildren(processedBlock))

def linesToList(lines):
    listNodes = []
    for line in lines:
        listNodes.append(ParentNode("li", textToChildren(line)))
    return listNodes

def unorderedListBlock(block):
    lines = block.split("\n")
    processedLines = []
    for line in lines:
        processedLines.append(line.replace("-", "").strip())
    listNodes = linesToList(processedLines)
    return ParentNode("ul", listNodes)

def orderedListBlock(block):
    lines = block.split("\n")
    processedLines = []
    for line in lines:
        processedLines.append(line[2:].strip())
    listNodes = linesToList(processedLines)
    return ParentNode("ol", listNodes)

def blockToNode(block, blockType):
    match blockType:
        case BlockType.PARAGRAPH:
            return paragraphNode(block)
        case BlockType.HEADING:
            return headingNode(block)
        case BlockType.CODE:
            return codeNode(block)
        case BlockType.QUOTE:
            return quoteBlock(block)
        case BlockType.UNORDERED_LIST:
            return unorderedListBlock(block)
        case BlockType.ORDERED_LIST:
            return orderedListBlock(block)

def markdownto_html(markdown):
    blocks = markdownToBlocks(markdown)
    convertedBlocks = []
    for block in blocks:
        blockType = blockToBlockType(block)
        convertedBlocks.append(blockToNode(block, blockType))
    return ParentNode("div", convertedBlocks)

def extractTitle(markdown):
    blocks = markdownToBlocks(markdown)
    for block in blocks:
        if re.match(rf"^{re.escape('#')}(?![{re.escape('#')}])", block):
            return block.replace("#", "").strip()
    raise Exception("no header found")
        
def generate_page(from_path, template_path, dest_path, basePath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(from_path) as srcFile, open(template_path) as templateFile, open(dest_path, "w") as destinationFile:
        src = srcFile.read()
        template = templateFile.read()
        content = markdownto_html(src).to_html()
        title = extractTitle(src)
        finalHTML = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', f'href="{basePath}').replace('src="/', f'src="{basePath}')
        destinationFile.write(finalHTML)
