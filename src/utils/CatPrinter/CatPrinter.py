import sys
import asyncio
from bleak import BleakClient
from PyQt6.QtCore import QTimer
from src.utils.CatPrinter.crc8table import format_command
from src.utils.PubSub import pubsub
from src.utils.CatPrinter.OrderToText import getImage_textBytes

# minimal mxw01 printing sequence derived from https://github.com/eerimoq/moblin/tree/main/Moblin/Integrations/CatPrinter

class CatPrinter(object) :
    def __init__(self):
        #hardcoded address for now :P
        self.printer_address = "FE16E45D-6E8A-039D-16C7-B668107E8F62" if sys.platform == "darwin" else "48:0F:57:2A:DD:09"  
        self.printer_characteristic = "0000ae01-0000-1000-8000-00805f9b34fb"
        self.notify_uuid = "0000ae02-0000-1000-8000-00805f9b34fb"
        self.data_characteristic = "0000ae03-0000-1000-8000-00805f9b34fb"
        self.printid = 0xa9
        self.client = None

        self.pendingConnection = False

        self.connectToClient_wrapper()
        pubsub.subscribe("printerBtn_clicked", self.connectToClient_wrapper)
    
    def connectToClient_wrapper(self, e = None) :
        if self.pendingConnection :
            print('its currently pending connection please wait!')
            return
        if self.client is not None and self.client.is_connected :
            print('printer is already connected!')
            return
        QTimer.singleShot(0, lambda: asyncio.create_task(self.connectClient())) # need qtimer singleshot to wait until app event loop has started

    async def print_sequence(self, myOrder = None) :
        if myOrder is not None :
            getImage_textBytes(myOrder)
        if not self.client.is_connected :
            print("not connected to printer!")
            return

        myImg_inBytes = getImage_textBytes(myOrder)
        try :
            await self.client.start_notify(self.notify_uuid, self.notification_handler)
            await self.print_request(myImg_inBytes)
            await self.write_chunk(myImg_inBytes)
            await self.client.stop_notify(self.notify_uuid) # stop notify after every print_seq
        except Exception as e :
            print("printing failed!", e)

        await asyncio.sleep(3)
        pubsub.publish("print_finished")
        print("end of sequence")


    async def connectClient(self) :
        self.pendingConnection = True
        retries = 5 
        self.client = BleakClient(self.printer_address, disconnected_callback=self.on_disconnect) 
        await self.client.disconnect()
        print("expected", self.client)
        print("cat trying to connect...")
        for attempts in range(retries) :
            try :
                await self.client.connect()
                print("client connected successfully")
                break
            except Exception as e:
                print("failed attempt", attempts + 1)
                await asyncio.sleep(3)

        if self.client.is_connected :
            self.client = self.client
            pubsub.publish("printer_connected", True)
            print("cat connected successfully!")
        else : 
            pubsub.publish("printer_connected", False)
            print("cat failed to connect...")
        self.pendingConnection = False

    
    def on_disconnect(self, e = None) :
        pubsub.publish("printer_connected", False)
        print("printer disconnected!", e)

    async def print_request(self, image_data = None) :
        if image_data is None :
            row_count = 90 # how long it would print (height).. default 90
        else :
            row_count = len(image_data) // 48 # because each row has 48 bytes

        payload = row_count.to_bytes(2, "little") + bytes.fromhex("3000")
        printReq_cmd = format_command(self.printid, payload)
        await self.client.write_gatt_char(self.printer_characteristic, printReq_cmd)
        print("print req complete")
        await asyncio.sleep(2)

    async def write_chunk(self, image_data = None) :
    
        if image_data is None : # default for testing
            myrow = b"\xff\xff\x00\x00" * 12 # each row contains 48 bytes
            myrow2 = b"\x00\x00\xff\xff" * 24
            image_data = (myrow + myrow2) * 45 
        
        chunk_size = 180 if sys.platform == "darwin" else 508 # mtu for os differs
        for i in range(0, len(image_data), chunk_size):
            await self.client.write_gatt_char(self.data_characteristic, image_data[i:i+chunk_size], response=False)
            await asyncio.sleep(0.1)
        await asyncio.sleep(5)

    async def notification_handler(self, sender, data):
        # print(data)
        print(f"Printer response: {data.hex()}")

    async def disconnect_catPrinter(self) :
        if self.client.is_connected :
           await self.client.disconnect()