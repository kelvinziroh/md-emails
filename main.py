import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
    creds = get_creds(SCOPES)
    create_draft(creds)


def create_draft(creds):
    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()
        message.set_content("This is an automated draft email")

        message["To"] = "zirodev8687+person1@gmail.com"
        message["From"] = "zirodev8687@gmail.com"
        message["Subject"] = "Automated draft"

        # encode message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}
        draft = (
            service.users().drafts().create(userId="me", body=create_message).execute()
        )

        print(f"Draft id: {draft['id']}\nDraft message: {draft['message']}")
    except HttpError as err:
        print(f"An error occured: {err}")
        draft = None

    return draft


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


if __name__ == "__main__":
    main()
