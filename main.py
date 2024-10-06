import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class SyaroBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix = "\\",
            intents = intents
        )

    async def on_ready(self):
        print(f'{bot.user} is online.')
        # print('logging in as {0.user}'.format(bot))
        print(f'delay time: {str(round(bot.latency*1000, 2))}ms.')
        game = discord.Game("ブルーアーカイブ -Blue Archive-") # status
        await bot.change_presence(status=discord.Status.online, activity=game) # change status to game

    async def on_command_error(ctx, error):
        print(error)

    async def on_voice_state_update(self, member, before, after):
        # 當使用者開始講話（綠燈亮起）
        if after.self_mute is False and after.self_deaf is False and before.self_mute is True:
            await member.send(f"{member.guild.name}正在講話")
            print(f"{member.name} is now talking!")
        
        # 當使用者停止講話（綠燈熄滅）
        elif after.self_mute is True and before.self_mute is False:
            print(f"{member.name}不講話了")

    async def ping(ctx):
        await ctx.send(f'延遲時間為: {str(round(bot.latency*1000, 2))}ms')

    async def exit(ctx):
        await ctx.send(f'正在關閉機器人...')
        await bot.close()

    async def setup_hook(self):
        await bot.load_extension('cogs.general_operation')
        # await bot.load_extension('cogs.youtube_play')
        await bot.tree.sync(guild = None)

bot = SyaroBot()
bot.run(os.getenv("TOKEN"))