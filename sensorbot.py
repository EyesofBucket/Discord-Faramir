import os
import discord
from dotenv import load_dotenv
import subprocess

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
#print(TOKEN)

client = discord.Client()

@client.event
async def on_ready():
    for server in client.guilds:
        if server.name == SERVER:
            break
    print('{} has connected to Discord!\n\n{}(id: {})'.format(client.user, server.name, server.id))

@client.event
async def on_message(message):
    if message.content == '/sensors':
        sensors = subprocess.run(['sensors'], capture_output=True, text=True).stdout
        temps = []
        total = 0

        for x in range(54, 335, 56):
            temps.append(sensors[x:x+4])
            #print(sensors[x:x+4])

        for x in range(430, 766, 56):
            temps.append(sensors[x:x+4])
            #print(sensors[x:x+4])

        for x in temps:
            #print(x, total)
            total = float(total) + float(x)

        #print(len(temps))
        response = "**CPU Temps:**\nAvg Temp: " + str(total / len(temps))[:4] + "°C\nMax Temp: " + str(max(temps)) + "°C"
        await message.channel.send(str(response))

client.run(TOKEN)
