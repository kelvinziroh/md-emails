import pprint
import sys
from pathlib import Path

from googleapiclient.discovery import build

import drafts
import recipients
import src


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    creds = drafts.get_creds(SCOPES)
    service = build("gmail", "v1", credentials=creds)
    content = Path("content")
    template = Path("templates/template.html")

    # Handle drafts
    if len(sys.argv) < 2 or "--list" in sys.argv or "-l" in sys.argv:
        lst(service)

    if "--create" in sys.argv or "-c" in sys.argv:
        create(service, content, template)

    if "--edit" in sys.argv or "-e" in sys.argv:
        edit(service, content, template)

    if "--del" in sys.argv or "-D" in sys.argv:
        delete(service)

    if "--send" in sys.argv or "-s" in sys.argv:
        send(service)

    # Peek recipient data
    if "--rd-peek" in sys.argv:
        r_file_path = recipients.get_file_path()
        r_data = recipients.read_data(r_file_path)
        while True:
            view = int(
                input("\nSelect one:\n1. Variables\n2. Records\n[e.g. 1 or 2]->")
            )
            if view == 1:
                print("\nVariables")
                recipients.peek_vars(r_data)
                break
            if view == 2:
                print("\nRecords")
                recipients.peek_data(r_data, False)
                break


# Drafts
def lst(service):
    drafts_ = drafts.list_drafts(service)

    if drafts_:
        print_list(drafts_)
        print(f"Total no. of drafts: {len(drafts_)}")


def print_list(items):
    for item in items:
        pprint.pprint(item, sort_dicts=False)
        print("\n")


def create(service, content, template):
    # recipients = recipients.get_recipients(cc=True, bcc=True)
    recipients_ = recipients.get_recipients()
    html = parse_md(content, template)
    # drafts.create_draft(service, recipients, html, None)
    drafts.create_draft(service, recipients_, html, None)


def edit(service, content, template):
    id = input("Enter draft ID: ").strip()
    # recipients_ = recipients.get_recipients(cc=True, bcc=True)
    recipients_ = recipients.get_recipients()
    html = parse_md(content, template)
    # drafts.update_draft(service, id, recipients, html, None)
    drafts.update_draft(service, id, recipients_, html, None)


def parse_md(content, template):
    if content.exists():
        print("\nMessage files")
        for md_file in content.iterdir():
            print(f"* {md_file}")
        md_doc = input("\nEnter message file: ").strip()
        html = src.generate_page(md_doc, template)
        return html


def delete(service):
    id = input("Enter draft ID: ").strip()
    confirmation = input(f"Confirm deletion of draft ID {id}: [Y/n] ")
    if confirmation.lower() == "y":
        drafts.delete_draft(service, id)
    else:
        print(f"Deletion of draft ID {id} cancelled successfully")


def send(service):
    id = input("Enter draft ID: ").strip()
    drafts.send_draft(service, id)


if __name__ == "__main__":
    main()
