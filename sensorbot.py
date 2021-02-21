import os
import discord
from dotenv import load_dotenv
import subprocess
#from discord.ext import commands, tasks
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

#bot = commands.Bot(command_prefix='/')

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.overheat())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))

    async def overheat(self):
        await self.wait_until_ready()
        channel = self.get_channel(812316744210972672)

        while not self.is_closed():
            sensors = subprocess.run(['sensors'], capture_output=True, text=True).stdout
            temps = []
            total = 0

            for x in range(54, 335, 56):
                temps.append(sensors[x:x+4])

            for x in range(430, 766, 56):
                temps.append(sensors[x:x+4])

            if float(max(temps)) >= 70.0:
                await channel.send("**OVERHEAT!!** " + str(max(temps)))

            await asyncio.sleep(5)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.channel.name != "bot":
            return

        if message.content.startswith("!help"):
            await message.channel.send("Hello, " + message.author.name + "!\n\n **Usage:**\n!help - *Show this help message*\n!sensors - *Return temperature of CPUs on Faramir*\n\n**GitHub:** https://github.com/EyesofBucket/Discord-Faramir")

        if message.content.startswith("!sensors"):
            sensors = subprocess.run(['sensors'], capture_output=True, text=True).stdout
            temps = []
            total = 0

            for x in range(54, 335, 56):
                temps.append(sensors[x:x+4])
    
            for x in range(430, 766, 56):
                temps.append(sensors[x:x+4])

            for x in temps:
                total = float(total) + float(x)

            response = "**CPU Temps**\n*Avg Temp:* " + str(total / len(temps))[:4] + "°C\n*Max Temp:* " + str(max(temps)) + "°C"
            await message.channel.send(str(response))

client = BotClient()
client.run(TOKEN)
