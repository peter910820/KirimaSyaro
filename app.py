import discord
import os, re
from pytube import YouTube, exceptions


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
            print(type(message.author.voice))
            await join(message)
        elif message.content[1:] == 'leave':
            print(type(message.author.voice))
            await leave(message)
        elif message.content[1:] == 'menu':
            menu = '''
簡易menu 啊我就懶得打(((\n指令如下:
```\n
!join : 讓機器人到發話者的語音頻道\n
!leave : 讓機器人退出語音頻道\n
!play YouTube影片網址 : 增加歌曲到撥放清單並撥放\n
!playlist : 查詢當前撥放清單\n
!pause : 暫停音樂\n
!resume : 恢復音樂
```
暫時不支援撥放清單，然後桐個網址絕對不要添加兩次，絕對會出事。\n打完指令後等他一秒在打下一個指令，不然我也不知道會怎樣('''
            await message.channel.send(menu)

        elif re.match(r"^play .+$", message.content[1:],re.IGNORECASE):
            try:
                yt = YouTube(message.content[6:])
                yt.streams.filter().get_audio_only().download(filename=f'{yt.title}.mp3')
                play(yt.title)
            except exceptions.RegexMatchError:
                await message.channel.send('網址怪怪的呦')
            except:
                title = yt.title
                for f in forbidden_char:
                    title = title.replace(f,' ')
                yt.streams.filter().get_audio_only().download(filename=f'{title}.mp3')
                play(title)

        elif message.content[1:] == 'playlist':
            tmp_str = '```\n'
            if len(playlist) == 0:
                await message.channel.send('撥放清單目前為空呦')
            else:
                for p in playlist:
                    tmp_str = tmp_str + str(p) + '\n'
                tmp_str = tmp_str + '```'
                await message.channel.send(tmp_str)
        

        elif message.content[1:] == 'pause':
            if client.voice_clients[0].is_playing():
                client.voice_clients[0].pause()
                await message.channel.send('歌曲已暫停')
            else:
                await message.channel.send('沒有歌曲正在撥放呦')
        elif message.content[1:] == 'resume':
            if client.voice_clients[0].is_paused():
                client.voice_clients[0].resume()
                await message.channel.send('歌曲已繼續撥放')
            else:
                await message.channel.send('沒有歌曲正在暫停呦')

        ##########################################################

        elif re.match(r"^administrator_permissions_01 .+$", message.content[1:],re.IGNORECASE):
            try:
                yt = YouTube(message.content[30:])
                yt.streams.filter().get_audio_only().download(filename=f'{yt.title}.mp3')
                cycle_play(yt.title)
            except exceptions.RegexMatchError:
                await message.channel.send('網址怪怪的呦')
            except:
                title = yt.title
                for f in forbidden_char:
                    title = title.replace(f,' ')
                yt.streams.filter().get_audio_only().download(filename=f'{title}.mp3')
                cycle_play(title)

@client.event
async def join(message):
    if message.author.voice == None:
        await message.channel.send('使用者還沒進入語音頻道呦')
    elif client.voice_clients == []:
        voiceChannel = message.author.voice.channel
        await voiceChannel.connect()
        song = discord.Activity(type=discord.ActivityType.listening, name = 'Yotube的音樂')
        await client.change_presence(activity=song, status=discord.Status.online)
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
    
##########################################################    

def cycle_play(title):
    client.voice_clients[0].play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=f'{title}.mp3'), after = lambda _ : cycle_play(title))

client.run('MTA3OTAwMTQ2MzYzMzc2MDM0Ng.GimM6F.VUWfP9PjI8RXsc4CthGfdg3jjyPxasLwAs1BSM')