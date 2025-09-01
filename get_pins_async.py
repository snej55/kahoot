import asyncio
import time
import datetime
import aiohttp
import concurrent.futures

NUM_SCANNERS = 1 # number of scanners
INDIE_PIN_INFO = True # show debug info about pins per search
STEP_SIZE = 1000 # number of pins per search
SCANNERS_SIZE = 10000 # number of pins per scanner
TIME_RANGE = 10 # range of minutes to search for

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def scan_pin(pin):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000)) as session:
            url = f"https://kahoot.it/reserve/session/{pin}/"
            data = await fetch(session, url)
            t = int(time.time()) * 1000
            if t - TIME_RANGE * 60000 < data["startTime"]:
                return (pin, data["startTime"])
    except Exception as e:
        await asyncio.sleep(1)
        print(e)
        pass

async def scan_range(start_pin, end_pin):
    print(f"--------------- {start_pin} - {end_pin} ---------------")
    # execute coroutines concurrently
    results = await asyncio.gather(*(scan_pin(pin) for pin in range(start_pin, end_pin)))


    if INDIE_PIN_INFO:
        pins = [result for result in results if result != None]
        pins.sort(key=lambda x: -x[1])
        if len(pins):
            print(f"Best pin ({start_pin} - {end_pin}): {pins[0][0]}, started {datetime.timedelta(seconds=int(time.time() - pins[0][1] / 1000))} ago")

    return [result for result in results if result != None]

def scan(start, end):
    pins = []

    # scan all pins in range
    for start_pin in range(start, end, STEP_SIZE):
        pins.extend(asyncio.run(scan_range(start_pin, start_pin + STEP_SIZE)))
    
    print("---------------------------------")
    print(f"FINISHED SCANNING! ({start} - {end})")
    print("---------------------------------")

    if INDIE_PIN_INFO:
        pins.sort(key=lambda x: -x[1])
        print("PINS:")
        for i, pin in enumerate(pins):
            print(f"{i}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")

    return pins

print(f'Started scanning at {datetime.timedelta(seconds=int(time.time()))}')

pins = []
# create new thread for each scanner
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_SCANNERS) as e:
    threads = []
    for i in range(NUM_SCANNERS):
        threads.append(e.submit(scan, i * SCANNERS_SIZE, i * SCANNERS_SIZE + SCANNERS_SIZE))
    
    # get results of each scanner
    for t in concurrent.futures.as_completed(threads):
        pins.extend(t.result())

pins.sort(key=lambda x: -x[1])
print("##################\n\n\n\n\n\n\n\n\n##################")
print(f"PINS: 0 - {SCANNERS_SIZE * NUM_SCANNERS}")
for i, pin in enumerate(pins):
    print(f"{i}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")

    
