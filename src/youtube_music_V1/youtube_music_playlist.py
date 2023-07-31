import discord
import os, asyncio
from pytube import YouTube

forbidden_char = ['/','\\',':','*','?','"','<','>',"|"]
playlist, playlistUrl = [], []
original_title = []

def youtube_playlist(yt_playlist, message, client):  # def msg = the playlist URl
    if type(yt_playlist) != str: # yt_playlist is int or playlist
        if yt_playlist == 1: 
            if original_title in playlist:
                playlist.pop(0)
            original_title.pop()
            playlistUrl.pop(0)
            try:
                for file in os.scandir('O:/Myproject/syaroBot/music_tmp/'):
                    os.remove(file.path)
            except:
                print('OS錯誤')
        elif yt_playlist == 2: 
            print(original_title)
        else:
            for y in yt_playlist.video_urls:
                playlistUrl.append(y)
            print(playlistUrl)
            # playlist.append(yt_playlist.title)
    else:                        # yt_playlist is ia single music
        music = YouTube(yt_playlist)
        playlist.append(music.title)
        playlistUrl.append(yt_playlist)

    if len(playlistUrl) != 0 and client.voice_clients[0].is_playing() != True: 
        music = YouTube(playlistUrl[0])
        original_title.append(music.title)
        title = music.title
        try:
            music.streams.filter().get_lowest_resolution().download(filename=f'O:/Myproject/syaroBot//music_tmp/{title}.mp3')
        except:
            for f in forbidden_char:
                title = title.replace(f,' ')
            music.streams.filter().get_lowest_resolution().download(filename=f'O:/Myproject/syaroBot/music_tmp/{title}.mp3')
        client.voice_clients[0].play(discord.FFmpegOpusAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=f'O:/Myproject/syaroBot/music_tmp/{title}.mp3'), after = lambda _ : youtube_playlist(1, message, client))
    else:
        return
    
async def show_playlist(message, client):
    if len(playlist) == 0:
        await message.channel.send('播放清單目前為空呦')
    else:
        tmp_str = f'```\n現在歌曲:{original_title[0]}\n播放清單剩餘歌曲:\n'
        for p in playlist:
            tmp_str = tmp_str + str(p) + '\n'
        tmp_str = tmp_str + '```'
        await message.channel.send(tmp_str)

async def show_crrent_song(message, client):
    if len(original_title) == 0:
        await message.channel.send('播放清單目前為空呦')
    else:
        tmp_str = f'現在歌曲: **{original_title[0]}**'
        await message.channel.send(tmp_str)

async def stop_music(message, client):
    if client.voice_clients[0] != []:
        if client.voice_clients[0].is_playing():
            client.voice_clients[0].stop()
            print(client.voice_clients[0].is_playing())
            # await message.channel.send('歌曲已跳過')
        else:
            await message.channel.send('沒有歌曲正在播放呦')
    else:
        await message.channel.send('我還沒加入語音頻道呦')