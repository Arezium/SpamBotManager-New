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

def doClear():
  os.system('cls')
  os.system('clear')

def changeName(username, token):
  """
  Changes the bots names
  """
  headers = define.mainHeaders(token)
  req = requests.get(f'{define.baseURL}/users/@me', headers=headers, proxies=define.switchProxy())
  r = req.json()
  name = str(r.get("username"))
  # if name.startswith("TMH") or name.startswith("Real Vx") or name.startswith("Real Cosmo"):
    # return
  else:
    try:
      data = {"username": username}
      requests.patch(f'{define.baseURL}/users/@me', headers=headers, json=data, proxies=define.switchProxy())
    except:
      pass
  
#---------------------------------------------------#
#---------------------------------------------------#
