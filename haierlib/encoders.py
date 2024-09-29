import re


def encode_mac(mac_address: str) -> str:
    mac_address = re.sub(
        pattern=r"[^a-f\d]",
        repl="",
        string=mac_address,
        flags=re.IGNORECASE,
    ).lower()
    result = [hex(ord(char))[2:] for char in mac_address]
    result.extend(["00", "00", "00", "00"])
    return " ".join(result) + " "
