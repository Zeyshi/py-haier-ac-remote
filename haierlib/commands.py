import binascii
from enum import Enum, StrEnum
from typing import Callable

from haierlib import ac_types


class Commands(StrEnum):
    Init = "init"
    Hello = "hello"
    On = "on"
    Off = "off"
    Ping = "ping"
    SetState = "set_state"


def set_state(state: ac_types.State) -> str:
    def checksum(s: str) -> str:
        checksum = (
            sum(
                int(c, 16) * (i % 2 if i % 2 else 16)
                for i, c in enumerate([c for c in s if c in "0123456789abcdef"])
            )
            - 2 * 255
        )
        return hex(checksum)[2:]

    res = "ff ff 22 00 00 00 00 00 00 01 4d 5f 00 00 00 00 00 00 00 00 00 00 "
    res += f"00 0{state._mode.value} "
    res += f"00 0{state._fan_speed.value} "
    res += f"00 0{state._limits.value} "
    res += f"00 0{'9' if state._power else '1'} "
    res += f"00 0{'1' if state._health else '0'} "
    res += f"00 00 00 0{hex(state._target_temp - 16)[2:]} "
    res += checksum(res)
    return res


class RawCommands(Enum):
    request = "00 00 27 14 00 00 00 00 "
    response = "00 00 27 15 00 00 00 00 "
    zero16 = "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
    hello = "ff ff 0a 00 00 00 00 00 00 01 4d 01 59 "
    on = "ff ff 0a 00 00 00 00 00 00 01 4d 02 5a "
    off = "ff ff 0a 00 00 00 00 00 00 01 4d 03 5b "
    init = "ff ff 08 00 00 00 00 00 00 73 7b "
    set_state: Callable = set_state


def order_byte(n: int) -> str:
    hex_value = binascii.hexlify(bytes([n % 256])).decode("ascii").ljust(2, "0")
    return f"00 00 00 {hex_value} "
