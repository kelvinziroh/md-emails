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

    draft_items = []
    if draft_objs:
        for obj in draft_objs:
            draft_item = {}
            draft_item["draft_id"] = obj["id"]
            draft_item["message_id"] = obj["message"]["id"]
            draft_item["thread_id"] = obj["message"]["threadId"]
            headers = (
                service.users()
                .messages()
                .get(userId="me", id=draft_item["message_id"], format="metadata")
                .execute()
            )["payload"]["headers"]

            header_filters = ["Date", "Subject", "To", "From"]
            filtered_headers = [
                header for header in headers if header["name"] in header_filters
            ]

            draft_item["date"] = [
                header["value"] for header in headers if header["name"] == "Date"
            ][0]
            draft_item["subject"] = [
                header["value"] for header in headers if header["name"] == "Subject"
            ][0]
            draft_item["to"] = [
                header["value"] for header in headers if header["name"] == "To"
            ][0]
            draft_item["from"] = [
                header["value"] for header in headers if header["name"] == "From"
            ][0]

            draft_items.append(draft_item)

    print(draft_items)
    # print(pprint.pformat(draft, indent=4, sort_dicts=True))


if __name__ == "__main__":
    main()
