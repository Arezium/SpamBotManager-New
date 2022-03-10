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
    define
)
from libs.define import *

class Misc(commands.Cog, name="Miscellanous Commands"):
  def __init__(self, bot):
    self.bot = bot
    self.tokens = define.tokens
    self.arezid = define.arezium
    self.vined = define.vined
    self.allowed = define.allowed

  @commands.command(name="status", description="Available statuses are: online, dnd (do not disturb), offline, idle")
  async def status(self, ctx, *, args):
    """Changes the bots statuses (fail)"""
    args = args.lower()
    for token in self.tokens:
        try:
          resp = requests.patch(f"{define.baseURL}/users/@me/settings", headers=define.mainHeaders(token), data=json.dumps({"custom_status": {"text":args}}))
        except:
          pass
    await ctx.send(resp.text)
        
  
  

                                  
def setup(bot):
  bot.add_cog(Misc(bot))