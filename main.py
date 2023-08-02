import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="\\", intents=intents) # \

@bot.event
async def on_ready():
    print(f'{bot.user} is online.')
    # print('logging in as {0.user}'.format(bot))
    print(f'delay time: {str(round(bot.latency*1000, 2))}ms.')
    game = discord.Game("ブルーアーカイブ -Blue Archive-") # status
    await bot.change_presence(status=discord.Status.online, activity=game) # change status to game

@bot.event
async def on_command_error(ctx, error):
    print(error)

@bot.command()
async def ping(ctx):
    await ctx.send(f'延遲時間為: {str(round(bot.latency*1000, 2))}ms')

@bot.command()
async def exit(ctx):
    await ctx.send(f'正在關閉機器人...')
    await bot.close()

async def main():
    await bot.load_extension('cogs.general_operation')
    await bot.load_extension('cogs.youtube_play')
    await bot.start(os.getenv('TOKEN'))

asyncio.run(main())