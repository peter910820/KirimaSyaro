import discord
from discord.ext import commands

class GeneralOperation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("GeneralOperation cog test success!")

async def setup(bot):
    await bot.add_cog(GeneralOperation(bot))