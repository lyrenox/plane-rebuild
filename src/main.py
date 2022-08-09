import re
from random import choice, randint

import discord
from discord.ext import commands

from .views import Highlow


class Main(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith(f"<@{self.bot.user.id}>"):
            query = re.split(r' ', message.content.lower().replace(f'<@{self.bot.user.id}>', '').replace('\n', ' ').strip(' '))
            
            def keywords(keywords: list):
                for i in keywords:
                    if i in query:
                        index = query.index(i)
                        return True, index
                    else:
                        continue
                return False, None

            if keywords(["hi", "hello", "hey", "sup", "yo"])[0]:
                await message.channel.send(
                    choice([
                        f"Hello, {message.author.display_name}!",
                        f"Hey, {message.author.display_name}!",
                        f"Good day, {message.author.display_name}!",
                        f"Nice to meet you, {message.author.display_name}!",
                        "Hello!",
                        "Hi!",
                        f"Sup, {message.author.display_name}!"
                    ])
                )

            elif keywords(["choose", "pick"])[0]:
                def isnumeric(item):
                    return True if item.isnumeric() else False

                i = keywords(["choose", "pick"])[1]
                number = [int(x) for x in list(filter(isnumeric, query[i:]))]

                if len(number) > 2:
                    if number[2] != 1:
                        outcome = [(randint(number[0], number[1])) for i in range(number[2])]
                        total = sum(outcome)
                        outcome = [str(x) for x in outcome]
                        await message.channel.send(f"**{message.author.display_name}** picked {', '.join(outcome[:-1])} and {outcome[-1]}. That adds up to a total of **{total}**!")
                    else:
                        outcome = randint(number[0], number[1])
                        await message.channel.send(f"**{message.author.display_name}** picked **{outcome}** ({number[0]} - {number[1]})")
                else:
                    outcome = randint(number[0], number[1])
                    await message.channel.send(f"**{message.author.display_name}** picked **{outcome}** ({number[0]} - {number[1]})")

            elif keywords(["highlow"])[0]:
                hint = randint(1, 100)
                number = randint(1, 100)
                view = Highlow(author_id=message.author.id, hint=hint, number=number)
                view.message = await message.channel.send(f"**{message.author.display_name}**, I have chosen a number between 1 and 100.\nIs the number higher or lower than **{hint}**?", view=view) 



def setup(bot):
    bot.add_cog(Main(bot)) 
    