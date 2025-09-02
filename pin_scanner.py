import asyncio
import time
import datetime
import aiohttp
import concurrent.futures
import math

from rich import print
from rich.pretty import Pretty
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich.live import Live
from rich import box
from rich.text import Text

THRESHOLD = 5 # minutes since game started

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def scan_pin(pin):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1024)) as session:
            await asyncio.sleep(0)
            data = await fetch(session, f"https://kahoot.it/reserve/session/{pin}/")
            if time.time() * 1000 - THRESHOLD * 60000 < data["startTime"]:
                return (pin, data["startTime"])
    except:
        return None

def scan(pin):
    return asyncio.run(scan_pin(pin))

def setup():
    start_pin = 0
    end_pin = 20000
    while True:
        try:
            start_pin = int(input("Enter the pin to start scanning from: "))
            if start_pin < 0 or start_pin >= 1000000:
                raise ValueError
            break
        except ValueError:
            print("Please try again - start pin must be a positive integer less than 1,000,000.")
    
    while True:
        try:
            end_pin = int(input("Enter the pin to scan up to: "))
            if end_pin < start_pin or end_pin > 1000000:
                raise ValueError
            break
        except ValueError:
            print("Please try again - end pin must be a positive integer greater or equal to the start pin, and less than 1,000,000.")
    
    print(f"\nScanning between {start_pin} - {end_pin}")

    return start_pin, end_pin

def generate_table(pins, progress, total) -> Table:
    table = Table(show_header=True, title=f"Kahoot Games • {progress/total * 100 :.2f}%", header_style="italic", box=box.HEAVY_EDGE)
    table.add_column("Game Pin")
    table.add_column("Duration")
    table.add_column("Start Time")

    pins.sort(key=lambda x: -x[1])
    for pin in pins:
        table.add_row(Pretty(pin[0]), 
                      str(datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))),
                      str((datetime.datetime.now() - datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))).strftime("%H:%M:%S")))
    return table

if __name__ == "__main__":
    panel = Panel(Text("Welcome to the Kahoot Pin Scanner", style="italic"), expand=False)
    print(panel)

    print(Rule())

    print("Please enter the range of pins to scan (min: 0 - max: 1,000,000)\n")
    start_pin, end_pin = setup()

    print(Rule())

    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as e:
        futures = {e.submit(scan, pin): pin for pin in range(start_pin, end_pin)}

        pins = []
        progress = 0
        with Live(generate_table(pins, progress, end_pin - start_pin), refresh_per_second=1) as live:
            for future in concurrent.futures.as_completed(futures):
                live.update(generate_table(pins, progress, end_pin - start_pin))
                try:
                    progress += 1
                    data = future.result()
                    if data is not None:
                        pins.append(data)
                except Exception as e:
                    print(e)

            live.update(generate_table(pins, end_pin - start_pin, end_pin - start_pin))

        print(f"{math.floor((end_pin - start_pin) / 1000000 * 10000) / 10000}% of  pins were scanned ({(end_pin - start_pin)} / 1,000,000)")
        print(f"{math.floor(len(pins) / (end_pin - start_pin) * 100 * 10000) / 10000}% of pins scanned where active ({len(pins)} / {end_pin - start_pin})")