import discord

# Create a view with buttons for users to indicate if they're joining or declining an invite.
class ReadyOrNotView(discord.ui.View):
    
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)   # Call the parent class's __init__ method
        self.joined_users = []
        self.declined_users = []
        self.initiatior = None  # The user who started the invite
        self.players = 0  # Number of players the initiator is looking for

    # Function to send an initial message (or embed) with this view
    async def send(self, interaction: discord.Interaction):
        embed = self.create_embed()
        await interaction.response.send_message(view=self, embed=embed)
        self.message = await interaction.original_response()

    # Utility function to convert a list of users into a string for display. If no users, a default string is returned.
    def convert_user_list_to_str(self, user_list, default_str=""):
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

    # def Create_Post(self,title,description):
           
    def check_players(self):
        if len(self.joined_users) >= self.players:
            return True
        else:
            return False

    def disable_buttons(self):
        self.join_button.disabled = True
        self.decline_button.disabled = True

    # Update the message with the current state of who joined and declined
    async def update_message(self):
        if self.check_players():
                self.disable_buttons()
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