import discord
from pytube import YouTube

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is online.')
    print(str(client.latency))
    game = discord.Game("Visual Studio Code")
    await client.change_presence(activity=game, status=discord.Status.online)
    

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        if message.content[1:] == 'ping':
            # print(message.content)
            await message.channel.send(f'延遲時間為:{str(client.latency)}')
        elif message.content[1:] == 'join':
            print(type(client.voice_clients))
            print(message.author.voice)
            await join(message)
        elif message.content[1:] == 'leave':
            print(type(client.voice_clients[0]))
            print(type(message.author.voice))
            await leave(message)

@client.event
async def join(message):
    
    if message.author.voice == None:
        await message.channel.send('使用者還沒進入語音頻道呦')
    elif client.voice_clients == []:
        voiceChannel = message.author.voice.channel
        await voiceChannel.connect()
    else:
        await message.channel.send("我已經在語音頻道了呦")

@client.event
async def leave(message):
    
    if client.voice_clients == []:
        await message.channel.send("我目前不在任何頻道呦")
    else:
        await client.voice_clients[0].disconnect()
        
client.run('MTA3OTAwMTQ2MzYzMzc2MDM0Ng.GimM6F.VUWfP9PjI8RXsc4CthGfdg3jjyPxasLwAs1BSM')