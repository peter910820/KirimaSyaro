import discord, os
from discord import app_commands
from discord.ext import commands

class YoutubePlayer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name= "test", description="你覺得他會回你甚麼?")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Your user name:{interaction.user}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YoutubePlayer(bot), guild= None)