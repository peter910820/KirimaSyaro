import discord
from discord import app_commands
from discord.ext import commands

class GeneralOperation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name= "test", description="testing bot delay")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"delay time: {str(round(self.bot.latency*1000, 2))}ms.")  

    @app_commands.command(name= "join", description= "🌟加入語音頻道🌟")
    async def join(self, interaction: discord.Interaction) -> None:
        if interaction.user.voice == None:
            await interaction.response.send_message("未加入頻道")
        elif self.bot.voice_clients == []:
            voiceChannel = interaction.user.voice.channel
            await voiceChannel.connect()
        else:
            await interaction.response.send_message("已加入頻道")

    @app_commands.command(name= "leave", description= "🌟離開語音頻道🌟")
    async def leave(self, interaction: discord.Interaction) -> None:
        if self.bot.voice_clients != []:
            await self.bot.voice_clients[0].disconnect()
            self.play_queue = []
            await self.bot.change_presence(activity = discord.Game("ブルーアーカイブ -Blue Archive-"), status=discord.Status.online)
            await interaction.response.send_message("已離開頻道❌")
        else:
            await interaction.response.send_message("目前沒有在任何頻道❌")


async def setup(bot):
    await bot.add_cog(GeneralOperation(bot))