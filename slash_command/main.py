import discord, os, asyncio
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

agogoBar_ID = 751068627322798130
@tree.command(name = "test", description = "哈哈你試試看", guild=None)
async def test_command(interaction):
    await interaction.response.send_message("吃我雞雞")

@tree.command(name= "join", description= "join into voice channel.", guild= None)
async def join(interaction):
    if interaction.user.voice == None:
        await interaction.response.send_message("未加入頻道")
    elif client.voice_clients == []:
            voiceChannel = interaction.user.voice.channel
            await voiceChannel.connect()
            music = discord.Activity(type=discord.ActivityType.listening, name = "Yotube的音樂")
            await client.change_presence(activity=music, status=discord.Status.online)
    else:
        await interaction.response.send_message("已加入頻道")

@tree.command(name= "leave", description= "leave voice channel.", guild= None)
async def leave(interaction):
    if client.voice_clients != []:
        await client.voice_clients[0].disconnect()
        game = discord.Game("ブルーアーカイブ -Blue Archive-") # status
        await client.change_presence(status=discord.Status.online, activity=game)
        # play_queue = []
    else:
        await interaction.response.send_message("未加入頻道")


@tree.command(name= "voice", description= "voice channel test", guild= None)
async def join(interaction):
    await interaction.response.send_message(f"您所在的語音頻道名稱為: {interaction.user.voice.channel.name}\n您所在的語音頻道ID為: {interaction.user.voice.channel.id}")

@tree.command(name= "information", description= "看看所有interaction資料", guild= discord.Object(id=agogoBar_ID))
async def join(interaction):
    await interaction.response.send_message(interaction.data)


@client.event
async def on_ready():
    await tree.sync(guild=None)
    print(f'{client.user} is online.')
    # print('logging in as {0.user}'.format(bot))
    print(f'delay time: {str(round(client.latency*1000, 2))}ms.')
    game = discord.Game("ブルーアーカイブ -Blue Archive-") # status
    await client.change_presence(status=discord.Status.online, activity=game) # change status to game

client.run(os.getenv('TOKEN'))

# async def main():
#     await client.start(os.getenv('TOKEN'))

# asyncio.run(main())