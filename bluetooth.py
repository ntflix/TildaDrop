from typing import AsyncGenerator
import aioble
import bluetooth

_ADV_INTERVAL_US = 250000

_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
_GENERIC_THERMOMETER = aioble.const(768)


async def advertise():
    print("Advertising")

    temp_service = aioble.Service(_ENV_SENSE_UUID)

    temp_char = aioble.Characteristic(
        temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
    )

    aioble.register_services(temp_service)

    while True:
        connection = await aioble.advertise(
            _ADV_INTERVAL_US,
            name="Tildagon",
            services=[_ENV_SENSE_UUID],
            appearance=_GENERIC_THERMOMETER,
            manufacturer=(0xABCD, b"1234"),
        )

        print("Connected to", connection.device)


async def scan():
    print("Scanning")
    async with aioble.scan(duration_ms=5000) as scanner:
        async for result in scanner:
            print(result, result.name(), result.rssi, result.services())
            yield result
