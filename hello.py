import discord
from discord import app_commands

class baseOpr:
    def __init__(self) -> None:
        pass
    
    def register_commands(bot):
        @bot.tree.command(name="hello")
        async def hello(interaction: discord.Interaction):
            await interaction.response.send_message(f'Hey {interaction.user.mention}! This is a slash command')
    
    
    
    



