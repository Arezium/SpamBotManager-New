import threading
from threading import Thread
import flask
from flask import Flask
import requests
import discord, asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from contextlib import redirect_stdout
import subprocess
import random
from random import randrange
import math
import json, inspect, io, textwrap, traceback, os, sys
from itertools import cycle
from libs import (
    define,
    spam
)
from libs.define import *
from libs.spam import *

class Spam(commands.Cog, name="Spam Commands"):
  def __init__(self, bot):
    self.bot = bot
    self.tokens = define.tokens
    self.arezid = define.arezium
    self.vined = define.vined
    
  @commands.command()
  async def dm(self, ctx, member: discord.Member, *, msg:str="Get Rekt Dreamphobe"):
    """Spamdms someone"""
    id = str(member.id)
    
    await ctx.send(f"Sending dms to {member.mention} using {len(self.tokens)} bots")
  
    threads = []
  
    for token in self.tokens:
       thread = Thread(target = spam.spamDM, args = [ctx, token, id, msg])
       thread.start()
       threads.append(thread)
       
       
    for thread in threads:
       thread.join()
    
    return await ctx.send(f"Finished DMing {member.mention}")


  
  @commands.command()
  async def spam(self, ctx, *, msg:str="Get Rekt Dreamphobe"):
    """Spams a message"""
    id = str(ctx.message.channel.id)
  
    threads = []

    for token in self.tokens:
       thread = threading.Thread(target = spam.spamMsg, args = [token, msg, id])
       thread.start()
       threads.append(thread)
       
    for thread in threads:
       thread.join()
    
  @commands.command()
  async def say(self, ctx, *, msg:str="HI"):
    """Sends a message"""
    id = str(ctx.message.channel.id)
  
    threads = []

    for token in self.tokens:
       thread = threading.Thread(target = spam.sendMsg, args = [token, msg, id])
       thread.start()
       threads.append(thread)
       
    for thread in threads:
       thread.join()

    
def setup(bot):
  bot.add_cog(Spam(bot))