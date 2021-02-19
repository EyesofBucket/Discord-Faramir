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
    print('{client.user} has connected to Discord!\n\n{server.name}(id: {server.id})')

@client.event
async def on_message(message):
    if message.content == '/sensors':
        response = subprocess.run(['sensors'], capture_output=True, text=True).stdout
        await message.channel.send(response)

client.run(TOKEN)
