import pprint
import sys
from pathlib import Path

from googleapiclient.discovery import build

import drafts
import src
from recipients import get_recipients


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    creds = drafts.get_creds(SCOPES)
    service = build("gmail", "v1", credentials=creds)
    content = Path("content")
    template = Path("templates/template.html")

    # list drafts (default)
    if len(sys.argv) < 2 or "--list" in sys.argv or "-l" in sys.argv:
        drafts_ = drafts.list_drafts(service)

        if drafts_:
            print_list(drafts_)
            print(f"Total no. of drafts: {len(drafts_)}")

    # create draft
    if "--create" in sys.argv or "-c" in sys.argv:
        recipients = get_recipients(cc=True, bcc=True)
        if content.exists():
            print("\nMessage files")
            for md_file in content.iterdir():
                print(f"* {md_file}")
            md_doc = input("\nEnter message file: ").strip()
            html = src.generate_page(md_doc, template)
            drafts.create_draft(service, recipients, html, None)

    # update draft
    # if "--edit" in sys.argv or "-e" in sys.argv:
    #     id = input("Enter draft ID: ").strip()
    #     recipients = get_recipients(cc=True, bcc=True)
    #     if md_doc.exists():
    #         html = src.generate_page(md_doc, template)
    #         drafts.update_draft(service, id, recipients, html, None)

    # delete draft
    if "--del" in sys.argv or "-D" in sys.argv:
        id = input("Enter draft ID: ").strip()
        confirmation = input(f"Confirm deletion of draft ID {id}: [Y/n] ")
        if confirmation.lower() == "y":
            drafts.delete_draft(service, id)
        else:
            print(f"Deletion of draft ID {id} cancelled successfully")

    # send draft
    if "--send" in sys.argv or "-s" in sys.argv:
        id = input("Enter draft ID: ").strip()
        drafts.send_draft(service, id)


def print_list(items):
    for item in items:
        pprint.pprint(item, sort_dicts=False)
        print("\n")


if __name__ == "__main__":
    main()
