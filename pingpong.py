from nextcord import *
from dotenv import load_dotenv
import os
load_dotenv()



TOKEN = os.getenv("TOKEN")
CLIENT = Client()



@CLIENT.event
async def on_ready():
    print(f"Bot is ready as {CLIENT.user}")

@CLIENT.slash_command(name = "ping" , description = "봇의 핑을 보여줌")
async def ping(inter : Interaction):
    ping = int(round(CLIENT.latency * 1000))
    embed = Embed(title = "pong!", description = ("ping : {}ms").format(ping), color=0x706172)
    await inter.send(embed = embed)

    del ping , embed


if __name__ == "__main__":
    CLIENT.run(TOKEN)