import pprint

from googleapiclient.discovery import build

import drafts


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    creds = drafts.get_creds(SCOPES)
    service = build("gmail", "v1", credentials=creds)
    drafts_ = drafts.list_drafts(service)

    print(drafts_)


if __name__ == "__main__":
    main()
