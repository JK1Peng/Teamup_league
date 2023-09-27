# Necessary imports
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

# Create a view with buttons for users to indicate if they're joining or declining an invite.
class ReadyOrNotView(discord.ui.View):
    
    # Lists to track users who joined or declined the invite
    joined_users = []
    declined_users = []
    initiatior: discord.User = None  # The user who started the invite
    players: int = 0  # Number of players the initiator is looking for

    # Function to send an initial message (or embed) with this view
    async def send(self, interaction: discord.Interaction):
        embed = self.create_embed()
        await interaction.response.send_message(view=self, embed=embed)
        self.message = await interaction.original_response()

    # Utility function to convert a list of users into a string for display. If no users, a default string is returned.
    def convert_user_list_to_str(self, user_list, default_str="No one"):
        if len(user_list):
            return "\n".join(user_list)
        return default_str
    
    # Create an embed that shows who initiated the invite, who joined, and who declined.
    def create_embed(self):
        if self.initiatior:
            desc = f"{self.initiatior.display_name} is looking for another {self.players - 1} players"
        else:
            desc = "Initiator is unknown."
        embed = discord.Embed(title="Let's get together", description=desc)
        embed.add_field(inline=True, name="(°ロ°)☝come", value=self.convert_user_list_to_str(self.joined_users))
        embed.add_field(inline=True, name="❌Declined", value=self.convert_user_list_to_str(self.declined_users))
        return embed

    # Update the message with the current state of who joined and declined
    async def update_message(self):
        embed = self.create_embed()
        await self.message.edit(view=self, embed=embed)

    # Button interaction for joining
    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.display_name not in self.joined_users:
            self.joined_users.append(interaction.user.display_name)
        if interaction.user.display_name in self.declined_users:
            self.declined_users.remove(interaction.user.display_name)
        await self.update_message()

    # Button interaction for declining
    @discord.ui.button(label="Declined", style=discord.ButtonStyle.red)
    async def decline_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.display_name not in self.declined_users:
            self.declined_users.append(interaction.user.display_name)
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)
        await self.update_message()

# Set up the bot with the necessary command prefix and intents
bot = commands.Bot(command_prefix="ms!", intents=discord.Intents.all())

# This function starts the bot
def run_discord_bot():
    TOKEN = 'Your-Token-Here' 

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

    # Slash command to start the "team up" interaction
    @bot.tree.command(name="teamup")
    async def hello(interaction: discord.Interaction, players: int):
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
