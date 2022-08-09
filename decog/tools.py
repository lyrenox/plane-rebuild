import os
from dotenv import load_dotenv

import discord
from discord import option, Embed
from discord.ext import commands
from discord.ui import Modal, InputText
from dateutil import parser


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Invite the bot to your server!")
    async def invite(self, ctx):
        await ctx.respond("[Invite](https://discord.com/api/oauth2/authorize?client_id=781705025582792704&permissions=274878253120&scope=bot%20applications.commands) **LatiOS** to your server!")


    @discord.slash_command(description="Creates a simple rich embed message.")
    @option('author_name', description="The author of the embed.", required=False, default=None)
    @option('author_icon', description="The link to the icon beside the author's name.", required=False, default=Embed.Empty)
    @option('author_url', description="The link when clicked on the author's name.", required=False, default=Embed.Empty)
    @option('channel', discord.TextChannel, description="The channel to send the embed.", required=False)
    @option('colour', description="The colour of the the embed. Must be a hex code.", required=False, default=None)
    @option('content', description="The text sent along with the embed. Must be 4000 characters or fewer.", required=False, default='')
    @option('description', description="The description of the embed. Must be 4096 characters or fewer.", required=False, default=Embed.Empty)
    @option('footer', description="The footer of the the embed.", required=False, default=None)
    @option('footer_icon', description="The link to the icon beside the footer.", required=False, default=Embed.Empty)
    @option('image', description="The link to the image at the bottom of the embed.", required=False, default=Embed.Empty)
    @option('thumbnail', description="The link to the thumbnail on the top right corner of the embed.", required=False, default=Embed.Empty)
    @option('timestamp', description="Sets a timestamp beside the footer.", required=False, default=None)
    @option('title', description="The title of the the embed. Must be 256 characters or fewer.", required=False, default=Embed.Empty)
    @option('url', description="The link when clicked on the title.", required=False, default=Embed.Empty)
    async def simple_embed(self, ctx, channel, content, title, url, description, colour, footer, footer_icon, timestamp, author_name, author_url, author_icon, thumbnail, image):
        if timestamp is not None:
            if timestamp.lower() == 'now':
                timestamp = discord.utils.now()
            else:
                try:
                    timestamp = parser.parse(timestamp)
                except:
                    timestamp = Embed.Empty
        else:
            timestamp = Embed.Empty

        embed = Embed(
            title = title,
            url = url,
            description = description,
            colour = int(colour.upper(), 16) if colour is not None else Embed.Empty,
            timestamp = timestamp
        )
        embed.set_image(url=image)
        embed.set_thumbnail(url=thumbnail)

        if footer is not None:
            embed.set_footer(text=footer, icon_url=footer_icon)
        if author_name is not None:
            embed.set_author(name=author_name, url=author_url, icon_url=author_icon)
        
        target = ctx.channel if channel is None else channel

        try:
            await target.send(content, embed=embed)
        except:
            await ctx.respond("Unable to send embed.\nCheck if at least one of `title`, `description`, `footer`, `author_name`, `thumbnail`, `image` is filled in.\nIf not, the bot may not have permissions to send in that channel.", ephemeral=True)
        else:
            await ctx.respond(f"Embed successfully sent to {target.mention}!", ephemeral=True)

def setup(bot):
    bot.add_cog(Tools(bot))