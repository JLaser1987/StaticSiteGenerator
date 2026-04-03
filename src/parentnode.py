from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise(ValueError("tag is required"))
        if self.children is None:
            raise(ValueError("children are required"))
        output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            string = child.to_html()
            output += string
        output += f"</{self.tag}>"
        return output