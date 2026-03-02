import unittest

from block import (
    BlockType,
    block_to_block_type,
    check_for_ordered,
    check_for_quote,
    check_for_unordered,
)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> one\n> two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "just a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestCheckForQuote(unittest.TestCase):
    def test_all_lines_quoted(self):
        block = "> a\n> b\n> c"
        self.assertTrue(check_for_quote(block))

    def test_mixed_lines_not_quote(self):
        block = "> a\nb"
        self.assertFalse(check_for_quote(block))


class TestCheckForUnordered(unittest.TestCase):
    def test_all_lines_unordered(self):
        block = "- a\n- b\n- c"
        self.assertTrue(check_for_unordered(block))

    def test_mixed_lines_not_unordered(self):
        block = "- a\nb"
        self.assertFalse(check_for_unordered(block))


class TestCheckForOrdered(unittest.TestCase):
    def test_sequential_ordered(self):
        block = "1. a\n2. b\n3. c"
        self.assertTrue(check_for_ordered(block))

    def test_non_sequential_not_ordered(self):
        block = "1. a\n3. b"
        self.assertFalse(check_for_ordered(block))

    def test_missing_dot_not_ordered(self):
        block = "1 a\n2 b"
        self.assertFalse(check_for_ordered(block))


if __name__ == "__main__":
    unittest.main()
