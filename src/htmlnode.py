class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self. children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        properties_string = ""
        if self.props == None or len(self.props) == 0:
            return properties_string
        else:
            for property in self.props:
                properties_string += f' {property}="{self.props[property]}"'
            return properties_string

    def __repr__(self):
        return f"HTML Node(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value for Leafnode specified.")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag for parentnode specified.")
        if self.children == None:
            raise ValueError("No child for parentnode specified.")
        else:
            child_html_string = ""
            for child in self.children:
                child_html_string += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{child_html_string}</{self.tag}>"