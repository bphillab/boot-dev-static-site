from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5

def block_to_block_type(block):
    if re.match(r"^#{,6}\s", block):
        return BlockType.HEADING
    elif check_for_code(block):
        return BlockType.CODE
    elif check_for_quote(block):
        return BlockType.QUOTE
    elif check_for_unordered(block):
        return BlockType.UNORDERED_LIST
    elif check_for_ordered(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def check_for_quote(block):
    splt = block.split("\n")
    for i in splt:
        if not i.startswith(">"):
            return False
    return True

def check_for_unordered(block):
    splt = block.split("\n")
    for i in splt:
        if not i.startswith("-"):
            return False
    return True

def check_for_ordered(block):
    splt = block.split("\n")
    indx = 1
    for i in splt:
        if not i.startswith(f"{indx}."):
            return False
        indx += 1
    return True

def check_for_code(block):
    splt = block.split("\n")
    return splt[0] == "```" and splt[-1][-3:] == "```"