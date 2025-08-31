## Kahoot bot generator

Two python scripts to generate kahoot bots. They can have auto-generated names or be used to display texts in the lobby.

These scripts heavily rely on the  [KahootPY](https://github.com/vehbiu/kahoot-py/tree/main) library. You can install it with:

```
pip install -U KahootPY
```

### The different scripts:

 - `main.py` asks you to enter a text (song lyrics, etc), and then generates a new bot for each word.
 - `names.py` generates a specified number of bots with random names & usernames.

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
python3 names.py
```
