# -*- coding: utf-8 -*-

print("Importing modules... This might take a while.")
try:
  import threading
  from threading import Thread
  import server
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
except:
  import os
  os.system("pip install -r requirements.txt")

from libs import (
    define,
    other
)
print("Imported local dependencies.")
from libs.define import (
  http_amount,
  socks4_amount,
  socks5_amount,
  total_proxies,
  tokens,
  folder,
  tok,
  vined,
  bot
)
print("Imported the main modules and variables.")
from libs.other import doClear



owner_id = vined
bot = bot

print("ok")

doClear()

print(f"Loaded {http_amount} HTTP proxies")
print(f"Loaded {socks4_amount} Socks4 proxies")
print(f"Loaded {socks5_amount} Socks5 proxies")

print(f"\nLoaded {total_proxies} total proxies")
print("\n")

print(f"Loaded {len(define.tokens)} bot tokens")

print("\n\nLogging in bot...")
  

@bot.event
async def on_message(message):
        
    if message.author.id in define.people:
      if message.content.startswith("*dm") and message.author.id in define.anti_dm:
        return
        
      return await define.bot.process_commands(message)

cog_list = []
for filename in os.listdir(folder):
  if filename.endswith('.py'):
      try:
        bot.load_extension(f'{folder}.{filename[:-3]}')
        cog_list.append(filename[:-3])
        print("Loaded cog", filename)
      except Exception as e:
          print(f"An error occurred while loading {filename}: {e}")

server.keep_alive()
  
bot.run(tok) 