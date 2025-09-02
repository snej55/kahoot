# Kahoot bot generator & pin scanner

## Pin scanners

Ever wanted to join a random kahoot game? These scripts scan for open games by checking if pins are active. There are three, but is `pin_scanner.py` is the recommended one. If `pin_scanner.py` is too slow on your system, try `get_pins_async.py` instead.

`get_pins.py` scans the pins synchronously (*very slow*), `get_pins_async.py` scans the pins asynchronously (*very fast*), and `pin_scanner.py` uses multiprocessing to scan the pins (*very fast*). See [the different scripts](https://github.com/snej55/kahoot/tree/main?tab=readme-ov-file#the-different-scripts) for more details.



## Bot generator & libraries
Two python scripts to generate kahoot bots. They can have auto-generated names or be used to display texts in the lobby.

These scripts heavily rely on the  [KahootPY](https://github.com/vehbiu/kahoot-py/tree/main) library. You can install it with:

```
pip install kahoot
```

Or just do:
```
pip install -r requirements.txt
```

### The different scripts:

 - `text.py` asks you to enter a text (song lyrics, etc), and then generates a new bot for each word.
 - `names.py` generates a specified number of bots with random names & usernames.
 - `pin_scanner.py` is a (*fast*) pin scanner that uses rich to display live results in a sorted table. This is the most useable scanner as well as the most efficient, so generally use this one over the others. If it's too slow on your system, try `get_pins_async.py` instead.
 - `get_pins_async.py` scans kahoot pins asynchronously (*fast*). Scans the first 40,000 pins at the moment (10,000 per thread), though you can easily configure this. Only gives useful results at the end of the scan. Generally use `pin_scanner.py` instead.
 - `get_pins.py` scans kahoot pins in sequence (*snail pace*)

### Running:

1. Clone the repo:

```
git clone https://github.com/snej55/kahoot.git
cd kahoot
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Run it!

```
python3 text.py
# or
python3 ...
```
