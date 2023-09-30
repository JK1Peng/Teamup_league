# Necessary imports
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from view import ReadyOrNotView
import hello , matching
from search import Search


# Set up the bot with the necessary command prefix and intents
bot = commands.Bot(command_prefix="ms!", intents=discord.Intents.all())

message_history = []


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

    # hello.register_commands(bot)
    matching.register_commands(bot)
    srch = Search()
    srch.register_commands(bot)



    @bot.tree.command(name="edit")
    #1156679737482154117
    #1157462800717852812
    async def edit(interaction: discord.Interaction):
        # Sending the initial response
        await interaction.response.send_message(f'Hey {interaction.user.mention}! This is a slash command')
        # Fetching the response message
        response_msg = await interaction.original_response()
        
        # Editing the response message
        await response_msg.edit(content="This is the edited content!")

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
