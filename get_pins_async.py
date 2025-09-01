import asyncio
import time
import requests
import datetime

async def scan_pin(pin):
    t = int(time.time()) * 1000
    try:
        url = f"https://kahoot.it/reserve/session/{pin}/"
        data = requests.get(url).json()
        if t - 1000000 < data["startTime"]:
            print(f"Started {datetime.timedelta(seconds=int((t - data["startTime"]) / 1000))} ago (pin: {pin}), at {datetime.timedelta(seconds=int(data["startTime"] / 1000))}")
    except:
        pass

async def pin_scan(start_pin, end_pin):
    scans = []
    for pin in range(start_pin, end_pin):
        scans.append(scan_pin(pin))
    await asyncio.gather(*scans)

if __name__ == "__main__":
    asyncio.run(pin_scan(0, 1000000))