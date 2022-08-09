import discord
from discord import Embed

class Highlow(discord.ui.View):
    def __init__(self, author_id, hint, number):
        super().__init__(timeout=20)
        self.author_id = author_id
        self.hint = hint
        self.number = number

        if self.number < self.hint:
            self.outcome = 'lower'
        if self.number == self.hint:
            self.outcome = 'jackpot'
        if self.number > self.hint:
            self.outcome = 'higher'

        self.win = f"**You won! :tada:** Your hint was {self.hint}. The number was {self.number}."
        self.loss = f"**You lost...** Your hint was {self.hint}. The number was {self.number}."
        self.jackpot = f"**JACKPOT! :fireworks:** Your hint was {self.hint}. The number was {self.number}."

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if isinstance(self.message, discord.message.Message):
            await self.message.edit(embed=Embed(description="You took too long.", color=0xed4245), view=self)
        elif isinstance(self.message, discord.interactions.Interaction):
            await self.message.edit_original_message(embed=Embed(description="You took too long.", color=0xed4245), view=self)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("It's not your menu.", ephemeral=True)
            return False
        else:
            return True

    @discord.ui.button(label="Lower", style=discord.ButtonStyle.primary)
    async def lower_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True
            child.style = discord.ButtonStyle.secondary
        if self.outcome == 'lower':
            button.style = discord.ButtonStyle.success
            result = self.win
        else:
            button.style = discord.ButtonStyle.danger
            result = self.loss
        await interaction.response.edit_message(content=result, view=self)
        self.stop()

    @discord.ui.button(label="JACKPOT!", style=discord.ButtonStyle.primary)
    async def jackpot_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True
            child.style = discord.ButtonStyle.secondary
        if self.outcome == 'jackpot':
            button.style = discord.ButtonStyle.success
            result = self.win
        else:
            button.style = discord.ButtonStyle.danger
            result = self.loss
        await interaction.response.edit_message(content=result, view=self)
        self.stop()

    @discord.ui.button(label="Higher", style=discord.ButtonStyle.primary)
    async def higher_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True
            child.style = discord.ButtonStyle.secondary
        if self.outcome == 'higher':
            button.style = discord.ButtonStyle.success
            result = self.win
        else:
            button.style = discord.ButtonStyle.danger
            result = self.loss
        await interaction.response.edit_message(content=result, view=self)
        self.stop()