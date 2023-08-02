import discord
import os, re
from pytube import YouTube, exceptions, Playlist

from src.youtube_music_V1.youtube_music_playlist import *
from src.youtube_music_V1.youtube_music_operate import *
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

forbidden_char = ['/','\\',':','*','?','"','<','>',"|"]
playlist = []

@client.event
async def on_ready():
    print(f'{client.user} is online.')
    print(f'延遲時間為:{str(client.latency)}')
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
            await join(message)
        elif message.content[1:] == 'leave':
            await leave(message)
        elif message.content[1:] == 'menu':
            menu = '''
簡易menu 啊我就懶得打(((\n指令如下:
```\n
!join : 讓機器人到發話者的語音頻道\n
!leave : 讓機器人退出語音頻道\n
!play YouTube影片網址 : 增加歌曲到播放清單並播放\n
!playlist : 查詢當前播放清單\n
!pause : 暫停音樂\n
!resume : 恢復音樂
```
暫時不支援播放清單，然後同個網址絕對不要添加兩次，絕對會出事。\n打完指令後等他一秒在打下一個指令，不然我也不知道會怎樣('''
            await message.channel.send(menu)

        elif re.match(r"^play_playlist .+$", message.content[1:]):
            yt_playlist = Playlist(message.content[6:])
            try:
                print(yt_playlist.owner)
            except:
                await message.channel.send('網址怪怪的呦')
            youtube_playlist(yt_playlist, message, client)

        elif re.match(r"^play .+$", message.content[1:]):
            youtube_playlist(message.content[6:], message, client,)

        elif message.content[1:] == 'playlist':
            tmp_str = '```\n'
            if len(playlist) == 0:
                await message.channel.send('播放清單目前為空呦')
            else:
                for p in playlist:
                    tmp_str = tmp_str + str(p) + '\n'
                tmp_str = tmp_str + '```'
                await message.channel.send(tmp_str)
        elif message.content[1:] == 'test_playlist':
            await show_playlist(message, client)
        elif message.content[1:] == 'now':
            await show_crrent_song(message, client)
        elif message.content[1:] == 'skip':
            await stop_music(message, client)


        elif message.content[1:] == 'close':
            await close()
        
        ##########################################################

        elif re.match(r"^administrator_permissions_01 .+$", message.content[1:],re.IGNORECASE):
            try:
                yt = YouTube(message.content[30:])
                yt.streams.filter().get_lowest_resolution().download(filename=f'{yt.title}.mp3')
                cycle_play(yt.title)
            except exceptions.RegexMatchError:
                await message.channel.send('網址怪怪的呦')
            except:
                title = yt.title
                for f in forbidden_char:
                    title = title.replace(f,' ')
                yt.streams.filter().get_lowest_resolution().download(filename=f'{title}.mp3')
                cycle_play(title)

@client.event
async def join(message):
    if message.author.voice == None:
        await message.channel.send('使用者還沒進入語音頻道呦')
    elif client.voice_clients == []:
        voiceChannel = message.author.voice.channel
        await voiceChannel.connect()
        music = discord.Activity(type=discord.ActivityType.listening, name = 'Yotube的音樂')
        await client.change_presence(activity=music, status=discord.Status.online)
    else:
        await message.channel.send("我已經在語音頻道了呦")

@client.event
async def leave(message):
    if client.voice_clients == []:
        await message.channel.send("我目前不在任何頻道呦")
    else:
        await client.voice_clients[0].disconnect()
        game = discord.Game("Visual Studio Code")
        await client.change_presence(activity=game, status=discord.Status.online)

def play(title):
    print(title)
    if title in playlist:
        playlist.remove(title)
        os.remove(f'S:/Myproject/syaroBot/{title}.mp3')
    else:
        playlist.append(title)
        print(playlist)
    print(len(playlist))
    if len(playlist) != 0 and client.voice_clients[0].is_playing() == False:
        client.voice_clients[0].play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=f'{playlist[0]}.mp3'), after = lambda _ : play(playlist[0]))
    else:
        return
    
async def close():
    await client.close()
##########################################################    

def cycle_play(title):
    client.voice_clients[0].play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=f'{title}.mp3'), after = lambda _ : cycle_play(title))

client.run('MTA3OTAwMTQ2MzYzMzc2MDM0Ng.GimM6F.VUWfP9PjI8RXsc4CthGfdg3jjyPxasLwAs1BSM')