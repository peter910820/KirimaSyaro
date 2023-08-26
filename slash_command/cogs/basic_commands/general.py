import discord, os
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name= "id", description="check user id.")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Your user name:{interaction.user.id}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot), guild= None)