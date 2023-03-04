import discord
import os, re
from pytube import YouTube, Playlist

yt = YouTube('https://music.youtube.com/watch?v=M2cckDmNLMI&list=RDCLAK5uy_mRcc2Y3l-RoZsDt27qu8CBGpKt-5w7v8g')
print('download...')
yt.streams.filter().get_audio_only().download(filename='b.mp3')