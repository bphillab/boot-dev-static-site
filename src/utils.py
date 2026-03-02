import re

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
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(doc):
    blocks = [i.strip() for i in doc.split("\n\n")]
    return [block for block in blocks if block]
