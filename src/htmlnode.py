from dataclasses import dataclass

from src.textnode import TextType


@dataclass
class HTMLNode:
    tag:str|None = None
    value:str|None = None
    children:list[HTMLNode] | None = None
    props:dict[str, str]| None = None

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        tmp = ""
        if not self.props:
            return tmp
        for key, value in self.props.items():
            tmp += f'{key}="{value}" '
        return tmp[:-1]

    def __repr__(self) -> str:
        return f"HTMLNode(tag='{self.tag}', attributes={self.attributes}, children={len(self.children)}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag:str|None, value:str, props:dict[str, str]| None = None):
        super().__init__(value=value, tag=tag, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("Value cannot be empty")
        if not self.tag:
            return self.value
        props_html = self.props_to_html()
        props_segment = "" if not props_html else f" {props_html}"
        return f"<{self.tag}{props_segment}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag='{self.tag}', attributes={self.attributes}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self,tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag cannot be empty")
        if not self.children:
            raise ValueError("Children cannot be empty")
        return f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value=text_node.text, props={"src": text_node.url, "alt": text_node.text})
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)

        case _:
            raise Exception("Not implemented")
