from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, \
    split_nodes_link, text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType
import unittest
class TestSplitDelimiter(unittest.TestCase):
    def test_split_delimiter(self):
        text = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([text], "__", TextType.TEXT)
        self.assertEqual(len(new_nodes), 1)

    def test_split_bold_delimiter(self):
        text = TextNode("This is a **text** node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([text], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
    def test_raises_exception_no_matched_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_many_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(
            text
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_many_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(
            text
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links(
            "This is text with an (https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

class TestSplitLinkImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ], new_nodes
        )

    def test_split_no_links_images(self):
        node = TextNode(
            "This is text with an (https://i.imgur.com/zjjcJKZ.png) and another (https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
class TestSplitImagesThenLinks(unittest.TestCase):
    def test_mixed_pipeline(self):
        nodes = [TextNode("a ![img](i) b [link](l) c", TextType.TEXT)]
        step1 = split_nodes_image(nodes)
        got = split_nodes_link(step1)
        want = [
            TextNode("a ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "i"),
            TextNode(" b ", TextType.TEXT),
            TextNode("link", TextType.LINK, "l"),
            TextNode(" c", TextType.TEXT),
        ]
        self.assertEqual(got, want)
class TestTextToTextnodes(unittest.TestCase):
    def test_plain_text(self):
        text = "just text"
        got = text_to_textnodes(text)
        want = [TextNode("just text", TextType.TEXT)]
        self.assertEqual(got, want)

    def test_bold_italic_code(self):
        text = "a **bold** b __it__ c `code` d"
        got = text_to_textnodes(text)
        want = [
            TextNode("a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" b ", TextType.TEXT),
            TextNode("it", TextType.ITALIC),
            TextNode(" c ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" d", TextType.TEXT),
        ]
        self.assertEqual(got, want)

    def test_images_and_links(self):
        text = "a ![img](i) b [link](l) c"
        got = text_to_textnodes(text)
        want = [
            TextNode("a ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "i"),
            TextNode(" b ", TextType.TEXT),
            TextNode("link", TextType.LINK, "l"),
            TextNode(" c", TextType.TEXT),
        ]
        self.assertEqual(got, want)

    def test_mixed_all(self):
        text = "x **b** ![i](u) __it__ [ln](v) `c` y"
        got = text_to_textnodes(text)
        want = [
            TextNode("x ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("i", TextType.IMAGE, "u"),
            TextNode(" ", TextType.TEXT),
            TextNode("it", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("ln", TextType.LINK, "v"),
            TextNode(" ", TextType.TEXT),
            TextNode("c", TextType.CODE),
            TextNode(" y", TextType.TEXT),
        ]
        self.assertEqual(got, want)

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


