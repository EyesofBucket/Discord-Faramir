import os
import discord
from dotenv import load_dotenv
from datetime import datetime, timezone
import subprocess
#from discord.ext import commands, tasks
import asyncio
import re
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
CHANNEL_BOT = os.getenv('CHANNEL_BOT')
CHANNEL_ADMIN = os.getenv('CHANNEL_ADMIN')
CHANNEL_DOWNTIME = os.getenv('CHANNEL_DOWNTIME')
HOMEDIR = os.getenv('HOMEDIR')

#bot = commands.Bot(command_prefix='/')

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.overheat())
        self.bg_task = self.loop.create_task(self.maintenance())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print(CHANNEL_BOT + "\n" + CHANNEL_ADMIN + "\n" + CHANNEL_DOWNTIME)
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

    async def maintenance(self):
        await self.wait_until_ready()
        channel = self.get_channel(813591477460140053)
        schedule = 0
        
        while not self.is_closed():
            if os.path.isfile('/run/systemd/shutdown/scheduled'):
                if schedule <= 1: # 0 or 1 send message
                    schedule = 2
                    shutdowntime = subprocess.run(["perl -wne 'm/^USEC=(\d+)\d{6}$/ and printf(%s, scalar localtime $1)' < /run/systemd/shutdown/scheduled"], shell=True, capture_output=True, text=True).stdout
                    shutdownmode = subprocess.run(['cat /run/systemd/shutdown/scheduled | grep MODE'], shell=True, capture_output=True, text=True).stdout
                    #timedate = datetime.fromtimestamp(int(shutdowntime[5:]))
#                    mode = shutdownmode[5:]
                    print("before json")
                    f = open(HOMEDIR + 'sdargs.json',)
                    print("opened")
                    sdargs = json.load(f)
                    print(sdargs)
                    #sdargs = json.loads(sdjson)
                    #print(sdargs)
                    print(sdargs["sdduration"])
                    await channel.send("**Maintenance Scheduled:**\nScheduled for: {1}\nType: {0}Description: {2}\nEstimated Duration: {3}".format(shutdownmode[5:], shutdowntime, sdargs["sdmessage"], sdargs["sdduration"]))
                    #open(HOMEDIR + 'sdargs.json', 'w').close()
            elif schedule > 0:
                schedule = 0
                await channel.send("**Maintenance Cancelled**")
            await asyncio.sleep(5)

    async def on_message(self, message):
        prefix="!"
        if message.author.id == self.user.id:
            return

# ALL USERS

        if message.content.startswith(prefix + "help"):
            await message.channel.send("Hello, " + message.author.name + "!\n\n **Usage:**\n!help - *Show this help message*\n!sensors - *Return temperature of CPUs on Faramir*\n\n**GitHub:** https://github.com/EyesofBucket/Discord-Faramir")

# ADMIN ONLY

        if message.channel.name != "admin":
            return

        if message.content.startswith(prefix + "shutdown"):
            msg = message.content
            sdtype = re.search(" -type ([^ ]*)",msg)
            sdmessage = re.search(" -message \"([^\"]*)",msg)
            sdtime = re.search("-time ([^ ]*)",msg)
            sdduration = re.search("-duration \"([^\"]*)",msg)
            sdcancel = re.search("-cancel",msg)
            cancel = ""
            
            try:
                cancel = sdcancel.group(0)
            except:
                print("whoops")

            if cancel == "-cancel":
                subprocess.run(['shutdown', '-c']).stdout
            else:
                args ={
                    "sdmessage" : sdmessage.group(1),
                    "sdduration" : sdduration.group(1)
                }
                
                with open(HOMEDIR + "sdargs.json", "w") as outfile:
                    json.dump(args, outfile)
                
                # Parse shutdown type into shell argument
                if sdtype.group(1) == "reboot":
                     typeflag = "-r"
                elif sdtype.group(1) == "shutdown":
                     typeflag = "-P"
                
                subprocess.run(['shutdown', typeflag, sdtime.group(1)]).stdout

        if message.content.startswith(prefix + "sensors"):
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
