import asyncio
import threading
import random
import time
import requests

from kahoot import KahootClient
from kahoot.packets.impl.respond import RespondPacket
from kahoot.packets.server.game_over import GameOverPacket
from kahoot.packets.server.game_start import GameStartPacket
from kahoot.packets.server.question_end import QuestionEndPacket
from kahoot.packets.server.question_ready import QuestionReadyPacket
from kahoot.packets.server.question_start import QuestionStartPacket

async def question_start(packet: QuestionStartPacket):
    print(f"Question started: {packet}")

async def main(username, pin):
    client = KahootClient()

    async def game_start(packet: GameStartPacket):
        print(f"Game started: {packet}")

    async def game_over(packet: GameOverPacket):
        print(f"Game over: {packet}")

    async def question_start(packet: QuestionStartPacket):
        print(f"Question started: {packet}")
        question_number: int = packet.game_block_index
        time.sleep(random.random() * 6)
        await client.send_packet(RespondPacket(client.game_pin, random.randint(0, packet.number_of_choices), question_number))

    async def question_end(packet: QuestionEndPacket):
        print(f"Question ended: {packet}")

    async def question_ready(packet: QuestionReadyPacket):
        print(f"Question ready: {packet}")
    
    client.on("game_start", game_start)
    client.on("game_over", game_over)
    client.on("question_start", question_start)
    client.on("question_end", question_end)
    client.on("question_ready", question_ready)
    await client.join_game(game_pin=pin, username=username)

def join(username, pin):
    time.sleep(random.random() * 10)
    asyncio.run(main(username, pin))

def getUserName(userData):
    print(userData)
    try:
        return random.choice(
            [
                userData["results"][0]["name"]["first"],
                userData["results"][0]["name"]["first"],
                userData["results"][0]["name"]["first"] + " " + userData["results"][0]["name"]["last"],
                userData["results"][0]["name"]["title"] + ". " + userData["results"][0]["name"]["last"],
                userData["results"][0]["login"]["username"],
                userData["results"][0]["login"]["username"],
                (userData["results"][0]["name"]["first"] + " " + userData["results"][0]["name"]["last"]).lower()
            ]
        )
    except IndexError:
        return random.choice(["Paw Patrol Hero", "PIKACHU", "i eat pork", "bananarama", "Butter", "Jonathan", "aah pickles", "Mrs. Norris", "Ronald Weasley"])

pin = 000000
while True:
    try:
        pin = int(input("Enter the game pin: "))
        break
    except ValueError:
        print("Please enter a number!")

numBots = 0
while True:
    try:
        numBots = int(input("Enter the number of bots desired: "))
        if numBots < 0:
            raise ValueError
        break
    except ValueError:
        print("Please enter a number!")

names = []
for _ in range(numBots):
    userData = requests.get("https://randomuser.me/api").json()
    names.append(getUserName(userData))

threads = []

for word in names:
    t = threading.Thread(target=join, args=(word, pin))
    t.start()
    threads.append(t)

for t in threads:
    t.join()