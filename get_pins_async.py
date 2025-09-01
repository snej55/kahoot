import asyncio
import time
import datetime
import aiohttp

STEP_SIZE = 500

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def scan_pin(pin):
    try:
        async with aiohttp.ClientSession() as session:
            t = int(time.time()) * 1000
            url = f"https://kahoot.it/reserve/session/{pin}/"
            data = await fetch(session, url)
            return (pin, data["startTime"])
    except Exception as e:
        pass

async def scan(start_pin, end_pin):
    print(f"--------------- {start_pin} - {end_pin} ---------------")
    # create coroutines
    coroutines = [scan_pin(pin) for pin in range(start_pin, end_pin)]
    # execute coroutines concurrently
    results = await asyncio.gather(*coroutines)

    pins = [result for result in results if result != None]
    pins.sort(key=lambda x: -x[1])

    # for result in pins:
    #     if result != None:
    #         print(f"Found pin: {result[0]}, started at {str(datetime.timedelta(seconds=int(result[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - result[1] / 1000))} ago")

    return pins

if __name__ == "__main__":
    pins = []
    print(f'Started scanning at {datetime.timedelta(seconds=time.time())}')
    
    for start_pin in range(0, 10000, STEP_SIZE):
        pins.extend(asyncio.run(scan(start_pin, start_pin + STEP_SIZE)))
    pins.sort(key=lambda x: -x[1])
    
    print("---------------------------------")
    print("FINISHED SCANNING!")
    print("---------------------------------")

    print("PINS:")
    for i, pin in enumerate(pins):
        print(f"{i}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")