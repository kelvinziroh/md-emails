import pprint
import sys

from googleapiclient.discovery import build

import drafts


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    creds = drafts.get_creds(SCOPES)
    service = build("gmail", "v1", credentials=creds)

    # handle draft listing case (default case)
    if len(sys.argv) < 2 or "--list" in sys.argv or "-l" in sys.argv:
        drafts_ = drafts.list_drafts(service)

        if drafts_:
            for draft in drafts_:
                pprint.pprint(draft, sort_dicts=False)
                print("\n")

            print(f"Total no. of drafts: {len(drafts_)}")

    # handle creation case
    if "--create" in sys.argv or "-c" in sys.argv:
        drafts.create_draft(service)

    # handle update case
    if "--edit" in sys.argv or "-e" in sys.argv:
        id = input("Enter draft ID: ").strip()
        drafts.update_draft(service, id)


if __name__ == "__main__":
    main()
