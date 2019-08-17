import discord
import asyncio
import time
import datetime
import os
import logging
from threading import Timer, Thread
from collections import deque
from urllib.request import HTTPError
import runescape
import tempfile

client = discord.Client()

player_lock = asyncio.Lock()
tts_lock = asyncio.Lock()

enabled = True
current_key = None
server_settings = dict()
thread_list = list()
report_queue = deque()

CMD_PREFIX = "rs:"

@client.event
@asyncio.coroutine
def on_ready():
    global thread_list
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print("Current servers:")
    for server in client.guilds:
        print("* {} ({})".format(server.name,server.id))
        logging.info("Connected to server {} ({})".format(server.name,server.id))
    print('------')
    logging.info("Logged in successfully as {} [{}]".format(client.user.name, client.user.id))
    yield from client.change_presence(activity=discord.Game(name='Runescape'))

@client.event
@asyncio.coroutine
def on_message(message):
    global enabled
    global current_key

    logstring = ""
    if(isinstance(message.channel, discord.abc.GuildChannel)):
        logstring+=("[{}/{}] {}: ".format(message.guild.name,message.channel.name,message.author.name))
    elif(isinstance(message.channel, discord.abc.PrivateChannel)):
        logstring+=("[PRIVATE] {}: ".format(message.author.name))
    else:
        logstring+=("[UNKNOWN] {}: ".format(message.author.name))

    content = message.clean_content
    logstring+=content

    if(content.startswith('`') and content.endswith('`')):
        content = message.content[1:-1]

    if(message.author == client.user):
        #Ignore own messages
        return

    for command in command_set:
        for command_str in command["commands"]:
            if content.startswith(CMD_PREFIX+command_str):
                logging.info(logstring)
                with message.channel.typing():
                    yield from command["function"](message)
                return
    logging.debug(logstring)

@client.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    global message_channel
    global enabled
    logging.info("Voice state change for user " + before.name)

def get_key(key_name):
    try:
        with open(".keyfile") as f:
            keylist = f.readlines()
        for x in keylist:
            if(x.split(":"))[0] == key_name:
                return x.split(":")[1].strip()
        logging.error(str("Key "+key_name+" not found."))
        return None
    except:
        return None

@asyncio.coroutine
def send_msg(channel, msg):
    yield from channel.send(msg)

@asyncio.coroutine
def create_rs_text(msg):
    content = msg.content
    if(content.startswith('`') and content.endswith('`')):
        content = msg.content[1:-1]
    logging.info("Parsing message {}".format(msg.id))
    img = runescape.parse_string(content.replace(CMD_PREFIX,""))
    filename = ""
    fileobj = None
    if(len(img)==1):
        fileobj = tempfile.NamedTemporaryFile(suffix=".png",prefix="runescape-")
        filename = fileobj.name
        logging.info("Saving png for {} at {}".format(msg.id, filename))
        runescape.single_frame_save(img[0], file=fileobj.file)
        fileobj.file.flush()
    else:
        fileobj = tempfile.NamedTemporaryFile(suffix=".gif",prefix="runescape-")
        filename = fileobj.name
        logging.info("Saving gif for {} at {}".format(msg.id, filename))
        runescape.multi_frame_save(img, file=fileobj.file)
        fileobj.file.flush()
    fileobj.file.seek(0)
    yield from msg.channel.send(file=discord.File(fileobj.file, filename=filename))
    logging.info("{} uploaded and closed".format(filename))

command_set = [
    {
        "commands":[""],
        "function": create_rs_text
    },
]

discord_token = get_key("discord_bot_token")
if(discord_token == None):
    discord_token = input("You must specify the discord bot token: ")
os.environ['DISCORD_TOKEN'] = discord_token

os.makedirs("logs", exist_ok=True)
file = open("logs/bot.log", "a+")
# file.close()
logging.basicConfig(filename="logs/bot.log",format="(%(asctime)s) %(levelname)s:%(message)s",level=logging.INFO)
logging.info("Logging configured.")

while(True):
    try:
        client.run(os.environ.get('DISCORD_TOKEN'))
    except discord.ConnectionClosed:
        print("ConnectionClosed error. Restarting")
