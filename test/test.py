from pytube import YouTube, Playlist
playlist = []
yt_playlist = "https://www.youtube.com/watch?v=NarVowwWS_Q&list=PLM0jRdHj2C1kHn3wfjLhvEmYyAM8erI7B&index=14"
a = YouTube(yt_playlist)
a.streams.filter().get_lowest_resolution().download(filename=f"O:/Myproject/syaroBot/music_tmp/{a.title}.mp3")