import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE_TEXT)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        txts = node.text.split(delimiter)
        if len(txts) % 2 == 0:
            raise ValueError("Invalid markdown")

        # txts = node.text.split(delimiter)

        for i in range(len(txts)):
            if txts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(txts[i], TextType.PLAIN_TEXT))
            else:
                split_nodes.append(TextNode(txts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        original_txt = node.text
        img_txts = extract_markdown_images(original_txt)

        if not img_txts:
            new_nodes.append(node)
            continue

        for i in range(len(img_txts)):
            img_alt, img_link = img_txts[i][0], img_txts[i][1]
            delimiter = f"![{img_alt}]({img_link})"
            split_txts = original_txt.split(delimiter, 1)

            if len(split_txts) != 2:
                raise ValueError("Invalid markdown")

            if split_txts[0] != "":
                new_nodes.append(TextNode(split_txts[0], TextType.PLAIN_TEXT))

            original_txt = split_txts[-1]
            new_nodes.append(TextNode(img_alt, TextType.IMAGE_TEXT, img_link))

        if original_txt:
            new_nodes.append(TextNode(original_txt, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        original_txt = node.text
        link_txts = extract_markdown_links(original_txt)

        if not link_txts:
            new_nodes.append(node)
            continue

        for i in range(len(link_txts)):
            a_txt, a_link = link_txts[i][0], link_txts[i][1]
            delimiter = f"[{a_txt}]({a_link})"
            split_txts = original_txt.split(delimiter, 1)

            if len(split_txts) != 2:
                raise ValueError("Invalid markdown")

            if split_txts[0] != "":
                new_nodes.append(TextNode(split_txts[0], TextType.PLAIN_TEXT))

            original_txt = split_txts[-1]
            new_nodes.append(TextNode(a_txt, TextType.LINK_TEXT, a_link))

        if original_txt:
            new_nodes.append(TextNode(original_txt, TextType.PLAIN_TEXT))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)"
    return re.findall(pattern, text)
