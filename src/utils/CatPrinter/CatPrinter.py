import asyncio
from bleak import BleakClient
from PyQt6.QtCore import QTimer
from src.utils.CatPrinter.crc8table import format_command
from src.utils.PubSub import pubsub

class CatPrinter(object) :
    def __init__(self):
        self.printer_address = "48:0F:57:2A:DD:09"
        self.printer_characteristic = "0000ae01-0000-1000-8000-00805f9b34fb"
        self.notify_uuid = "0000ae02-0000-1000-8000-00805f9b34fb"
        self.data_characteristic = "0000ae03-0000-1000-8000-00805f9b34fb"
        reset = 0xa0
        status = 0xa1
        drawBitmap = 0xa2
        drawingMode = 0xbe
        setEnergy = 0xaf
        setQuality = 0xa4
        deviceinfo = 0xa8
        self.printid = 0xa9
        version = 0xb1
        self.client = None
        self.connected = False
        QTimer.singleShot(0, lambda: asyncio.create_task(self.connectClient()))


    async def test_sequence(self) :
        print(self.client)
        if not self.client.is_connected :
            print("not connected to printer!")
            return
        await self.client.start_notify(self.notify_uuid, self.notification_handler)
        await self.print_request(self.client)
        await self.write_chunk(self.client)

        pubsub.publish("print_finished")
        print("end of sequence")

    async def connectClient(self) :
        retries = 5 
        self.client = BleakClient(self.printer_address) 
        await self.client.disconnect()
        print("expected", self.client)
        print("cat trying to connect...")
        for attempts in range(retries) :
            try :
                await self.client.connect()
                print("client connected successfully")
                break
            except Exception as e:
                print(e)
                print("failed attempt", attempts + 1)
                await asyncio.sleep(3)

        if self.client.is_connected :
            self.client = self.client
            self.connected = True
            print("cat connected successfully!")
        else : 
            print("cat failed to connect...")

    async def print_request(self,client, row_count = None) :
        if row_count is None :
            row_count = 90 # how long it would print.. default 90

        payload = row_count.to_bytes(2, "little") + bytes.fromhex("3000")
        printReq_cmd = format_command(self.printid, payload)
        await client.write_gatt_char(self.printer_characteristic, printReq_cmd)
        print("print req complete")
        await asyncio.sleep(2)

    async def write_chunk(self, client, image_data = None) :
    
        if image_data is None : 
            myrow = b"\xff\xff\x00\x00" * 12 
            myrow2 = b"\x00\x00\xff\xff" * 24
            image_data = (myrow + myrow2) * 45 
        chunk_size = 508
        for i in range(0, len(image_data), chunk_size):
            await client.write_gatt_char(self.data_characteristic, image_data[i:i+chunk_size])
            await asyncio.sleep(0.1)
        await asyncio.sleep(5)

    async def notification_handler(self, sender, data):
        # print(data)
        print(f"Printer response: {data.hex()}")