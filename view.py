import discord
import random

waiting_list = {}

image_urls = [
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltcd4b2978c3289d76/6520b45996bebf0759a06656/101023_Prestige_Coven_Akali_Splash.jpg",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blte2aba634714a9979/6520b459705ef310da48bbb1/101023_Coven_Akali_Splash.jpg",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltaa71585244693dee/64d2da9f7c819b73a170c1f8/Immortal-Journey-Kayle---Final.jpg?disposition=inline",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt01c9dd64d8aa9c9e/64d2daac0bea57385cf1b3a3/Immortal-Journey-Sona---Final.jpg?disposition=inline",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt244a2948351b09ba/64d2da9f0a8e9920a20e87a2/Immortal-Journey-Soraka---Final.jpg?disposition=inline",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt939d51f2813d3802/64c31a49332559f11a19119a/Soul-Fighter-Gwen--Final.jpg",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt75a65c6f4b4ee2d2/647117b63f34da11bf7b571f/DRX-Worlds-Winners-2022.jpg",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt1d186491a32f5edb/645c2455562ac16e655fafce/Snow-Moon-Morgana---Final.jpg?disposition=inline",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt32882fcfacca8cd5/644b33c7df452f0942b2da4b/050223_Inkshadow_KaiSa_Splash.jpg",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltc364818b728665d1/648279b474d5017909013d98/061323_Shan_Hai_Scrolls_Lillia_Splash.jpg",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt7addfd4f52aa4a74/63cf0f53bf2b513f9caf87ac/Lunar-Empress-Ashe---Final.jpg",
        "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt2e3b3de50988e224/62ec856ece66ad7665f83872/MonsterTamer_LuluandKogmaw_Final.jpg",
    ]

# Create a view with buttons for users to indicate if they're joining or declining an invite.
class ReadyOrNotView(discord.ui.View):
    
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)   # Call the parent class's __init__ method
        self.joined_users = []
        self.quit_user = []
        self.initiatior = None  # The user who started the invite
        self.game = {}
        self.gamemode = None
        self.rank = None
        self.players = 0  # Number of players the initiator is looking for
        self.chosen_url = random.choice(image_urls)

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
            desc = f"{self.initiatior.display_name} is looking for {self.rank} players, need {self.players} "
        else:
            desc = "Initiator is unknown."
        embed = discord.Embed(title="Let's get together", description=desc)
        embed.set_image(url=self.chosen_url)
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
        # if self.check_players():
        #         self.disable_buttons()
        embed = self.create_embed()
        await self.message.edit(view=self, embed=embed)

    # Button interaction for joining
    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.initiatior:
            button.disabled = True           
        await interaction.response.defer()
        if interaction.user.display_name not in self.joined_users:
            self.joined_users.append(interaction.user.display_name)
        for user_id in [self.initiatior.id, interaction.user.id]:
            if user_id not in waiting_list:
                waiting_list[user_id] = []
        if interaction.user not in waiting_list[self.initiatior.id]:
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
 