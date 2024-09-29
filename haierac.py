from haierlib import ac_types, encoders, parsers
from haierlib.commands import Commands, RawCommands, order_byte
from typing import Optional
import socket
import binascii


class HaierAC:
    def __init__(
        self, ip: str, mac: str, port: int = 56800, timeout: int = 500
    ) -> None:
        self._ip = ip
        self._port = port
        self._mac = mac
        self._mac_encoded = encoders.encode_mac(mac)
        self._timeout = timeout
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock_is_connected = False
        self._seq = 0
        self._state = ac_types.State()

    def recv_loop(self) -> None:
        if not self._sock_is_connected:
            self._sock.connect((self._ip, self._port))
            self._sock_is_connected = True
        while True:
            recv_data = self._sock.recv(1000)
            if recv_data:
                print("-- Has Data --")
                print(parsers.parse_resp(recv_data, self._state))
                break

    def request(self, cmd: str, state: Optional[ac_types.State] = None) -> bytes:
        res = RawCommands.request.value
        res += RawCommands.zero16.value
        res += RawCommands.zero16.value
        res += self._mac_encoded
        res += RawCommands.zero16.value
        res += order_byte(self._seq)
        match cmd:
            case Commands.Hello:
                res += order_byte(len(RawCommands.hello.value.split(" ")) - 1)
                res += RawCommands.hello.value
            case Commands.Init:
                res += order_byte(len(RawCommands.init.value.split(" ")) - 1)
                res += RawCommands.init.value
            case Commands.On:
                res += order_byte(len(RawCommands.on.value.split(" ")) - 1)
                res += RawCommands.on.value
            case Commands.Off:
                res += order_byte(len(RawCommands.off.value.split(" ")) - 1)
                res += RawCommands.off.value
            case Commands.SetState:
                res += order_byte(
                    len(RawCommands.set_state(state).split(" ")) - 1
                )
                res += RawCommands.set_state(state)
        return bytes.fromhex(res)

    def ping(self) -> bytes:
        res = "00 00 5d f2 00 00 00 00 "
        res += f"00 00 00 {order_byte(self._seq)} 00 00 00 30 "
        res += RawCommands.zero16.value
        res += RawCommands.zero16.value
        res += self._mac_encoded
        res += "00 00 00 00"
        return bytes.fromhex(res)

    def send_hello(self) -> None:
        req = self.request(Commands.Hello)
        self._sock.sendall(req)
        self._seq += 1

    def send_init(self) -> None:
        req = self.request(Commands.Init)
        self._sock.sendall(req)
        self._seq += 1

    def send_on(self) -> None:
        req = self.request(Commands.On)
        self._sock.sendall(req)
        self._seq += 1

    def send_off(self) -> None:
        req = self.request(Commands.Off)
        self._sock.sendall(req)
        self._seq += 1

    def set_temp(self, temp: int) -> None:
        new_state = self._state
        new_state._target_temp = temp
        req = self.request(Commands.SetState, new_state)
        self._sock.sendall(req)
        self._seq += 1
