import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


def delete_draft(service, draft_id):
    try:
        service.users().drafts().delete(userId="me", id=draft_id).execute()
        print(f"Draft '{draft_id}' deleted successfully.")
    except HttpError as err:
        print(f"An error occured: {err}")


def update_draft(service, draft_id):
    try:
        message = create_message()
        draft = (
            service.users()
            .drafts()
            .update(userId="me", id=draft_id, body=message)
            .execute()
        )
        print(f"Draft id: {draft['id']}\nDraft message: {draft['message']}")
    except HttpError as err:
        print(f"An error occured: {err}")
        draft = None

    return draft


def list_drafts(service):
    try:
        drafts_obj = service.users().drafts().list(userId="me").execute()["drafts"]

        drafts = []
        for obj in drafts_obj:
            headers = filter_headers(service, obj["message"]["id"])
            draft = create_ddict(obj, headers)
            drafts.append(draft)
    except HttpError as err:
        print(f"An error occured: {err}")
        drafts = None

    return drafts


def create_ddict(obj, headers):
    ddict = {}
    ddict["draft_id"] = obj["id"]
    ddict["message_id"] = obj["message"]["id"]
    ddict["thread_id"] = obj["message"]["threadId"]
    ddict["date"] = get_header_value(headers, "Date")
    ddict["subject"] = get_header_value(headers, "Subject")
    ddict["to"] = get_header_value(headers, "To")
    ddict["from"] = get_header_value(headers, "From")
    return ddict


def get_header_value(headers, header_name):
    return [header["value"] for header in headers if header["name"] == header_name][0]


def filter_headers(service, message_id):
    headers = (
        service.users()
        .messages()
        .get(userId="me", id=message_id, format="metadata")
        .execute()["payload"]["headers"]
    )
    filters = ["Date", "Subject", "To", "From"]
    return [header for header in headers if header["name"] in filters]


def create_draft(service):
    try:
        message = create_message()
        draft = service.users().drafts().create(userId="me", body=message).execute()

        print(f"Draft id: {draft['id']}\nDraft message: {draft['message']}")
    except HttpError as err:
        print(f"An error occured: {err}")
        draft = None

    return draft


def create_message():
    message = EmailMessage()
    message["From"] = "zirodev8687@gmail.com"
    message["To"] = input("Recipient: ").strip()
    message["Subject"] = input("Subject: ").strip()
    message.set_content(input("Enter message:\n>").strip())

    # encode message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"message": {"raw": encoded_message}}


def get_creds(scopes):
    creds = None

    # Use availabe valid credentials if created earlier
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    # log user in if there are no valid credentials available
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Run the complete authorization flow if first time
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds
