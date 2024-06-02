import espnow
import time


def broadcast_forever():
    """
    Sends messages to all ESP-Now devices
    """
    bcast_address = b"\xff" * 6

    esp_device = espnow.ESPNow()
    esp_device.active(True)
    esp_device.add_peer(bcast_address)
    esp_device.irq(receive_irq)

    i = 0
    print("Starting broadcast loop...")
    while True:
        msg = f"Hear ye, hear ye! Broadcast #{i}"
        esp_device.send(bcast_address, msg, True)

        i += 1
        time.sleep(0.5)


def receive_irq(esp_device):
    """
    Callback method when a message is received. This prints the sender
    and message to stdout.
    """
    print(f"Got Message: {esp_device.irecv(0)}")
