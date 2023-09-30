import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from view import ReadyOrNotView



modes_list = {
    "aram": {
        "url": "https://cdnb.artstation.com/p/assets/images/images/051/838/615/large/sam-snow-aramicon.jpg?1658300678"
    }
}



def format_as_table(headers, data):
    # Find the max width for each column
    widths = [max(len(str(val)) for val in col) for col in zip(headers, *data)]
    widths = [max(widths[i], len(headers[i])) for i in range(len(headers))]

    # Create a row formatter string
    row_format = "| " + \
        " | ".join(["{:>" + str(width) + "}" for width in widths]) + " |"

    # Build the table
    table = row_format.format(*headers)  # Header row
    table += "\n" + "|-" + \
        "-|".join(["-" * width for width in widths]) + "-|"  # Divider
    for row in data:
        table += "\n" + row_format.format(*row)

    return "```\n" + table + "\n```"  # Wrap the table in a code block


def register_commands(bot):
    @app_commands.describe(gamemode="The mode you want to choose")
    @app_commands.choices(gamemode=[
        app_commands.Choice(name="Normal", value="normal"),
        app_commands.Choice(name="Solo/duo", value="solo"),
        app_commands.Choice(name="Flex", value="flex"),
        app_commands.Choice(name="Aram", value="aram"),
        app_commands.Choice(name="Custom", value="custom")
    ])
    @app_commands.describe(rank="What rank you want to play with")
    @app_commands.choices(rank=[
        app_commands.Choice(name="Iron", value="iron"),
        app_commands.Choice(name="Silver", value="silver"),
        app_commands.Choice(name="Gold", value="gold"),
        app_commands.Choice(name="Plat", value="plat"),
        app_commands.Choice(name="Emerald", value="emerald"),
        app_commands.Choice(name="Diamond", value="diamond"),
        app_commands.Choice(name="Master", value="master"),
        app_commands.Choice(name="Iron/Silver", value="ironS"),
        app_commands.Choice(name="Silver/Gold", value="silverG"),
        app_commands.Choice(name="Gold/Plat", value="goldP"),
        app_commands.Choice(name="Plat/Emerald", value="platE"),
        app_commands.Choice(name="Emerald/Diamond", value="emeraldD"),
        app_commands.Choice(name="Diamond/Master", value="diamondM"),

    ])
    @app_commands.describe(players="how many team members you need")
    @app_commands.choices(players=[
        app_commands.Choice(name="1", value=1),
        app_commands.Choice(name="2", value=2),
        app_commands.Choice(name="3", value=3),
        app_commands.Choice(name="4", value=4)
    ])
    # Slash command to start the "team up" interaction
    @bot.tree.command(name="teamup", description="place to team up!")
    async def teamup(interaction: discord.Interaction, gamemode: app_commands.Choice[str], rank: app_commands.Choice[str], players: app_commands.Choice[int],):
        view = ReadyOrNotView(timeout=None)
        view.game = modes_list[gamemode.value]
        view.initiatior = interaction.user
        view.players = players.value
        await view.send(interaction)

    @bot.tree.command(name='table', description = "return table")
    async def send_table(interaction: discord.Interaction):
        headers = ["Player", "Age", "City"]
        data = [
            ["Alice", 30, "New York"],
            ["Bob", 25, "Los Angeles"],
            ["Charlie", 35, "Chicago"]
        ]
        table = format_as_table(headers, data)
        await interaction.response.send_message(f'{table}')





