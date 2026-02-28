from dataclasses import dataclass

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
        for key, value in self.props.items():
            tmp += f'{key}="{value}" '
        return tmp[:-1]

    def __repr__(self) -> str:
        return f"HTMLNode(tag='{self.tag}', attributes={self.attributes}, children={len(self.children)}, props={self.props})"