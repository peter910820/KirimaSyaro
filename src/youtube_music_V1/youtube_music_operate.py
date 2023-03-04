async def pause_music(message, client):
    if client.voice_clients[0].is_playing():
        client.voice_clients[0].pause()
        await message.channel.send('歌曲已暫停')
    else:
        await message.channel.send('沒有歌曲正在播放呦')

async def resume_music(message, client):
    if client.voice_clients[0].is_paused():
        client.voice_clients[0].resume()
        await message.channel.send('歌曲已繼續播放')
    else:
        await message.channel.send('沒有歌曲正在暫停呦')
        
