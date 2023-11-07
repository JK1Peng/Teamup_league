import asyncio
import discord
import sqlite3
from urllib.parse import quote
from discord import app_commands
from discord.ext import commands
from discord import Embed
from view import ReadyOrNotView
from view import waiting_list
from getrank import get_opgg_ranking

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
        # view.game = modes_list[gamemode.value]
        view.initiatior = interaction.user
        view.players = players.value
        view.rank = rank.name
        view.gamemode = gamemode.name
        # waiting_list.append(interaction.user)
        await view.send(interaction)

    @bot.tree.command(name='table', description="return table")
    async def send_table(interaction: discord.Interaction):
        # 创建嵌入对象
        embed = discord.Embed(title="Pending member list", color=0x3498db)

        # 检查用户是否在等待列表中
        if interaction.user.id in waiting_list:
            # 连接到数据库
            conn = sqlite3.connect('bindings.db')
            cursor = conn.cursor()

            for i in waiting_list[interaction.user.id]:
                # 获取玩家的所有游戏ID和地区
                cursor.execute("SELECT game_id, region FROM user_bindings WHERE dc_id=?", (i.id,))
                rows = cursor.fetchall()

                # 如果数据库中没有找到条目，添加一个占位信息
                if not rows:
                    embed.add_field(name=i.name, value="No game IDs found.", inline=False)
                    continue

                game_info = ""
                for game_id, region in rows:
                    opgg_link = f"https://{region}.op.gg/summoner/userName={game_id}"
                    # solorank = {get_opgg_ranking(game_id,region)}
                    game_info += f"In-Game Name: {game_id}\nOPGG Link: [Click Here]({opgg_link})\n\n"

                # 添加一个包含所有游戏信息的字段
                embed.add_field(name=i.name, value=game_info.strip(), inline=False)
            
            conn.close()
        else:
            # 如果用户不在等待列表中，发送一个信息
            embed.description = "You are not on the waiting list."

        # 发送嵌入消息给用户
        await interaction.user.send(embed=embed)
        await interaction.response.send_message('I have sent you a table in DM!', ephemeral=True)
