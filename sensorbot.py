import os
import discord
from dotenv import load_dotenv
import subprocess
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
#print(TOKEN)

bot = commands.Bot(command_prefix='/')

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super()
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

@tasks.loop(seconds=5.0)
async def overheat(channel):
    await 
    sensors = subprocess.run(['sensors'], capture_output=True, text=True).stdout
    temps = []
    total = 0

    for x in range(54, 335, 56):
        temps.append(sensors[x:x+4])
        #print(sensors[x:x+4])

    for x in range(430, 766, 56):
        temps.append(sensors[x:x+4])

    if float(max(temps)) >= 35.0:
        await channel.send("**OVERHEAT!!** " + str(max(temps)))

@bot.command()
async def sensors(ctx):
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
    response = "**CPU Temps**\n*Avg Temp:* " + str(total / len(temps))[:4] + "°C\n*Max Temp:* " + str(max(temps)) + "°C"
    await ctx.send(str(response))

overheat.start(channel_bot)
bot.run(TOKEN)
