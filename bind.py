import discord
from discord import app_commands
import sqlite3
from urllib.parse import quote

class Bind:
    def __init__(self) -> None:
        self.setup_database()

    def setup_database(self):
        self.conn = sqlite3.connect('bindings.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_bindings (
            dc_id INTEGER,
            game_id TEXT,
            region TEXT,
            PRIMARY KEY (dc_id, game_id)
        )
        ''')
        self.conn.commit()

    def register_commands(self, bot):
        
        # 假设你有以下的游戏列表：
        games = ["League of Legends", "Dota 2", "Valorant"]

        # 转化为Choice对象的列表：
        choices = [app_commands.Choice(name=game, value=game) for game in games]

        # 当注册命令时使用这些choices：
        @bot.tree.command(name="select_game", description="Select your favorite game")
        @app_commands.choices(game=choices)
        async def select_game(interaction: discord.Interaction, game: app_commands.Choice[str]):
            await interaction.response.send_message(f'You selected {game.name}!')
      

        @app_commands.describe(region="Server Location")
        @app_commands.choices(region=[
            app_commands.Choice(name="NA", value="na"),
            app_commands.Choice(name="EUW", value="euw"),
            app_commands.Choice(name="EUNE", value="eune"),
            app_commands.Choice(name="OCE", value="oce"),
            app_commands.Choice(name="KR", value="kr"),
            app_commands.Choice(name="JP", value="jp"),
            app_commands.Choice(name="BR", value="br"),
            app_commands.Choice(name="LAS", value="las"),
            app_commands.Choice(name="LAN", value="lan"),
            app_commands.Choice(name="RU", value="ru"),
            app_commands.Choice(name="TW", value="tw")
        ])
        @bot.tree.command(name="bind", description="Bind your DC ID with a Game ID")
        async def bind(interaction: discord.Interaction, game_id: str, region: app_commands.Choice[str]):
            normalized_game_id = game_id.replace(" ", "").lower()
            # 检查用户已经绑定了多少个游戏ID
            self.cursor.execute("SELECT COUNT(*) FROM user_bindings WHERE dc_id = ?", (interaction.user.id,))
            (number_of_bindings,) = self.cursor.fetchone()

            # 如果用户已经有两个绑定，则阻止他们添加新的绑定
            if number_of_bindings >= 2:
                await interaction.response.send_message(f'{interaction.user.mention}, you can only bind up to 2 game IDs.', ephemeral=True)
                return

            # 检查是否已存在相同的游戏ID绑定
            self.cursor.execute("SELECT game_id FROM user_bindings WHERE dc_id = ? AND game_id = ?", (interaction.user.id, normalized_game_id))
            row = self.cursor.fetchone()
            if row:
                await interaction.response.send_message(f'{interaction.user.mention}, you have already bound the game ID {game_id} in region {region.name}.', ephemeral=True)
                return

            # 插入新的绑定
            self.cursor.execute("INSERT INTO user_bindings (dc_id, game_id, region) VALUES (?, ?, ?)", (interaction.user.id, normalized_game_id, region.name))
            self.conn.commit()

            await interaction.response.send_message(f'Successfully bound {interaction.user.mention} to game ID {game_id} in region {region.name}!')


        @bot.tree.command(name="unbind", description="Unbind a specific Game ID")
        async def unbind(interaction: discord.Interaction, game_id: str):
            # Check if the game_id exists for the user
            normalized_game_id = game_id.replace(" ", "").lower()
            self.cursor.execute("SELECT game_id FROM user_bindings WHERE dc_id = ? AND game_id = ?", (interaction.user.id, normalized_game_id))
            row = self.cursor.fetchone()
            if row:
                # Delete the game_id since it exists
                self.cursor.execute("DELETE FROM user_bindings WHERE dc_id = ? AND game_id = ?", (interaction.user.id, game_id))
                self.conn.commit()
                await interaction.response.send_message(f'Successfully unbound {interaction.user.mention} from game ID {game_id}!')
            else:
                await interaction.response.send_message(f'{interaction.user.mention}, you do not have a binding with game ID {game_id}.')


        @bot.tree.command(name="get_binding", description="Get your Game IDs binding")
        async def get_binding(interaction: discord.Interaction):
            self.cursor.execute("SELECT game_id, region FROM user_bindings WHERE dc_id=?", (interaction.user.id,))
            rows = self.cursor.fetchall()
            
            if not rows:
                await interaction.response.send_message(f'{interaction.user.name} has no game ID bound.')
                return

            # 创建一个Embeds
            embed = discord.Embed(
                title=f"Bindings for {interaction.user.name}", 
                description="Here are your game IDs and their respective regions.",
                color=discord.Color.blue()  # 这里设置Embeds的颜色，你可以更换为你想要的颜色。
            )


            for row in rows:
                game_id, region = row
                game_id_encoded = quote(game_id)
                opgg_link = f"https://{region}.op.gg/summoner/userName={game_id_encoded}"
                embed.add_field(
                    name=f"Game ID: {game_id}",
                    value=f"Region: {region} | [OPGG link]({opgg_link})",
                    inline=False  # 设为False意味着每个字段都会从新的一行开始
                )
            
            await interaction.response.send_message(embed=embed)
        
        
    def close(self):
        self.conn.close()
