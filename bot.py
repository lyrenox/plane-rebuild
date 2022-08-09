import os
from dotenv import load_dotenv

import discord
from discord import Embed, slash_command
from discord.ui import View, Button

load_dotenv()


class Latios(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=discord.Intents(messages=True), *args, **kwargs)
        self.owners = [717408952035573767]
        self.token = os.getenv('BETA_TOKEN')
        self.colourBlue = 0x4287f5

        for cog in ['src.main', 'src.fun', 'decog.test', 'src.kahoot']:
            try:
                self.load_extension(cog)
                print(f"Loaded {cog}")
            except Exception as e:
                print(f"Failed to load {cog}: {e}")
            
      
    async def on_ready(self):
        print(f"Connected as {self.user} (ID: {self.user.id})\n" + "--- "*10)


    def run(self):
        super().run(self.token)


if __name__ == '__main__':
    bot = Latios()
    bot.run()