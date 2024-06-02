import app
from .bluetooth import advertise, scan
import asyncio

from events.input import Buttons, BUTTON_TYPES


class TildaDropApp(app.App):
    text: str
    text2: str

    def __init__(self):
        self.button_states = Buttons(self)
        self.text = "B to advertise"
        self.text2 = "E to scan"

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.text = "advertising"
            self.text2 = ""
            x = advertise()
            asyncio.run(x)
        elif self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.text = "scanning"
            self.text2 = ""
            x = scan()
            asyncio.run(x)
        elif self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()

    def draw(self, ctx):
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(0, 1, 0).move_to(-95, -12).text(self.text)
        ctx.rgb(0, 1, 0).move_to(-95, 12).text(self.text2)


__app_export__ = TildaDropApp
