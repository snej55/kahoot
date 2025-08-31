import asyncio
import threading
import random
import time
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
    asyncio.run(main(username, pin))

pin = 000000
while True:
    try:
        pin = int(input("Enter the game pin: "))
        break
    except ValueError:
        print("Please enter a number!")

done = False

while not done:
    lyrics = input("Enter your text: ")
    threads = []

    lyrics = lyrics.split(" ")
    lyrics.reverse()

    for word in lyrics:
        t = threading.Thread(target=join, args=(word, pin))
        time.sleep(0.3)
        t.start()
        threads.append(t)
    
    done = input("Are you done? (y): ").lower() == "y"

for t in threads:
    t.join()