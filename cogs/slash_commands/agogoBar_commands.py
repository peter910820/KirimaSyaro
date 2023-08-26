import discord, os, asyncio
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

class AgogoBarCommands():
    def __init__(self, tree):
        self.tree = tree
        self.agogoBar_ID = 751068627322798130

    @tree.command(name = "testtttt", description = "測試用", guild=discord.Object(agogoBar_ID))
    async def test_command(interaction):
        await interaction.response.send_message("吃我老二")