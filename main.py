import pprint

from googleapiclient.discovery import build

import drafts


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    # "https://www.googleapis.com/auth/gmail.modify"
    creds = drafts.get_creds(SCOPES)
    service = build("gmail", "v1", credentials=creds)
    # create_draft(service)
    # for i, draft in enumerate(drafts.list_drafts(service)):
    #     print(f"*{i + 1}->{draft}")
    draft_objs = drafts.list_drafts(service)

    if draft_objs:
        for obj in draft_objs:
            draft_id = obj["id"]
            msg_id = obj["message"]["id"]
            thread_id = obj["message"]["threadId"]
            headers = (
                service.users()
                .messages()
                .get(userId="me", id=msg_id, format="metadata")
                .execute()
            )["payload"]["headers"]

            header_filters = ["Date", "Subject", "To", "From"]
            filtered_headers = [
                header for header in headers if header["name"] in header_filters
            ]

            print(
                f"Draft id: {draft_id}\nMessage id: {msg_id}\nThread id: {thread_id}\n\nHeaders:\n"
            )
            for header in filtered_headers:
                print(header)
            print("\n")

    # print(pprint.pformat(draft, indent=4, sort_dicts=True))


if __name__ == "__main__":
    main()
