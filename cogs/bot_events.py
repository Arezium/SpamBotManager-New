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



class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.anti_dm = define.anti_dm
    self.wlist = define.people

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"Logged in {self.bot.user} - {self.bot.user.id}\nInvite: https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8")




def setup(bot):
  bot.add_cog(Events(bot))