from typing import Any, Callable, Coroutine
import ubinascii
import network
import espnow
from .wifi_reset import wifi_reset


class Comms:
    def __init__(self):
        # A WLAN interface must be active to send()/recv()
        self.sta = wifi_reset()  # Reset wifi to AP off, STA on and disconnected

        self.e = espnow.ESPNow()
        self.e.active(True)

    def reset(self) -> None:
        self.__init__()

    def get_mac(self) -> str:
        wlan_sta = network.WLAN(network.STA_IF)
        wlan_sta.active(True)

        wlan_mac = wlan_sta.config("mac")
        mac_str = ubinascii.hexlify(wlan_mac).decode()
        print(f"MAC address: {mac_str}")
        return mac_str

    async def advertise(self):
        print("Advertising")

    async def scan(self):
        print("Scanning")

    async def send(
        self,
        message: str,
        mac: str | bytes | None = None,  # Send to broadcast by default
    ):
        peer_mac: bytes = b""

        if mac is None:
            peer_mac = b"\xFF\xFF\xFF\xFF\xFF\xFF"
        else:
            if isinstance(mac, str):
                peer_mac = bytes.fromhex(mac)
            else:
                peer_mac = mac

        try:
            self.e.add_peer(peer_mac)  # Must add_peer() before send()
            print("Peer added")
        except OSError as e:
            if "ESP_ERR_ESPNOW_EXIST" in str(e):
                print("Peer already added")
            else:
                raise e

        print(f"Sending to {peer_mac}")
        try:
            self.e.send(peer_mac, message)
            self.e.send(peer_mac, b"end")
        except OSError as e:
            if "ETIMEDOUT" in str(e):
                print("Timeout")

        print("Sent message")

    async def receive(self, on_receive: Callable[[bytes, str], None]):
        while True:
            host, msg = self.e.recv()
            if msg:  # msg == None if timeout in recv()
                # convert message to string
                msg_str = msg.decode()
                # print(host, msg_str)
                if msg == b"end":
                    break
                on_receive(host, msg_str)
