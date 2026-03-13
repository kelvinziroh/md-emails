from googleapiclient.discovery import build

import drafts


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
    creds = drafts.get_creds(SCOPES)
    service = build("gmail", "v1", credentials=creds)
    # create_draft(service)
    for i, draft in enumerate(drafts.list_drafts(service)):
        print(f"*{i + 1}->{draft}")


if __name__ == "__main__":
    main()
