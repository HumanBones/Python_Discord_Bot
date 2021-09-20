import discord
import settings
import logging
import random
import os
import youtube_dl
from discord.ext import commands, tasks 


TOKEN = settings.TOKEN
bot = commands.Bot(command_prefix="!")

ydl_opts = {
    'format': '250'
}

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

    @commands.command()
    async def join(self, ctx, channel="General"):
      voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
      voice = discord.utils.get(bot.voice_clients, guild=ctx.guild) 

      if voice is None:
          await voiceChannel.connect()

      else:
        await ctx.send("Already in voice channel!")
    
    @commands.command()
    async def play(self, ctx, url : str):
      voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
      song_there = os.path.isfile("song.mp3")

      if voice is None:
        await ctx.send("Not in voice channel! Use command !join")
      
      try:
          if song_there:
            os.remove("song.mp3")

      except PermissionError:
          await ctx.send("Song already playing!")
          return


      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
      for file in os.listdir("./"):
        if file.endswith(".webm"):
          os.rename(file, "song.webm")
      
      voice.play(discord.FFmpegOpusAudio("song.webm"))

      


      

    @commands.command()
    async def fuckoff(self, ctx):
      voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
      if voice is not None:
        await voice.disconnect()
      else:
        await ctx.send("Not connected.\nWhy you bully me? :(")

    @commands.command()
    async def pause(self, ctx):
      voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
      if voice.is_playing():
        voice.pause()
      else:
        await ctx.send("No auido is playing!")

    @commands.command()
    async def resume(self, ctx):
      voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
      if voice.is_paused():
        voice.resume()
      else:
        await ctx.send("No auido paused!")

    @commands.command()
    async def stop(self, ctx):
      voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
      if voice.is_playing():
        voice.stop()
      else:
        await ctx.send("No auido is playing!Are you def")





@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))


bot.add_cog(BotCommands(bot))
init_logger()
bot.run(TOKEN)
