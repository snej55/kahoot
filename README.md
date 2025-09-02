# Kahoot bot generator & pin scanner

## Pin scanners

Every wanted to join a random kahoot game? These scripts scan for open games by checking each pin. `get_pins.py` scans the pins synchronously (*very slow*), `get_pins_async.py` scans the pins asynchronously (*very fast*), and `pin_scanner.py` uses multiprocessing to scan the pins (*very fast*).

## Bot generator
Two python scripts to generate kahoot bots. They can have auto-generated names or be used to display texts in the lobby.

These scripts heavily rely on the  [KahootPY](https://github.com/vehbiu/kahoot-py/tree/main) library. You can install it with:

```
pip install -U KahootPY
```

### The different scripts:

 - `main.py` asks you to enter a text (song lyrics, etc), and then generates a new bot for each word.
 - `names.py` generates a specified number of bots with random names & usernames.
 - `get_pins.py` scans kahoot pins in sequence (*very slow*)
 - `get_pins_async.py` scans kahoot pins asynchronously (*fast*). Scans the first 40,000 pins at the moment (10,000 per thread). Gives useful results at the end of the scan.
 - `pin_scanner.py` Alternate pin scanner with similar speed to `get_pins_async.py` (*fast*). Only scans the first 10,000 pins at the moment, you can configure this in the code. Gives the results as it scans.

### Running:

1. Clone the repo:

```
git clone https://github.com/snej55/kahoot.git
cd kahoot
```

2. Install the required packages:

```
pip install -U KahootPY requests
```

3. Run it!

```
python3 main.py
# or
python3 ...
```
