from typing import Any, Callable, Coroutine
import ubinascii
import network
import espnow


class Comms:
    def __init__(self):
        # A WLAN interface must be active to send()/recv()
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(False)
        self.sta.active(True)
        self.sta.disconnect()  # Because ESP8266 auto-connects to last Access Point

        self.e = espnow.ESPNow()
        self.e.active(False)
        self.e.active(True)

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

    async def send(self, mac: str | bytes, message: str):
        if isinstance(mac, str):
            peer_mac = bytes.fromhex(mac)
        else:
            peer_mac = mac

        self.e.add_peer(peer_mac)  # Must add_peer() before send()
        self.e.send(peer_mac, message)
        self.e.send(peer_mac, b"end")
        print("Sent message")

    async def receive(
        self, on_receive: Callable[[bytes, str], Coroutine[Any, Any, None]]
    ):
        while True:
            host, msg = self.e.recv()
            if msg:  # msg == None if timeout in recv()
                # convert message to string
                msg_str = msg.decode()
                # print(host, msg_str)
                if msg == b"end":
                    break
                await on_receive(host, msg_str)
