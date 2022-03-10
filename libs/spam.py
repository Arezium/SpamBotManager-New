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
    
def spamDM(ctx, token, userID, message):
    makeDMdata = {
"recipient_id": userID
    }
    
    DMdata = {
"content": message
    }
    
    headers= mainHeaders(token)
    MakeDM = requests.post(f"{baseURL}/users/@me/channels", json=makeDMdata, headers=headers, proxies=switchProxy())
    json_= json.loads(MakeDM.content)
    for i in range(randrange(11,15)):
        try:
          result = requests.post(f"{baseURL}/channels/{json_['id']}/messages", json=DMdata, headers=headers, proxies=switchProxy())
                    
        except:
          pass

def spamMsg(token, message, channelID):
    
    msgData = { 
      "content": message
    }
    
    headers = mainHeaders(token)

    for i in range(randrange(3,8)):
      requests.post(f"{baseURL}/channels/{channelID}/messages", json=msgData, headers=headers, proxies=switchProxy())

def sendMsg(token, message, channelID):
    
    msgData = {
      "content": message
    }
    
    headers = mainHeaders(token)

    requests.post(f"{baseURL}/channels/{channelID}/messages", json=msgData, headers=headers, proxies=switchProxy())

#---------------------------------------------------#
#---------------------------------------------------#