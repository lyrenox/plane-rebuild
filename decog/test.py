import random

import discord
from discord.ext import commands
from discord.commands import option
from discord import Embed

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.POKEMON_LIST = ["MissingNo","Bulbasaur","Ivysaur","Venusaur","Charmander","Charmeleon","Charizard","Squirtle","Wartortle","Blastoise","Caterpie","Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto","Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu","Raichu","Sandshrew","Sandslash","Nidoran ♀","Nidorina","Nidoqueen","Nidoran ♂","Nidorino","Nidoking","Clefairy","Clefable","Vulpix","Ninetales","Jigglypuff","Wigglytuff","Zubat","Golbat","Oddish","Gloom","Vileplume","Paras","Parasect","Venonat","Venomoth","Diglett","Dugtrio","Meowth","Persian","Psyduck","Golduck","Mankey","Primeape","Growlithe","Arcanine","Poliwag","Poliwhirl","Poliwrath","Abra","Kadabra","Alakazam","Machop","Machoke","Machamp","Bellsprout","Weepinbell","Victreebel","Tentacool","Tentacruel","Geodude","Graveler","Golem","Ponyta","Rapidash","Slowpoke","Slowbro","Magnemite","Magneton","Farfetch'd","Doduo","Dodrio","Seel","Dewgong","Grimer","Muk","Shellder","Cloyster","Gastly","Haunter","Gengar","Onix","Drowzee","Hypno","Krabby","Kingler","Voltorb","Electrode","Exeggcute","Exeggutor","Cubone","Marowak","Hitmonlee","Hitmonchan","Lickitung","Koffing","Weezing","Rhyhorn","Rhydon","Chansey","Tangela","Kangaskhan","Horsea","Seadra","Goldeen","Seaking","Staryu","Starmie","Mr. Mime","Scyther","Jynx","Electabuzz","Magmar","Pinsir","Tauros","Magikarp","Gyarados","Lapras","Ditto","Eevee","Vaporeon","Jolteon","Flareon","Porygon","Omanyte","Omastar","Kabuto","Kabutops","Aerodactyl","Snorlax","Articuno","Zapdos","Moltres","Dratini","Dragonair","Dragonite","Mewtwo","Mew"]
        self.prefix = ['', 'Bulb', 'Ivy', 'Venu', 'Char', 'Char', 'Char', 'Squirt', 'War', 'Blast', 'Cater', 'Meta', 'Butter', 'Wee', 'Kak', 'Bee', 'Pid', 'Pidg', 'Pidg', 'Rat', 'Rat', 'Spear', 'Fear', 'Ek', 'Arb', 'Pika', 'Rai', 'Sand', 'Sand', 'Nido', 'Nido', 'Nido', 'Nido', 'Nido', 'Nido', 'Clef', 'Clef', 'Vul', 'Nine', 'Jiggly', 'Wiggly', 'Zu', 'Gol', 'Odd', 'Gloo', 'Vile', 'Pa', 'Para', 'Veno', 'Veno', 'Dig', 'Dug', 'Meow', 'Per', 'Psy', 'Gol', 'Man', 'Prime', 'Grow', 'Arca', 'Poli', 'Poli', 'Poli', 'Ab', 'Kada', 'Ala', 'Ma', 'Ma', 'Ma', 'Bell', 'Weepin', 'Victree', 'Tenta', 'Tenta', 'Geo', 'Grav', 'Gol', 'Pony', 'Rapi', 'Slow', 'Slow', 'Magne', 'Magne', 'Far', 'Do', 'Do', 'See', 'Dew', 'Gri', 'Mu', 'Shell', 'Cloy', 'Gas', 'Haunt', 'Gen', 'On', 'Drow', 'Hyp', 'Krab', 'King', 'Volt', 'Electr', 'Exegg', 'Exegg', 'Cu', 'Maro', 'Hitmon', 'Hitmon', 'Licki', 'Koff', 'Wee', 'Rhy', 'Rhy', 'Chan', 'Tang', 'Kangas', 'Hors', 'Sea', 'Gold', 'Sea', 'Star', 'Star', 'Mr.', 'Scy', 'Jyn', 'Electa', 'Mag', 'Pin', 'Tau', 'Magi', 'Gyara', 'Lap', 'Dit', 'Ee', 'Vapor', 'Jolt', 'Flare', 'Pory', 'Oma', 'Oma', 'Kabu', 'Kabu', 'Aero', 'Snor', 'Artic', 'Zap', 'Molt', 'Dra', 'Dragon', 'Dragon', 'Mew', 'Mew']
        self.suffix = ['', 'basaur', 'ysaur', 'usaur', 'mander', 'meleon', 'izard', 'tle', 'tortle', 'toise', 'pie', 'pod', 'free', 'dle', 'una', 'drill', 'gey', 'eotto', 'eot', 'tata', 'icate', 'row', 'row', 'kans', 'bok', 'chu', 'chu', 'shrew', 'slash', 'oran', 'rina', 'queen', 'ran', 'rino', 'king', 'fairy', 'fable', 'pix', 'tales', 'puff', 'tuff', 'bat', 'bat', 'ish', 'oom', 'plume', 'ras', 'sect', 'nat', 'moth', 'lett', 'trio', 'th', 'sian', 'duck', 'duck', 'key', 'ape', 'lithe', 'nine', 'wag', 'whirl', 'wrath', 'ra', 'bra', 'kazam', 'chop', 'choke', 'champ', 'sprout', 'bell', 'bell', 'cool', 'cruel', 'dude', 'eler', 'em', 'ta', 'dash', 'poke', 'bro', 'mite', 'ton', 'fetchd', 'duo', 'drio', 'eel', 'gong', 'mer', 'uk', 'der', 'ster', 'tly', 'ter', 'gar', 'ix', 'zee', 'no', 'by', 'ler', 'orb', 'ode', 'cute', 'utor', 'bone', 'wak', 'lee', 'chan', 'tung', 'fing', 'zing', 'horn', 'don', 'sey', 'gela', 'khan', 'sea', 'dra', 'deen', 'king', 'yu', 'mie', 'mime', 'ther', 'nx', 'buzz', 'mar', 'sir', 'ros', 'karp', 'dos', 'ras', 'to', 'vee', 'eon', 'eon', 'eon', 'gon', 'nyte', 'star', 'to', 'tops', 'dactyl', 'lax', 'cuno', 'dos', 'tres', 'tini', 'nair', 'nite', 'two', 'ew']
    
    async def fetch_pokemon(self, ctx: discord.AutocompleteContext):
        return [poke for poke in self.POKEMON_LIST if poke.startswith(ctx.value.capitalize())][:25]

    @discord.slash_command(description="Fuse two Pokemon to get an entirely new species!")
    @option("face", description="The face for the new Pokemon.", required=False, autocomplete=fetch_pokemon)
    @option("body", description="The body for the new Pokemon.", required=False, autocomplete=fetch_pokemon)
    async def fuse(self, ctx, face, body):
        if face is None:
            face = random.choice(self.POKEMON_LIST)
        if body is None:
            body = random.choice(self.POKEMON_LIST)

        if face == 'Koffing' and body == 'Eevee':
            name = 'Covfefe'
        elif face == 'Mr. Mime':
            name = self.prefix[self.POKEMON_LIST.index(face)] + " " + self.suffix[self.POKEMON_LIST.index(body)].capitalize()
        elif face == 'MissingNo' and body == 'MissingNo':
            name = 'Zero'
        elif face == 'MissingNo':
            name = body[0] + ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', (len(body) - 1))) 
        elif body == 'MissingNo':
            name = face[0] + ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', (len(face) - 1))) 
        else:
            name = self.prefix[self.POKEMON_LIST.index(face)] + self.suffix[self.POKEMON_LIST.index(body)]

        e = Embed(title=name)
        e.set_image(url=f"https://images.alexonsager.net/pokemon/fused/{self.POKEMON_LIST.index(body)}/{self.POKEMON_LIST.index(body)}.{self.POKEMON_LIST.index(face)}.png")
        await ctx.respond(f"You fused {face} and {body}!", embed=e)

def setup(bot):
    bot.add_cog(Test(bot))