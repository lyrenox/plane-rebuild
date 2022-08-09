from random import randint

import discord
from discord import option, Embed
from discord.ext import commands

from .views import Highlow


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Pick a random number.")
    @option('end', int, description="The maximum number to choose from.")
    @option('start', int, description="Starting number to choose from. Default: 1", required=False, default=1)
    @option('count', int, description="Number of times to pick the number. Default: 1", required=False, default=1)
    async def pick(self, ctx, end, start, count):
        if count != 1:
            outcome = [(randint(start, end)) for i in range(count)]
            total = sum(outcome)
            outcome = [str(x) for x in outcome]
            await ctx.respond(f"**{ctx.author.display_name}** picked {', '.join(outcome[:-1])} and {outcome[-1]}. That adds up to a total of **{total}**!")
        else:
            outcome = randint(start, end)
            await ctx.respond(f"**{ctx.author.display_name}** picked **{outcome}**")

    @discord.slash_command(description="Play a game of highlow.")
    async def highlow(self, ctx):
        hint = randint(1, 100)
        number = randint(1, 100)
        view = Highlow(author_id=ctx.author.id, hint=hint, number=number)
        view.message = await ctx.respond(f"**{ctx.author.display_name}**, I have chosen a number between 1 and 100.\nIs the number higher or lower than **{hint}**?", view=view)


def setup(bot):
    bot.add_cog(Fun(bot)) 