import discord
from discord import app_commands


class Search:
    message_history = []

    def __init__(self):
        pass

    def searchbyname(self, location='na', player_name=None):
        opggurl = "https://www.op.gg/summoners/" + \
            location+"/" + player_name.replace(" ", "%20")
        return opggurl

    def register_commands(self, bot):
        @bot.tree.command(name="search")
        @app_commands.describe(location="Server Location")
        @app_commands.choices(location=[
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
        async def search(interaction: discord.Interaction, opgg_name: str, location: app_commands.Choice[str]):
            opgglink = self.searchbyname(location.value, opgg_name)
            await interaction.response.send_message(f'{opgg_name} : OPGG in game profile link  {opgglink}')

        @app_commands.describe(location="Server Location")
        @app_commands.choices(location=[
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
        @bot.tree.command(name="multisearch")
        async def multisearch(interaction: discord.Interaction, location: app_commands.Choice[str], 
                            player1: str, player2: str = None, player3: str = None, 
                            player4: str = None, player5: str = None):
            
            players = [player1, player2, player3, player4, player5]
            
            # Manually handle URL encoding for common characters (e.g., space becomes %20)
            encoded_players = []
            for p in players:
                if p:
                    encoded_players.append(p.replace(" ", "%20"))
                    
            opgglink = f'https://www.op.gg/multisearch/{location.value}?summoners={"%2C".join(encoded_players)}'
            await interaction.response.send_message(f'Multi-Search OPGG link: {opgglink}')


