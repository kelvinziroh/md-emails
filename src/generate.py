import os
from pathlib import Path

from .block_md import markdown_to_html_node


def generate_page(src_path, template_path):
    # print(f'* src:"{src_path}" temp:"{template_path}" -> dest:"{dest_path}"')

    # read src and template files
    with open(src_path, "r") as src_file:
        md = src_file.read()

    with open(template_path, "r") as temp_file:
        template = temp_file.read()

    # Fill template with html generated html content
    html_content = markdown_to_html_node(md).to_html()
    filled_template = template.replace("{{ Content }}", html_content)

    return filled_template
