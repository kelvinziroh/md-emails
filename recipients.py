import json
import sys
from pathlib import Path

import pandas as pd


def get_recipients():
    data_import = None

    manual = prompt_entry_type()

    if not manual:
        data_import = load_data()

    return {
        "primary": collect_group("Primary", manual, data_import),
        "cc": collect_group("Cc", manual, data_import),
        "bcc": collect_group("Bcc", manual, data_import),
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


def prompt_filter(data):
    email_var = filter_var = filter_val = None
    peek_vars(data)
    email_var = input("\nSelect an [email address] variable: ").strip()
    if not email_var:
        return email_var, filter_var, filter_val
    filter_var = input("\nSelect a [filter] variable: ").strip()
    filter_values = list(data[filter_var].unique())
    print(f"Unique values in [{filter_var}]:")
    for val in filter_values:
        print(val)
    filter_val = input("\nSelect a [filter] value: ").strip()
    return email_var, filter_var, filter_val


def collect_group(label, manual, data_import):
    print(f"\n[{label}] recipients")

    if manual:
        return prompt_manual_emails()
    else:
        email_var, filter_var, filter_val = prompt_filter(data_import)
        return extract_emails(data_import, email_var, filter_var, filter_val)


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


def extract_emails(data_import, email_var, filter_var, filter_val):
    emails = []
    if email_var:
        # filter dataframe for inteded category
        filtered_data = data_import[data_import[filter_var] == filter_val]
        emails = list(filtered_data[email_var])
    return emails


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
