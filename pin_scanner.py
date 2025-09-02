import asyncio
import time
import datetime
import aiohttp
import concurrent.futures
from rich.progress import track

NUM_PINS = 10000

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

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as e:
        futures = {e.submit(scan, pin): pin for pin in range(NUM_PINS)}

        pins = []
        for future in track(concurrent.futures.as_completed(futures), description=f'{NUM_PINS} pins: scanning...', total=NUM_PINS):
            try:
                data = future.result()
                if data is not None:
                    pins.append(data)
            except Exception as e:
                print(e)

pins.sort(key=lambda x: -x[1])
print("PINS:")
for i, pin in enumerate(pins):
    print(f"{i}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")

    
