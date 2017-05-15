import discord
from imgur import GetRandomImage
import random

PREFIX = "%"
CLIENT = discord.Client()
GRI = GetRandomImage()
HELP = "```" + \
       "Shitpost Bot\n" + \
       "{0}shitpost           - post random picture\n".format(PREFIX) + \
       "{0}refresh            - load random imgur gallery\n".format(PREFIX) + \
       "{0}load [album_id]    - load custom imgur gallery\n".format(PREFIX) + \
       "{0}insult [@user]     - random insult to mentioned user\n".format(PREFIX) + \
       "```"

async def join(message, server):
    channel_name = message.content[6:]
    for channels in server.channels:
        ch_perms = channels.permissions_for(server.me)
        if channels.name == channel_name and channels.type.name == 'voice':
            if ch_perms.connect and ch_perms.speak and ch_perms.use_voice_activation:
                await CLIENT.join_voice_channel(channels)
            else:
                break

async def leave(message, server):
    voice = CLIENT.voice_CLIENT_in(server)
    await voice.disconnect()

async def insult_user(message, user):
    msg = "{} {}".format(user, random.choice(open("tools//insults.txt").readlines()))
    await CLIENT.send_message(message.channel, msg)

@CLIENT.event
async def on_message(message):
    server = message.server

    if message.author == CLIENT.user:
        return

    elif message.content == ("{}help".format(PREFIX)):
        await CLIENT.delete_message(message)
        await CLIENT.send_message(message.channel, "{}! documentation has "
                                                   "been sent via private message!".format(message.author.mention))
        await CLIENT.send_message(message.author, HELP)

    elif message.content.startswith("{}join".format(PREFIX)):
        await join(message, server)

    elif message.content == ("{}leave".format(PREFIX)):
        await leave(message, server)

    elif message.content == "{}shitpost".format(PREFIX):
        img = get_random_image()
        await CLIENT.delete_message(message)
        await CLIENT.send_message(message.channel, img['url'])

    elif message.content == "{}refresh".format(PREFIX):
        GRI.load_album()
        msg = "Loaded Album: {}\nLink: {}{}".format(GRI.current_album['title'],
                                                    r"www.imgur.com/gallery/",
                                                    GRI.current_album['id'])
        await CLIENT.delete_message(message)
        await CLIENT.send_message(message.channel, msg)

    elif message.content.startswith("{}load".format(PREFIX)):
        _id = message.content[6:]
        GRI.custom_album(_id)
        msg = "Loaded Album: {}\nLink: {}{}".format(GRI.current_album['title'],
                                                    r"www.imgur.com/gallery/",
                                                    _id)
        await CLIENT.delete_message(message)
        await CLIENT.send_message(message.channel, msg)

    elif message.content.startswith("{}insult".format(PREFIX)):
        user = message.content[8:]
        await CLIENT.delete_message(message)
        await insult_user(message, user)

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user)
    print(CLIENT.user.id)
    GRI.load_album()
    await CLIENT.change_presence(game=discord.Game(name="Shitpost Bot || {}help".format(PREFIX)))
    print('ONLINE')

def get_random_image():
    return random.choice(GRI.current_album['images'])

CLIENT.run("MzEzNjgyMDUxNjQxMzc2NzY4.C_tVNA.HxDCaQWTGtqGVhp5TtQTX9eQlug")
