import re


def encode_mac(mac_address: str) -> str:
    """
    Converts a MAC address string to a formatted string with spaces.

    Args:
        mac_address (str): The input MAC address string.

    Returns:
        str: The formatted MAC address string with spaces.
    """

    result = []
    mac_address = re.sub(
        pattern=r"[^a-f\d]", repl="", string=mac_address, flags=re.IGNORECASE
    ).lower()
    result = [hex(ord(char))[2:] for char in mac_address]
    # for char in mac_address:
    #     result += hex(ord(char))
    result.extend(["00", "00", "00", "00"])
    return " ".join(result) + " "
