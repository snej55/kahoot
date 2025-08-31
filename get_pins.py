import time
import requests
import threading
import datetime

def scan(start, end):
    t = int(time.time()) * 1000
    print(f"looking from {t} ms between {start} and {end}")
    valid = False
    url = ""
    data = {}
    for pin in range(start, end):
        t = int(time.time()) * 1000
        try:
            url = f"https://kahoot.it/reserve/session/{pin}/"
            data = requests.get(url).json()
            if t - 1000000 < data["startTime"]:
                valid = True
                print(f"Started {datetime.timedelta(seconds=int((t - data["startTime"]) / 1000))} ago (pin: {pin})")
            else:
                valid = False
        except Exception:
            pass
            # print("error")
        if valid:
            print(f"Pin: {pin}")
        valid = False

threads = []
num_threads = 100
start = 0
gran = 1000000 / num_threads
for _ in range(num_threads):
    t = threading.Thread(target=scan, args=(int(start), int(start + gran)))
    t.start()
    threads.append(t)
    start += gran