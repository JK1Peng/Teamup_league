import discord
import responses
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="ms!",intents= discord.Intents.all())

def run_discord_bot():
    TOKEN = 'MTE0OTA1NTEyMjM4MzU2OTAwNg.GaWQ2_.nMq6mksiCh_AN-aFXXSV4RxaZd_pFZe1chtE_E'
    @bot.event
    async def on_ready():
        print ("discord bot is ready!")
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} commands')
        except Exception as e:
            print(e)

    @bot.tree.command(name = "hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f'Hey {interaction.user.mention}! This is a slash command')

    @bot.tree.command(name = "teamup")
    async def hello(interaction: discord.Interaction,mode : str,rank : str,player_need : str,summoner_name : str):
        await interaction.response.send_message(f'Hey {interaction.user.name} needs,gamemode:{mode},rank{rank},{player_need},i am {summoner_name}')

    @bot.command()
    async def panel(ctx):
        embed = discord.Embed(
            title="Panel Title",
            description="This is a panel",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Field1", value="value1", inline=False)
        embed.add_field(name="Field2", value="value2", inline=False)
        
        await ctx.send(embed=embed)

    bot.run(TOKEN)