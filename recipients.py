import json
import sys
from pathlib import Path


def get_recipients():
    manual = prompt_entry_type()

    data_import = None
    email_var = None

    if not manual:
        data_import = load_data()
        email_var = prompt_email_field(data_import)

    return {
        "primary": collect_group("Primary", manual, data_import, email_var),
        "cc": collect_group("cc", manual, data_import, email_var),
        "bcc": collect_group("bcc", manual, data_import, email_var),
    }


# input layer
def prompt_entry_type():
    while True:
        try:
            choice = int(input("1. Manual entry\n2. Data entry\n-> ").strip())
            if choice in (1, 2):
                return choice == 1
        except ValueError:
            pass


def prompt_email_field(data):
    peek_vars(data)
    return input("Select an [address] variable: ").strip()


def collect_group(label, manual, data_import, email_var):
    print(f"\n[{label}] recipients")

    if manual:
        return prompt_manual_emails()
    else:
        return extract_emails(data_import, email_var)


# data layer
def load_data():
    file_path = get_file_path()
    return read_data(file_path)


def prompt_manual_emails():
    emails = []
    while True:
        address = input("Enter email address: ").strip()
        if not address:
            break
        emails.append(address)
    return emails


def extract_emails(data_import, email_var):
    return [record[email_var] for record in data_import]


def peek_data(data):
    print("\nRecords")
    # full output
    if len(data) <= 10:
        for record in data:
            print(record["email_address"])
    # shortened output
    else:
        for record in data[:5]:
            print(record["email_address"])
        # vertical ellipsis
        for i in range(3):
            print(".")
        for record in data[-5:]:
            print(record["email_address"])

    print(f"\n{len(data)} total recipients")


def peek_vars(data):
    print("\nVariables")
    for key in data[0].keys():
        print(key)
    print(f"\n{len(data[0].keys())} total variables")


def read_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    return data


def get_file_path():
    recipients = Path("data/recipients")
    print("recipient files:")
    for fname in recipients.iterdir():
        print(fname)
    while True:
        file_name = input("\nEnter file name: ")
        file_path = Path(f"data/recipients/{file_name}")

        if file_path.exists():
            break

    return f"{file_path}"
