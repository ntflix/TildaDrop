# from https://docs.micropython.org/en/latest/library/espnow.html#espnow-and-wifi-operation

import network, time


def wifi_reset():  # Reset wifi to AP_IF off, STA_IF on and disconnected
    sta = network.WLAN(network.STA_IF)
    sta.active(False)
    # ap = network.WLAN(network.AP_IF)
    # ap.active(False)
    sta.active(True)
    while not sta.active():
        time.sleep(0.1)
    sta.disconnect()  # For ESP8266, because it auto-connects to last Access Point
    while sta.isconnected():
        time.sleep(0.1)
    # return sta, ap
    return sta
