import json
import sys
from pathlib import Path

import pandas as pd


def get_recipients():
    manual = prompt_entry_type()

    data_import = None
    email_var = None

    if not manual:
        data_import = load_data()
        email_var = prompt_email_field(data_import)

    return {
        "primary": collect_group("Primary", manual, data_import, email_var),
        "cc": collect_group("Cc", manual, data_import, email_var),
        "bcc": collect_group("Bcc", manual, data_import, email_var),
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
    if data.shape[0] <= 10:
        print(data)
    else:
        print(data.head(10))

    print(f"\n{data.shape[1]} total variables")
    print(f"{data.shape[0]} total records")


def peek_vars(data):
    vars = list(data.columns)
    print("\n   Variable\t\tUnique values count")
    for i, var in enumerate(vars):
        unique_count = len(data[var].unique())
        print(f"{i + 1}. {var}\t\t{unique_count}")
    print(f"\n{data.shape[1]} total variables")
    print(f"{data.shape[0]} total records")


def read_data(file_path):
    data = pd.read_json(file_path)
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
