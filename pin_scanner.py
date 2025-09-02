import asyncio
import time
import datetime
import aiohttp
import concurrent.futures

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
    asyncio.run(scan_pin(pin))

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as e:
        pins = {e.submit(scan, pin): pin for pin in range(NUM_PINS)}

        for future in concurrent.futures.as_completed(pins):
            try:
                data = future.result()
            except Exception as e:
                print(e)

pins = [key.result() for key in pins if key.result() is not None]
pins.sort(key=lambda x: -x[1])
print("PINS:")
for i, pin in enumerate(pins):
    print(f"{i}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")

    
