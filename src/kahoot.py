import discord
from discord.ext import commands

from .views import CategorySelect

class Kahoot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Start a Kahoot game.")
    async def kahoot(self, ctx):
        view = CategorySelect(ctx.author, ctx.channel)
        view.message = await ctx.respond(f"**New Kahoot session by {ctx.author.name} in <#{ctx.channel.id}>**\n*Select a category.*", view=view)


def setup(bot):
    bot.add_cog(Kahoot(bot))