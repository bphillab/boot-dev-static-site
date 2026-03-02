import re

from src.block import block_to_block_type, BlockType
from src.htmlnode import HTMLNode, text_node_to_html_node, ParentNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for i in old_nodes:
        if i.text_type == TextType.TEXT:
            text = i.text
            url = i.url
            new_text = text.split(delimiter)

            if len(new_text)%2 == 0:
                raise Exception("No matching delimiter found")
            for j in range(len(new_text)):
                if j%2 == 0:
                    new_nodes.append(TextNode(new_text[j], TextType.TEXT,url))
                else:
                    new_nodes.append(TextNode(new_text[j], text_type,url))
        else:
            new_nodes.append(i)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
def split_nodes_image(old_nodes):
    new_nodes = []
    for i in old_nodes:
        text = i.text
        type = i.text_type
        url = i.url
        images = extract_markdown_images(text)
        for image in images:
            splt = text.split(f"![{image[0]}]({image[1]})",1)
            new_nodes.append(TextNode(splt[0], type, url))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = splt[1]
        if text:
            new_nodes.append(TextNode(text, type,url))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for i in old_nodes:
        text = i.text
        type = i.text_type
        url = i.url
        links = extract_markdown_links(text)
        for link in links:
            splt = text.split(f"[{link[0]}]({link[1]})",1)
            new_nodes.append(TextNode(splt[0], i.text_type,url))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = splt[1]
        if text:
            new_nodes.append(TextNode(text, type,url))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(doc):
    doc = doc.strip()
    if not doc:
        return []
    blocks = re.split(r"\n{2,}", doc)
    return [block.strip() for block in blocks if block.strip()]

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        tag = get_html_tag(block_type)
        if block_type == BlockType.PARAGRAPH:
            markdown_block = markdown_block.replace("\n", " ")
        if not block_type == BlockType.CODE:
            children = text_to_children(markdown_block)
        if block_type == BlockType.CODE:
            special_text = markdown_block[3:-3]
            if special_text.startswith("\n"):
                special_text = special_text[1:]
            txt_node = [TextNode(special_text, TextType.CODE)]
            children = [text_node_to_html_node(i) for i in txt_node]

        html_node = ParentNode(tag=tag, children=children)
        html_nodes.append(html_node)
    root = ParentNode(tag="div", children=html_nodes)
    return root

def get_html_tag(block_type):
    match block_type:
        case BlockType.HEADING:
            return "h1"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.PARAGRAPH:
            return "p"
        case _:
            raise Exception("Not implemented")

def text_to_children(text):
    if not text:
        return []
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]
