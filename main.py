import pprint
import sys

from googleapiclient.discovery import build

import drafts


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    creds = drafts.get_creds(SCOPES)
    service = build("gmail", "v1", credentials=creds)

    # list drafts (default)
    if len(sys.argv) < 2 or "--list" in sys.argv or "-l" in sys.argv:
        drafts_ = drafts.list_drafts(service)

        if drafts_:
            print_list(drafts_)
            print(f"Total no. of drafts: {len(drafts_)}")

    # create draft
    if "--create" in sys.argv or "-c" in sys.argv:
        drafts.create_draft(service)

    # update draft
    if "--edit" in sys.argv or "-e" in sys.argv:
        id = input("Enter draft ID: ").strip()
        drafts.update_draft(service, id)

    # delete draft
    if "--del" in sys.argv or "-D" in sys.argv:
        id = input("Enter draft ID: ").strip()
        confirmation = input(f"Confirm deletion of draft ID {id}: [Y/n] ")
        if confirmation.lower() == "y":
            drafts.delete_draft(service, id)
        else:
            print(f"Deletion of draft ID {id} cancelled successfully")


def print_list(items):
    for item in items:
        pprint.pprint(item, sort_dicts=False)
        print("\n")


if __name__ == "__main__":
    main()
