import re
from enum import Enum

from htmlnode import *
from inline_md import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in md_blocks:
        html_nodes.append(md_block_to_html_block(block))

    return ParentNode("div", html_nodes)


def md_block_to_html_block(block):
    # get the block type
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING:
        return heading_blocks(block)
    if block_type == BlockType.UL:
        return ulist_blocks(block)
    if block_type == BlockType.OL:
        return olist_blocks(block)
    if block_type == BlockType.QUOTE:
        return blockquote_blocks(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_blocks(block)
    if block_type == BlockType.CODE:
        return code_blocks(block)


def heading_blocks(block):
    match = re.match(r"^(#+)\s", block)
    if match:
        heading_text = re.sub(r"^#+\s*", "", block).replace("\n", " ")
        hash_count = len(match.group(1))
        leafnodes = text_to_html_nodes(heading_text)

        return ParentNode(f"h{hash_count}", leafnodes)


def paragraph_blocks(block):
    text = block.strip().replace("\n", " ")
    leafnodes = text_to_html_nodes(text)

    return ParentNode("p", leafnodes)


def blockquote_blocks(block):
    text = re.sub(r"^>\s", "", block).strip().replace("\n", " ")
    leafnodes = text_to_html_nodes(text)

    return ParentNode("blockquote", leafnodes)


def olist_blocks(block):
    text = re.sub(r"^\d+\.\s", "", block, flags=re.MULTILINE)
    list_items = text.strip().split("\n")
    list_nodes = []
    for item in list_items:
        leafnodes = text_to_html_nodes(item)
        list_nodes.append(ParentNode("li", leafnodes))

    return ParentNode("ol", list_nodes)


def ulist_blocks(block):
    text = re.sub(r"^-\s", "", block, flags=re.MULTILINE)
    list_items = text.strip().split("\n")
    list_nodes = []
    for item in list_items:
        leafnodes = text_to_html_nodes(item)
        list_nodes.append(ParentNode("li", leafnodes))

    return ParentNode("ul", list_nodes)


def code_blocks(block):
    text = re.sub(r"^`{3}|`{3}$", "", block).lstrip()
    return ParentNode("pre", [LeafNode("code", text)])


def text_to_html_nodes(text):
    textnodes = text_to_textnodes(text)
    html_nodes = []
    for textnode in textnodes:
        html_node = text_node_to_html_node(textnode)
        html_nodes.append(html_node)
    return html_nodes


def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block != ""]
    return blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6}\s.+", block):
        return BlockType.HEADING
    elif re.match(r"^`{3}|`{3}$", block):
        return BlockType.CODE
    elif re.match(r"^>\s.*", block):
        return BlockType.QUOTE
    elif re.match(r"^(-\s.*\n)+", block):
        return BlockType.UL
    elif re.match(r"^(\d+\.\s.*\n)+", block):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH
