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
