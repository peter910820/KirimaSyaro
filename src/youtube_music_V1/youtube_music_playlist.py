import discord
import os
from pytube import YouTube

forbidden_char = ['/','\\',':','*','?','"','<','>',"|"]
playlist, playlistUrl = [], []
original_title = []

def youtube_playlist(yt_playlist, client):  # def msg = the playlist URl

    if type(yt_playlist) != str: # yt_playlist is int or playlist
        if yt_playlist == 1: 
            # playlist.pop(0)
            original_title.pop()
            playlistUrl.pop(0)
            try:
                for file in os.scandir('S:/Myproject/syaroBot/music_tmp/'):
                    os.remove(file.path)
            except:
                print('這是個不重要的Bug')
        else:
            for y in yt_playlist.video_urls:
                playlistUrl.append(y)
            print(playlistUrl)
            playlist.append(yt_playlist.title)
    else:                        # yt_playlist is ia single music
        music = YouTube(yt_playlist)
        original_title.append(music.title)
        playlistUrl.append(yt_playlist)

    if len(playlistUrl) != 0: 
        music = YouTube(playlistUrl[0])
        original_title.append(music.title)
        title = music.title
        try:
            music.streams.filter().get_audio_only().download(filename=f'S:/Myproject/syaroBot/music_tmp/{title}.mp3')
        except:
            for f in forbidden_char:
                title = title.replace(f,' ')
            music.streams.filter().get_audio_only().download(filename=f'S:/Myproject/syaroBot/music_tmp/{title}.mp3')
        client.voice_clients[0].play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=f'S:/Myproject/syaroBot/music_tmp/{title}.mp3'), after = lambda _ : youtube_playlist(1, client))
    else:
        return
    
async def show_playlist(message, client):
    if len(playlist) == 0:
        await message.channel.send('撥放清單目前為空呦')
    else:
        tmp_str = f'```\n現在歌曲:{original_title[0]}\n撥放清單剩餘歌曲:\n'
        for p in playlist:
            tmp_str = tmp_str + str(p) + '\n'
        tmp_str = tmp_str + '```'
        await message.channel.send(tmp_str)