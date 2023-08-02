import discord
from discord.ext import commands
from pytube import YouTube, Playlist
import os

class YoutubePlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forbidden_char = ['/','\\',':','*','?','"','<','>',"|"]
        self.play_queue = []
        self.title_queue = []
        self.ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'
        self.song_path = 'O:/Myproject/syaroBot/music_tmp/'

        self.play_prefix = "https://www.youtube.com/"
        self.playlist_prefix = ["https://www.youtube.com/playlist?list=", "https://youtube.com/playlist?list="]

    @commands.command()
    async def menu(self, ctx):
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
            暫時不支援播放清單，然後同個網址絕對不要添加兩次，絕對會出事。\n打完指令後等他一秒在打下一個指令，不然我也不知道會怎樣(
            '''
        await ctx.send(menu)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice == None:
            await ctx.send("使用者還沒進入語音頻道呦")
        elif self.bot.voice_clients == []:
            voiceChannel = ctx.author.voice.channel
            await voiceChannel.connect()
            music = discord.Activity(type=discord.ActivityType.listening, name = "Yotube的音樂")
            await self.bot.change_presence(activity=music, status=discord.Status.online)
        else:
            await ctx.send("我已經在語音頻道了呦")

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice == None:
            await ctx.send("使用者還沒進入語音頻道呦")
        elif self.bot.voice_clients == []:
            await ctx.send("我目前不在任何頻道呦")
        else:
            await self.bot.voice_clients[0].disconnect()
            game = discord.Game("ブルーアーカイブ -Blue Archive-") # status
            await self.bot.change_presence(status=discord.Status.online, activity=game)
            self.play_queue = []

    @commands.command()
    async def now(self, ctx):
        if len(self.title_queue) == 0:
            await ctx.send('播放清單目前為空呦')
        else:
            tmp_str = f"現在歌曲: **{self.title_queue[0]}**"
            await ctx.send(tmp_str)

    @commands.command()
    async def skip(self, ctx, count=1):
        if self.bot.voice_clients[0] != []:
            if self.bot.voice_clients[0].is_playing():
                self.bot.voice_clients[0].stop()
                if count > 1:
                    count -= 1
                    for _ in range(0, count):
                        self.play_queue.pop(0)
                        self.title_queue.pop(0)
                await ctx.send('歌曲已跳過')
            # else:
            #     await ctx.send('沒有歌曲正在播放呦')
        else:
            await ctx.send('我還沒加入語音頻道呦')

    @commands.command()        
    async def look(self, ctx):
        if len(self.play_queue) == 0:
            await ctx.send('播放清單目前為空呦')
        else:
            playlist_check = f"```\n播放清單剩餘歌曲: {len(self.play_queue)}首\n"
            for index, t in enumerate(self.title_queue, start=1):
                playlist_check += f"{index}. {t}\n"
                if len(playlist_check) >= 500:
                    playlist_check += " ...還有很多首"
                    break
            playlist_check += "```"
            print(self.play_queue)
            await ctx.send(playlist_check)

    @commands.command()
    async def play(self, ctx, url):
        if url.startswith(self.playlist_prefix[0]) or url.startswith(self.playlist_prefix[1]):
            if ctx.author.voice == None:
                await ctx.send('使用者還沒進入語音頻道呦')
            elif self.bot.voice_clients == []:
                voiceChannel = ctx.author.voice.channel
                await voiceChannel.connect()
                music = discord.Activity(type=discord.ActivityType.listening, name = 'Yotube的音樂')
                await self.bot.change_presence(activity=music, status=discord.Status.online)

                for file in os.scandir(self.song_path): #刪除之前的mp3檔案
                    if file.path[-4:] == '.mp3':
                        os.remove(file.path)

                url_parse = Playlist(url)
                print(url_parse.video_urls)
                for p in url_parse.video_urls:
                    self.play_queue.append(p)
                    url_parse = YouTube(p)
                    self.title_queue.append(url_parse.title)

                if not self.bot.voice_clients[0].is_playing():
                    music = YouTube(self.play_queue[0])
                    title = music.title
                    try:
                        music.streams.filter().get_lowest_resolution().download(filename=f"{self.song_path}/{title}.mp3")
                    except:
                        for f in self.forbidden_char:
                            title = title.replace(f," ")
                        music.streams.filter().get_lowest_resolution().download(filename=f"{self.song_path}/{title}.mp3")
                    self.bot.voice_clients[0].play(discord.FFmpegOpusAudio(executable=self.ffmpeg_path, source=f"{self.song_path}/{title}.mp3"), after = lambda _ : self.after_song(self))
            else:
                if not self.bot.voice_clients[0].is_playing():
                    await ctx.send("我已經在語音頻道了呦")
                else:
                    url_parse = Playlist(url)
                    print(url_parse.video_urls)
                    for p in url_parse.video_urls:
                        self.play_queue.append(p)
                        url_parse = YouTube(p)
                        self.title_queue.append(url_parse.title)   

        elif url.startswith(self.play_prefix):
            if ctx.author.voice == None:
                await ctx.send('使用者還沒進入語音頻道呦')
            elif self.bot.voice_clients == []:
                voiceChannel = ctx.author.voice.channel
                await voiceChannel.connect()
                music = discord.Activity(type=discord.ActivityType.listening, name = 'Yotube的音樂')
                await self.bot.change_presence(activity=music, status=discord.Status.online)

                for file in os.scandir(self.song_path): #刪除之前的mp3檔案
                    if file.path[-4:] == '.mp3':
                        os.remove(file.path)
                if not self.bot.voice_clients[0].is_playing():
                    try:
                        music = YouTube(url)
                        self.play_queue.append(url)
                        self.title_queue.append(music.title)
                        print(self.play_queue)
                        title = music.title
                        music.streams.filter().get_lowest_resolution().download(filename=f"{self.song_path}/{title}.mp3")
                        self.bot.voice_clients[0].play(discord.FFmpegOpusAudio(executable=self.ffmpeg_path, source=f"{self.song_path}/{title}.mp3"), after = lambda _ : self.after_song(self))
                    except OSError as err:
                        for f in self.forbidden_char:
                            title = title.replace(f," ")
                        music.streams.filter().get_lowest_resolution().download(filename=f"{self.song_path}/{title}.mp3")
                        self.bot.voice_clients[0].play(discord.FFmpegOpusAudio(executable=self.ffmpeg_path, source=f"{self.song_path}/{title}.mp3"), after = lambda _ : self.after_song(self))
                    except:
                        await ctx.send("找不到歌曲!")
            else:
                if not self.bot.voice_clients[0].is_playing():
                    await ctx.send("我已經在語音頻道了呦, 目前狀態為閒置狀態")
                else:
                    try:
                        music = YouTube(url)
                        self.play_queue.append(url)
                        self.title_queue.append(music.title)
                    except:
                        await ctx.send("找不到歌曲!")

        else:
            await ctx.send("找不到歌曲!")

    def after_song(self, ctx):
        self.play_queue.pop(0)
        self.title_queue.pop(0)
        try:
            for file in os.scandir(self.song_path):
                if file.path[-4:] == ".mp3":
                    os.remove(file.path)
        except:
            pass
        if self.play_queue != []:
            music = YouTube(self.play_queue[0])
            title = music.title
            try:
                music.streams.filter().get_lowest_resolution().download(filename=f"{self.song_path}/{title}.mp3")
            except:
                for f in self.forbidden_char:
                    title = title.replace(f," ")
                music.streams.filter().get_lowest_resolution().download(filename=f"{self.song_path}/{title}.mp3")
            self.bot.voice_clients[0].play(discord.FFmpegOpusAudio(executable=self.ffmpeg_path, source=f"{self.song_path}/{title}.mp3"), after = lambda _ : self.after_song(self))
    
class MusicOperate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pause(self, ctx):
        if self.bot.voice_clients[0].is_playing():
            self.bot.voice_clients[0].pause()
            await ctx.send('歌曲已暫停')
        else:
            await ctx.send('沒有歌曲正在播放呦')

    @commands.command()
    async def resume(self, ctx):
        if self.bot.voice_clients[0].is_paused():
            self.bot.voice_clients[0].resume()
            await ctx.send('歌曲已繼續播放')
        else:
            await ctx.send('沒有歌曲正在暫停呦')

async def setup(bot):
    await bot.add_cog(YoutubePlay(bot))
    await bot.add_cog(MusicOperate(bot))