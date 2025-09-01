import asyncio
import time
import datetime
import aiohttp
import concurrent.futures

STEP_SIZE = 500
NUM_THREADS = 4
THREADS_SIZE = 10000
THREAD_PIN_INFO = False

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def scan_pin(pin):
    try:
        async with aiohttp.ClientSession() as session:
            t = int(time.time()) * 1000
            url = f"https://kahoot.it/reserve/session/{pin}/"
            data = await fetch(session, url)
            if t - 1000000 < data["startTime"]:
                return (pin, data["startTime"])
    except Exception as e:
        pass

async def scan_range(start_pin, end_pin):
    print(f"--------------- {start_pin} - {end_pin} ---------------")
    # create coroutines
    coroutines = [scan_pin(pin) for pin in range(start_pin, end_pin)]
    # execute coroutines concurrently
    results = await asyncio.gather(*coroutines)

    pins = [result for result in results if result != None]
    pins.sort(key=lambda x: -x[1])

    if THREAD_PIN_INFO:
        print(f"Found {len(pins)} pins")
        if len(pins):
            print(f"Best pin: {pins[0][0]}, started at {str(datetime.timedelta(seconds=int(pins[0][1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pins[0][1] / 1000))} ago")

    return pins

def scan(start, end):
    pins = []

    for start_pin in range(start, end, STEP_SIZE):
        pins.extend(asyncio.run(scan_range(start_pin, start_pin + STEP_SIZE)))
    pins.sort(key=lambda x: -x[1])
    
    print("---------------------------------")
    print("FINISHED SCANNING!")
    print("---------------------------------")

    if THREAD_PIN_INFO:
        print("PINS:")
        for i, pin in enumerate(pins):
            print(f"{i}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")

    return pins


pins = []
with concurrent.futures.ThreadPoolExecutor(max_workers = NUM_THREADS) as e:
    print(f'Started scanning at {datetime.timedelta(seconds=int(time.time()))}')

    threads = []
    for i in range(NUM_THREADS):
        threads.append(e.submit(scan, i * THREADS_SIZE, i * THREADS_SIZE + THREADS_SIZE))
    
    for t in concurrent.futures.as_completed(threads):
        pins.extend(t.result())

pins.sort(key=lambda x: -x[1])
print("PINS:")
for i, pin in enumerate(pins):
    print(f"{i}. Pin: {pin[0]}, started at {str(datetime.timedelta(seconds=int(pin[1] / 1000))).split(' ')[-1]}, {datetime.timedelta(seconds=int(time.time() - pin[1] / 1000))} ago")

    
