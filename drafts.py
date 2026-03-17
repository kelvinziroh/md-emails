import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


def list_drafts(service):
    try:
        drafts_obj = service.users().drafts().list(userId="me").execute()
        drafts = drafts_obj["drafts"]
        # service.users().messages.get(userId="me", format="metadata")
    except HttpError as err:
        print(f"An error occured: {err}")
        drafts = None
    return drafts


def create_draft(service, content):
    try:
        message = create_message(content)
        draft = service.users().drafts().create(userId="me", body=message).execute()

        print(f"Draft id: {draft['id']}\nDraft message: {draft['message']}")
    except HttpError as err:
        print(f"An error occured: {err}")
        draft = None

    return draft


def create_message(content):
    message = EmailMessage()
    message.set_content(content)

    message["To"] = "zirodev8687+person1@gmail.com"
    message["From"] = "zirodev8687@gmail.com"
    message["Subject"] = "Automated draft"

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
