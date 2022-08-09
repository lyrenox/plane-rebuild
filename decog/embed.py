import discord
from discord.ext import commands
from discord import Embed
from discord.ui import View


class EditView(View):
    def __init__(self, author_id):
        super().__init__(timeout=10)
        self.author_id = author_id

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("It's not your menu.", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit_original_message(view=self)

    @discord.ui.select(
        placeholder = "Select an action...", 
        min_values = 1, 
        max_values = 1, 
        options = [
            discord.SelectOption(label="Edit Author"),
            discord.SelectOption(label="Edit Thumbnail"),
            discord.SelectOption(label="Edit Title and Description"),
            discord.SelectOption(label="Edit Fields"),
            discord.SelectOption(label="Edit Image"),
            discord.SelectOption(label="Edit Footer and Timestamp")
        ]
    )
    async def select_callback(self, select, interaction): 
        await interaction.response.send_message(f"You selected **{select.values[0]}**. This does not work yet lol", ephemeral=True)


    @discord.ui.button(label="All Done!", style=discord.ButtonStyle.success) 
    async def confirm_callback(self, button, interaction):
        await interaction.response.send_message("Not sent. This is just a test lol", ephemeral=True)

    @discord.ui.button(label="Abort", style=discord.ButtonStyle.danger)
    async def cancel_callback(self, button, interaction):
        await interaction.response.send_message("Not aborted. This is just a test lol", ephemeral=True)


class AdvEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="An advanced menu for you to create better looking embeds.")
    async def advanced_embed(self, ctx):
        view = EditView(author_id=ctx.author.id)
        view.message = await ctx.respond(embed=Embed(title="Not set", description="Not set"), view=view)


def setup(bot):
    bot.add_cog(AdvEmbed(bot))    

