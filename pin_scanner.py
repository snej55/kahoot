import asyncio
import time
import datetime
import aiohttp
import concurrent.futures

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()
    
async def scan_pin(pin):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1024)) as session:
            data = await fetch(session, f"https://kahoot.it/reserve/session/{pin}/")
            if time.time() * 1000 - 600000 < data["startTime"]:
                print(pin, datetime.timedelta(seconds=int((time.time() * 1000 - data["startTime"]) / 1000)))
                return (pin, data["startTime"])
    except:
        return None
    finally:
        await asyncio.sleep(0)
        # print(pin)

def scan(pin):
    asyncio.run(scan_pin(pin))

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as e:
        pins = {e.submit(scan, pin): pin for pin in range(10000)}

        for future in concurrent.futures.as_completed(pins):
            try:
                data = future.result()
                # print(data)
            except Exception as e:
                print(e)
            # print(future)
        
