import json
import sys
from pathlib import Path


def get_recipients():
    recipients = {}

    print("[Primary] recipients")
    recipients["primary"] = get_addresses()

    print("\n[Cc] recipients")
    recipients["cc"] = get_addresses()

    print("\n[Bcc] recipients")
    recipients["bcc"] = get_addresses()

    return recipients


def get_addresses():
    addresses = []

    while True:
        address = input("Enter email address: ").strip()
        if address == "":
            break
        addresses.append(address)

    return addresses


def peek_data(data, all):
    if len(data) <= 10 or all:
        # full output
        for record in data:
            print(record["email_address"])
    else:
        # shortened output
        for record in data[:5]:
            print(record["email_address"])

        # vertical ellipsis
        for i in range(3):
            print(".")

        for record in data[-5:]:
            print(record["email_address"])

    print(f"\n{len(data)} total recipients")


def peek_vars(data):
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
