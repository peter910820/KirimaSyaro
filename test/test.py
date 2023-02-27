import discord
import os, re
from pytube import YouTube,Playlist

playlistUrl,pl = [],[]
playlist = Playlist('https://www.youtube.com/watch?v=0Fk7ca1eSvc&list=PLegMSu_HyPZtoWPuoaObMF6iwRSkbBgeA&index=3')

if type(playlist) == "pytube.contrib.playlist.Playlist":
    print(type(playlist))