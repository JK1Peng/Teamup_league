# Necessary imports
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from view import ReadyOrNotView

# Set up the bot with the necessary command prefix and intents
bot = commands.Bot(command_prefix="ms!", intents=discord.Intents.all())

# This function starts the bot
def run_discord_bot():
    TOKEN = 'MTE0OTA1NTEyMjM4MzU2OTAwNg.GaWQ2_.nMq6mksiCh_AN-aFXXSV4RxaZd_pFZe1chtE_E' 

    # Event that runs when the bot is ready
    @bot.event
    async def on_ready():
        print("discord bot is ready!")
        try:
            synced = await bot.tree.sync()  # Sync commands with Discord API
            print(f'Synced {len(synced)} commands')
        except Exception as e:
            print(e)

    # Slash command example
    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f'Hey {interaction.user.mention}! This is a slash command')

    @app_commands.describe(gamemode="The mode you want to choose")
    @app_commands.choices(gamemode =[
        app_commands.Choice(name = "Normal",value = "normal"),
        app_commands.Choice(name = "Solo/duo",value = "solo"),
        app_commands.Choice(name = "Flex",value = "flex"),
        app_commands.Choice(name = "Aram",value = "aram"),
        app_commands.Choice(name = "Custom",value = "custom")
    ])

    @app_commands.describe(rank="What rank you want to play with")
    @app_commands.choices(rank =[
        app_commands.Choice(name = "Iron",value = "iron"),
        app_commands.Choice(name = "Silver",value = "silver"),
        app_commands.Choice(name = "Gold",value = "gold"),
        app_commands.Choice(name = "Plat",value = "plat"),
        app_commands.Choice(name = "Emerald",value = "emerald"),
        app_commands.Choice(name = "Diamond",value = "diamond"),
        app_commands.Choice(name = "Master",value = "master"),
        app_commands.Choice(name = "Iron/Silver",value = "ironS"),
        app_commands.Choice(name = "Silver/Gold",value = "silverG"),
        app_commands.Choice(name = "Gold/Plat",value = "goldP"),
        app_commands.Choice(name = "Plat/Emerald",value = "platE"),
        app_commands.Choice(name = "Emerald/Diamond",value = "emeraldD"),
        app_commands.Choice(name = "Diamond/Master",value = "diamondM"),
        
    ])


    
    # Slash command to start the "team up" interaction
    @bot.tree.command(name="teamup",description="place to team up!")
    async def hello(interaction: discord.Interaction, gamemode: app_commands.Choice[str],rank:app_commands.Choice[str],players: int):
        view = ReadyOrNotView(timeout=None)
        view.initiatior = interaction.user
        view.players = players
        await view.send(interaction)

    # Basic command examples
    @bot.command()
    async def help1(ctx):
        await ctx.send("this is a help command")

    @bot.command()
    async def panel(ctx):
        embed = discord.Embed(
            title="Panel Title",
            description="This is a panel",
            color=discord.Color.blue()
        )
        embed.add_field(name="Field1", value="React with :one:", inline=False)
        embed.add_field(name="Field2", value="React with :two:", inline=False)
        message = await ctx.send(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")

        # Check to see which reaction the user selects
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣"]

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's up!")
        else:
            if str(reaction.emoji) == "1️⃣":
                await ctx.send("You chose option 1!")
            elif str(reaction.emoji) == "2️⃣":
                await ctx.send("You chose option 2!")

    bot.run(TOKEN)
