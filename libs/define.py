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

global tokens
global arezium
global vined
global baseURL
global folder

prefix = "*"
intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(
    no_category = 'Other'
)
bot = commands.Bot(
    command_prefix = commands.when_mentioned_or(prefix),
    strip_after_prefix = True,
    help_command = help_command,
    intents=intents
)

baseURL = "https://discord.com/api/v8"

#env
tok = os.getenv("TOKEN") #the manager bot token
tokens = json.loads(os.environ["BOT_TOKENS"]) #list, main part of the bot
tokenserver = int(os.environ.get('WHITELISTED_TOKENS_SERVER')) #not needed (the server in which you can use the tokens command)
people = json.loads(os.environ["PEOPLE"]) #list - uses ids
blackListed = json.loads(os.environ["BLACKLISTED_CHANNELS"]) #list - uses ids
anti_dm = json.loads(os.environ['BLACKLISTED_PEOPLE']) #list, makes people not be able to use dm command - uses ids

#for information refer to below - uses id
owner = os.environ.get("OWNER")

#list - uses ids (the people that can access the owner_cmds cog (except load, reload and unload - only the bot owner can do that))
owners = json.loads(os.environ["OWNERS"])



folder = 'cogs'
allowed = owners


def getProxies(protocol):
  resp = requests.get(f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout=10000&country=all&ssl=all&anonymity=all")
  return resp.text

http, socks4, socks5 = False, False, True
  
http_proxyList = getProxies('http')
socks4_proxyList = getProxies('socks4')
socks5_proxyList = getProxies('socks5')

http_pool = cycle(http_proxyList)
socks4_pool = cycle(socks4_proxyList)
socks5_pool = cycle(socks5_proxyList)

#http_proxyList = open("./proxies/http_proxies.txt", "r").read().splitlines()
#socks4_proxyList = #open("./proxies/socks4_proxies.txt", "r").read().splitlines()
#socks5_proxyList = open("./proxies/socks5_proxies.txt", "r").read().splitlines()

http_amount = str(len(http_proxyList) if http == True else "0 (HTTP Proxies disabled)")
socks4_amount = str(len(socks4_proxyList) if socks4 == True else "0 (SOCKS4 Proxies disabled)")
socks5_amount = str(len(socks5_proxyList) if socks5 == True else "0 (SOCKS5 Proxies disabled)")
if http == True and socks4 == False and socks5 == False:
  total_proxies = http_amount
  
elif http == True and socks4 == True and socks5 == False:
  total_proxies = http_amount + socks4_amount
  
elif http == True and socks4 == True and socks5 == True:
  total_proxies = http_amount + socks4_amount + socks5_amount
  
elif http == False and socks4 == True and socks5 == False:
  total_proxies = socks4_amount
  
elif http == True and socks4 == True and socks5 == False:
  total_proxies = http_amount + socks4_amount
  
elif http == False and socks4 == False and socks5 == True:
  total_proxies = socks5_amount

#---------------------------------------------------#
#---------------------------------------------------#

def switchProxy():
      #return {
      #"http": random.choice(http_proxyList),
      #"socks4": random.choice(socks4_proxyList),
      #"socks5": random.choice(socks5_proxyList)
    #}
  if http == True and socks4 == False and socks5 == False:
    return {
    "http": next(http_pool)
  }
  elif http == True and socks4 == True and socks5 == False:
    return {
    "http": next(http_pool),
    "socks4": next(socks4_pool)
  }
  elif http == True and socks4 == True and socks5 == True:
    return {
    "http": next(http_pool),
    "socks4": next(socks4_pool),
    "socks5": next(socks5_pool)
  }
  elif http == False and socks4 == True and socks5 == False:
    return {
    "socks4": next(socks4_pool)
  }
  elif http == True and socks4 == True and socks5 == False:
    return {
    "http": next(http_pool),
    "socks4": next(socks4_pool)
  }
  elif http == False and socks4 == False and socks5 == True:
    return {
    "socks5": next(socks5_pool)
  }

def randstr(length):
  """
  Used to generate the cookie in mainHeaders()
  
  """
  alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
  text = ''
  for i in range(0, length):
      text += alpha[random.randint(0, len(alpha) - 1)]
  return text

def mainHeaders(token):
  """
  Defines the main header used in the bot
  
  """
  return {
        "authorization": "Bot "+str(token),
        "content-type": "application/json",
        "cookie": f"__cfuid={randstr(43)}; __dcfduid={randstr(32)}; locale=en-US",
        "origin": "https://discord.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjI0NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InNrIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTkwMTYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
  }
  
#---------------------------------------------------#
#---------------------------------------------------#