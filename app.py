import app
from events.input import Buttons, BUTTON_TYPES
from .comms import Comms

import asyncio

PEER_MAC = "64e833720028"


class TildaDropApp(app.App):
    text: str
    text2: str
    comms: Comms
    color: int = 0
    textColor: int = 1

    def __init__(self):
        self.button_states = Buttons(self)
        self.text = "A to send"
        self.text2 = "D to receive"
        self.comms = Comms()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.text = "Sending…"
            self.text2 = ""
            send_task = self.comms.send(
                mac=PEER_MAC,
                message="Hi",
            )
            asyncio.create_task(send_task)
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.text = "Receiving…"
            self.text2 = ""
            receive_task = self.comms.receive(self.on_receive)
            asyncio.create_task(receive_task)
        elif self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.text = "MAC"
            self.text2 = self.comms.get_mac()
        elif self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()

    def draw(self, ctx):
        # ctx.save()

        ctx.font_size = 36
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE

        ctx.rgb(
            self.color,
            self.color,
            self.color,
        ).rectangle(-120, -120, 240, 240).fill()

        ctx.rgb(
            self.textColor,
            self.textColor,
            self.textColor,
        ).move_to(
            0, -26
        ).text(self.text)

        ctx.rgb(
            self.textColor,
            self.textColor,
            self.textColor,
        ).move_to(
            0, 26
        ).text(self.text2)

        # ctx.restore()

    async def on_receive(self, host: bytes, msg: str):
        # print(f"Received message")
        self.text = "Received!"
        self.text2 = msg
        self.color = 1
        self.textColor = 0
        # self.text2 =


__app_export__ = TildaDropApp
