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


#---------------------------------------------------#
#---------------------------------------------------#

def getBotInvites(ids, invites):
  """
  Gets all the bots invites and lists it
  
  """
  for token in tokens:
    headers = mainHeaders(token)
    req = requests.get(f'{baseURL}/users/@me', headers=headers)
    r = req.json()
    id = r.get("id")
    ids.append(str(id))
    invite = f"https://discord.com/oauth2/authorize?client_id={id}&scope=bot&permissions=8"
    invites.append(invite)


def getBotInfo(ids, names):
  """
  Gets all the bots information and lists it
  
  """
  for token in tokens:
    headers = mainHeaders(token)
    req = requests.get(f'{baseURL}/users/@me', headers=headers, proxies=switchProxy())
    r = req.json()
    name = str(r.get("username")) + '#' + str(r.get("discriminator"))
    id = r.get("id")
    names.append(str(name))
    ids.append(str(id))
  
#---------------------------------------------------#
#---------------------------------------------------#