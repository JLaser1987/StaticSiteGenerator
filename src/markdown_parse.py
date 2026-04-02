from textnode import TextNode, TextType

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