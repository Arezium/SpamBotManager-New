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
    info
)
from libs.define import * 
from libs.info import getBotInvites, getBotInfo


class Information(commands.Cog, name="Information Commands"):
  def __init__(self, bot):
    self.bot = bot
    self.http = define.http_amount
    self.socks4 = define.socks4_amount
    self.socks5 = define.socks5_amount
    self.proxies = define.total_proxies
    self.tokens = define.tokens
    self.tserver = define.tokenserver
    self.wlist = define.people
    self.allowed = define.allowed
    self.anti_dm = define.anti_dm
  
  @commands.command()
  async def info(self, ctx):
    """Sends some information on the bot"""
  
    msg = await ctx.send("Loading information...")
    embed = discord.Embed(
    description=f"""
```
Bot info:
  - Total servers: {len(self.bot.guilds)}
  - Total members: {len(self.bot.users)}

Management info:
  - Total bot tokens: {len(self.tokens)}
  - HTTP proxies: {self.http}
  - Socks4 proxies: {self.socks4}
  - Socks5 proxies: {self.socks5}
  - Total proxies: {self.proxies}

Other:
  - People that can use the bot: {len(self.wlist)}
```"""
    )
  
    return await msg.edit(content="", embed=embed)



  @commands.command()
  async def invites(self, ctx):
    """Sends all the bots invites"""
    ids = []
    invites = []
  
    msg = await ctx.send("Loading invites...")

    info.getBotInvites(ids, invites)
  
    nl = "\n  "
    embed = discord.Embed(
    description=f"""```
Invites:
  {nl.join(invites)}
```"""
    )
  
    return await msg.edit(content="", embed=embed)


  @commands.command()
  async def bots(self, ctx):
    """Sends all the bots names and ids"""
    names = []
    ids = []
  
    msg = await ctx.send("Loading bots information...")

    info.getBotInfo(ids, names)
  
    nl = "\n  "
    embed = discord.Embed(
    description=f"""```
Names:
  {nl.join(names)}  
                 
IDs:
  {nl.join(ids)}
```"""
    )
  
    return await msg.edit(content="", embed=embed)

  @commands.command(hidden=True)
  async def tokens(self, ctx):
    toks = []
  
    if ctx.message.guild.id != self.tserver:
      return
    
    msg = await ctx.send("Loading bots information...")

    for token in self.tokens:
      toks.append(token)
    
    nl = "\n  "
    embed = discord.Embed(
    description=f"""```
Tokens:
  {nl.join(toks)}
```"""
    )
    return await msg.edit(content="", embed=embed)



def setup(bot):
  bot.add_cog(Information(bot))