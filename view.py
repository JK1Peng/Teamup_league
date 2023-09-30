import discord


waiting_list = {}



# Create a view with buttons for users to indicate if they're joining or declining an invite.
class ReadyOrNotView(discord.ui.View):
    
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)   # Call the parent class's __init__ method
        self.joined_users = []
        self.quit_user = []
        self.initiatior = None  # The user who started the invite
        self.game = {}
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
            desc = f"{self.initiatior.display_name} is looking for another {self.players} players"
        else:
            desc = "Initiator is unknown."
        embed = discord.Embed(title="Let's get together", description=desc)

        # if self.game['url']:
        #     embed.set_image(url=self.game['url'])

        embed.add_field(inline=True, name="(°ロ°)☝come", value=self.convert_user_list_to_str(self.joined_users))
        return embed

    # def Create_Post(self,title,description):
           
    def check_players(self):
        if len(self.joined_users) >= self.players:
            return True
        else:
            return False

    def disable_buttons(self):
        self.join_button.disabled = True
        self.Quit_button.disabled = True#write by yuba

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
        for user_id in [self.initiatior.id, interaction.user.id]:
            if user_id not in waiting_list:
                waiting_list[user_id] = []
        waiting_list[self.initiatior.id].append(interaction.user)
        await self.update_message()

    # Button interaction for quit，write by yubao
    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def Quit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)
            
        if (self.initiatior.id in waiting_list) and (interaction.user in waiting_list[self.initiatior.id]):
            waiting_list[self.initiatior.id].remove(interaction.user)    
        await self.update_message()
 