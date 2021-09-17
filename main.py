import discord
import settings
import logging
import random
from discord.ext import commands, tasks 


TOKEN = settings.TOKEN

def init_logger():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)



class BotCommands(commands.Cog):

    async def on_ready(self):
        print("bot online")

#Write commands starting with @commands.command() and then write an async def

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command()
    async def test(self, ctx, args):
        await ctx.send("yes "+ args)

    @commands.command()
    async def word(self, ctx):
        self.words = ["cat","dog","human","tree","house","rock","water"]
        random.shuffle(self.words)
        self.word = random.choice(self.words)
        await ctx.send("Your word is: "+ self.word)
    
    @commands.command()
    async def roll(self, ctx, num):
        self._num = int(num)
        self.rez = random.randint(0,self._num)
        await ctx.send(self.rez)


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))


bot.add_cog(BotCommands(bot))
init_logger()
bot.run(TOKEN)
