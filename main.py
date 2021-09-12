import discord
import settings
import os
import discord.ext
from discord.ext import commands, tasks
from discord.ext.commands.core import command


TOKEN = settings.TOKEN
client = commands.Bot(command_prefix="!")

class BotClient(discord.Client):
    
    @client.event
    async def on_ready(self):
        print("bot online")

    @client.command
    async def ping(self, ctx):
        await ctx.send("pong!")

client = BotClient()
client.run(TOKEN)