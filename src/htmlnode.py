class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("self.to_html not implemented")

    def props_to_html(self):
        html_props = ""
        if self.props:
            for key, item in self.props.items():
                html_props += f' {key}="{item}"'
        return html_props

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid: self.value cannot be None")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid: self.tag cannot be None")
        if not self.children:
            raise ValueError("Invalid: self.children cannot be None")

        child_nodes = ""
        for child in self.children:
            child_nodes += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_nodes}</{self.tag}>"

    def __repr__(self):
        return f"tag: {self.tag}, children: {self.children}, props: {self.props}"
