import os
import asyncio
from datetime import datetime, timedelta
from time import time
import random
import json

import discord
from discord import Embed
from discord.ui import Button


class CategorySelect(discord.ui.View):
    def __init__(self, host, channel):
        super().__init__(timeout=30)
        self.host = host
        self.channel = channel
        self.players = []
        self.data = None

        with open(os.getcwd()+'/src/kahoot/index.json', 'r') as f:
            self.categories = json.load(f)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.host.id:
            await interaction.response.send_message("You're not the host.", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit_original_message(embed=Embed(description="You took too long.", color=0xed4245), view=self)

    with open(os.getcwd()+'/src/kahoot/index.json', 'r') as f:
        f = json.load(f)
        quizlist = f.keys()
    @discord.ui.select(
        placeholder = "Select a quiz", 
        min_values = 1, 
        max_values = 1, 
        options = [discord.SelectOption(label=name) for name in quizlist]
    )
    async def select_callback(self, select, interaction): 
        try:
            with open(os.getcwd()+f'/src/kahoot/{self.categories[select.values[0]]}', 'r') as f:
                f = json.load(f)
            if len(f["questions"]) < 1:
                await interaction.response.send_message("This quiz has no questions!", ephemeral=True)
            else:
                self.data = f
        except Exception as e:
            await interaction.response.send_message("<:latiasRip:998903635188658208> Something went wrong while loading the quiz data.", ephemeral=True)
            print(e)
        
    @discord.ui.button(label="Start", style=discord.ButtonStyle.secondary) 
    async def start_game(self, button, interaction):
        if self.data is None:
            await interaction.response.send_message("You have to select a quiz first.", ephemeral=True)
        else:
            for child in self.children:
                child.disabled = True
            button.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            self.stop()
            e = Lobby(self.host)
            view = Join(self.host, self.channel, self.data, e)
            view.message = await self.channel.send(embed=e, view=view)
            await view.start()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_game(self, button, interaction):
        for child in self.children:
            child.disabled = True
        button.style = discord.ButtonStyle.danger
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("No fun then.")
        self.stop()



class Lobby(Embed):
    def __init__(self, host):
        self.start = datetime.now() + timedelta(seconds=30)
        super().__init__(title="A Kahoot game is starting!", description=f"Click the button to join! Starts <t:{round(self.start.timestamp())}:R>", color=0x864cbf)
        self.set_footer(text=f"Hosted by {host.name}")
        


class Join(discord.ui.View):
    def __init__(self, host, channel, data, embed):
        super().__init__()
        self.host = host
        self.channel = channel
        self.data = data
        self.players = []
        self.embed = embed
    
    async def start(self):
        await asyncio.sleep(30)
        if len(self.players) < 1:
            self.embed.description = "No one joined."
            for child in self.children:
                child.disabled = True
            await self.message.edit(embed=self.embed, view=self)
            await self.channel.send("So sad, no one joined.")
        else:
            self.embed.description = "The game has begun."

            random.shuffle(self.data['questions'])    # Randomly arrange the order of questions
            for q in self.data['questions']:          # Randomly arrange the order of answers, if there are more than 2 answers
                if len(q['a']) > 2:
                    random.shuffle(q['a'])

            if len(self.data['questions']) > 20:      # Get the first n questions only, in this case n = 20
                self.data['questions'] = self.data['questions'][:20]

            await self.channel.send(embed=Embed(title="Get Ready!", description=f"**{self.data['name']}** by {self.data['author']}\n\nQuestions: {len(self.data['questions'])}"))
            
            # Wait 5 seconds and start the quiz
            await asyncio.sleep(5)
            try:    # Sends Question 1
                view=Answers(self.host, self.channel, self.data, self.players, 1, [(p, 0, 0) for p in self.players])
                view.message = await self.channel.send(embed=Question(self.data, 1), view=view)
            except Exception as e:    # Sends Question 2 if an error occured
                self.channel.send("<:latiasRip:998903635188658208> An error occured while loading Question 1.")
                view=Answers(self.host, self.channel, self.data, self.players, 2, [(p, 0, 0) for p in self.players])
                view.message = await self.channel.send(embed=Question(self.data, 2), view=view)
                print(e)

            for child in self.children:
                child.disabled = True
            await self.message.edit(embed=self.embed, view=self)
            await view.run()
        self.stop()

    @discord.ui.button(label="0", emoji="<:icon:1005026244229869568>", style=discord.ButtonStyle.success) 
    async def join_callback(self, button, interaction):
        if interaction.user in self.players:
            self.players.remove(interaction.user)
            self.embed.clear_fields()
            if len(self.players) > 0:
                self.embed.add_field(name=f"Players ({len(self.players)})", value=', '.join([p.mention for p in self.players]))
            button.label = len(self.players)
            await interaction.response.edit_message(embed=self.embed, view=self)
            await interaction.followup.send("Removed you from the players list.", ephemeral=True)
        else:
            self.players.append(interaction.user)
            button.label = len(self.players)
            self.embed.clear_fields()
            self.embed.add_field(name=f"Players ({len(self.players)})", value=', '.join([p.mention for p in self.players]))
            await interaction.response.edit_message(embed=self.embed, view=self)
            await interaction.followup.send(embed=Embed(title="You're in!", description="See your name on screen?", color=0x864cbf), ephemeral=True)



class Question(Embed):
    def __init__(self, data, question):
        ref = data['questions'][question-1]
        super().__init__(title=f"Question {question}", description=ref['q'])

        number_emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        i = 0
        ans = ""
        for a in ref['a']:
            ans += f"{number_emoji[i]} {a['text']}\n"
            i += 1
        self.add_field(name="Choose an answer", value=ans)
        if 'img' in ref:
            self.set_image(url = ref['img'])



class Answers(discord.ui.View):
    def __init__(self, host, channel, data, players, question, scoreboard):
        super().__init__()
        self.host = host
        self.channel = channel
        self.data = data
        self.players = players
        self.scoreboard =  scoreboard # (user, score, answer streak)
        self.question = question
        self.answers = []
        self.correct = []
        self.wrong = []

    async def answer_callback(self, interaction):
        if interaction.user not in self.players:
            await interaction.response.send_message("Hey! You're not in the game.", ephemeral=True)
        elif interaction.user in [p[0] for p in self.correct] + self.wrong:
            await interaction.response.send_message("You already selected your answer.", ephemeral=True)
        else:
            if interaction.custom_id.startswith('correct'):
                self.correct.append(tuple((interaction.user, time())))
            elif interaction.custom_id.startswith('wrong'):
                self.wrong.append(interaction.user)
            chosen = int(interaction.custom_id.split('-')[1])
            self.answers.append(chosen)
            await interaction.response.send_message(f"You selected **{self.ref['a'][chosen]['text']}**.", ephemeral=True)

    async def run(self):
        self.ref = self.data['questions'][self.question-1]
        self.number_emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        i = 0
        for a in self.ref['a']:
            if a['isCorrect'] is True:
                button = Button(emoji=self.number_emoji[i], custom_id=f'correct-{i}', style=discord.ButtonStyle.primary)
            else:
                button = Button(emoji=self.number_emoji[i], custom_id=f'wrong-{i}', style=discord.ButtonStyle.primary)
            button.callback = self.answer_callback
            self.add_item(button)
            i += 1
        await self.message.edit(view=self)

        if 't' in self.ref:
            self.time = self.ref['t']
        else:
            self.time = 15
        rate = 4    # Refresh every n seconds
        self.timer = time()
        await self.message.edit(content=f"**{self.time}**")
        if self.time % rate != 0:
            await asyncio.sleep(self.time % rate)
            self.time -= self.time % rate
            await self.message.edit(content=f"**{self.time}**")
        while self.time > 0:
            await asyncio.sleep(rate)
            self.time -= rate
            if self.time == 0:
                await self.message.edit(content=f"**Time's up!**")
            else:
                await self.message.edit(content=f"**{self.time}**")
        self.total_time = time()
        for child in self.children:
            if child.custom_id.startswith('correct'):
                child.style = discord.ButtonStyle.success
            else:
                child.style = discord.ButtonStyle.secondary
            child.disabled = True

        # Show answers
        ans = ''
        i = 0
        for a in self.ref['a']:
            if a['isCorrect'] is True:
                emoji = '✅'
            else:
                emoji = '❌'
            ans += f"{emoji}{self.number_emoji[i]} {a['text']} **({self.answers.count(i)})**\n"
            i += 1
            e = self.message.embeds[0]
            e.clear_fields()
            e.add_field(name="Answers", value=ans)
        await self.message.edit(embed=e, view=self)

        # Update scores
        c_names = [p[0] for p in self.correct]
        i = 0
        for p in self.scoreboard:
            p = list(p)
            if p[0] in c_names:
                p[2] += 1
                p[1] += round((1 - ((self.correct[c_names.index(p[0])][1] - self.timer) / (2 * (self.total_time - self.timer)))) * (900 + ((p[2]*100) if p[2]<6 else 600)))
            else:
                p[2] = 0
            p = tuple(p)
            self.scoreboard[i] = p
            i += 1

        embed = Leaderboard(self.host, self.channel, self.data, self.players, self.question, self.scoreboard)
        embed.order_scores()
        await self.channel.send(embed=embed)
        await embed.next_question()
        self.stop()



class Leaderboard(Embed):
    def __init__(self, host, channel, data, players, question, scoreboard):
        super().__init__(title="Leaderboard")
        self.host = host
        self.channel = channel
        self.data = data
        self.players = players
        self.question = question
        self.scoreboard =  scoreboard # (user, score, answer streak)
        self.set_footer(text=f"{len(self.data['questions']) - self.question} questions left")

    def order_scores(self):
        def get_score(elem):
            return elem[1]
        self.ordered = self.scoreboard
        self.ordered.sort(key=get_score, reverse=True)

        scores = ''
        for p in self.ordered:
            scores += f"`#{self.ordered.index(p) + 1}` {p[0].name} : `{p[1]} points` {('`🔥'+str(p[2])+'`') if p[2]>1 else ''}\n"
        self.description = scores

    async def next_question(self):
        await asyncio.sleep(5)
        if self.question == len(self.data['questions']):
            scores = f"🏆 {self.ordered[0][0].name} : `{self.ordered[0][1]} points`\n"
            if len(self.players) > 1:
                scores += f"🥈 {self.ordered[1][0].name} : `{self.ordered[1][1]} points`\n" 
            if len(self.players) > 2:
                scores += f"🥉 {self.ordered[2][0].name} : `{self.ordered[2][1]} points`\n"
            scores += "\n**Thanks for playing!**" 
            await self.channel.send(embed=Embed(title="Final Results!", description=scores, color=0xffdd33))
        else:
            try:
                view=Answers(self.host, self.channel, self.data, self.players, self.question + 1, self.scoreboard)
                view.message = await self.channel.send(embed=Question(self.data, self.question + 1), view=view)
                await view.run()
            except Exception as e:
                await self.channel.send(f"<:latiasRip:998903635188658208> An error occured while loading Question {self.question + 1}.")
                view=Answers(self.host, self.channel, self.data, self.players, self.question + 2, self.scoreboard)
                view.message = await self.channel.send(embed=Question(self.data, self.question + 2), view=view)
                await view.run()
                print(e)
            