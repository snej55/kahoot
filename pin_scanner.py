import asyncio
import time
import datetime
import aiohttp
import concurrent.futures
from rich.progress import track

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def scan_pin(pin):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1024)) as session:
            await asyncio.sleep(0)
            data = await fetch(session, f"https://kahoot.it/reserve/session/{pin}/")
            if time.time() * 1000 - 600000 < data["startTime"]:
                print(pin, datetime.timedelta(seconds=int((time.time() * 1000 - data["startTime"]) / 1000)))
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

if __name__ == "__main__":
    print("##############################")
    print("# Welcome to the Pin Scanner #")
    print("##############################\n")
    print("Please enter the range of pins to scan (min: 0, max: 1000000)\n")
    start_pin, end_pin = setup()

    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as e:
        futures = {e.submit(scan, pin): pin for pin in range(start_pin, end_pin)}

        pins = []
        for future in track(concurrent.futures.as_completed(futures), description=f'{end_pin - start_pin} pins: scanning...', total=end_pin - start_pin):
            try:
                data = future.result()
                if data is not None:
                    pins.append(data)
            except Exception as e:
                print(e)

    pins.sort(key=lambda x: -x[1])
    print("PINS:")
    for i, pin in enumerate(pins):
        print(f"{i + 1}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")