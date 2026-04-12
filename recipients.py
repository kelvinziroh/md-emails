import json
import sys
from pathlib import Path


def get_recipients(cc=False, bcc=False):
    recipients = {}

    print("[Primary] recipients")
    recipients["primary"] = get_addresses()

    if cc:
        print("\n[Cc] recipients")
        recipients["cc"] = get_addresses()
    if bcc:
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
