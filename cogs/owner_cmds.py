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
    info,
    other
)
from libs.define import *
from libs.info import *
from libs.other import *

class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.http = define.http_amount
    self.socks4 = define.socks4_amount
    self.socks5 = define.socks5_amount
    self.proxies = define.total_proxies
    self.tokens = define.tokens
    self.arezid = define.arezium
    self.vined = define.vined
    self.tserver = define.tokenserver
    self.wlist = define.people
    self.allowed = define.allowed
    self.anti_dm = define.anti_dm
    self.folder = define.folder

  @commands.command()
  async def botname(self, ctx, *, bname):
    """
    Changes the name of all the bots
    
    """
    if ctx.author.id not in self.allowed:
      return
    else:
      threads = []
  
      for token in self.tokens:
         thread = threading.Thread(target = other.changeName, args = [bname, token])
         thread.start()
         threads.append(thread)
       
       
      for thread in threads:
         thread.join()
    return await ctx.send(f"Changed the name of {len(self.tokens)} bots to \"{bname}\"")

  
  @commands.command(name='eval')
  async def _eval(self, ctx, *, body):
        if ctx.message.author.id not in self.allowed:
          return
        """Evaluates python code"""
        def cleanup_code(content):
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
            return content.strip('` \n')
        env = {
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource,
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))
        
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                self.bot._last_result = ret
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')  # tick
        elif err:
            await ctx.message.add_reaction('\u2049')  # x
        else:
            await ctx.message.add_reaction('\u2705')

  def get_syntax_error(e):
      if e.text is None:
          return f'```py\n{e.__class__.__name__}: {e}\n```'
      return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

  @commands.command()
  async def load(self, ctx, cog):
        if ctx.message.author.id == self.vined:
            if cog == "*" or cog == "all":
                await ctx.send("Loading all cogs...")
                for filename in os.listdir(f'{self.folder}'):
                    if filename.endswith('.py'):
                        try:
                            self.bot.load_extension(f'{self.folder}.{filename[:-3]}')
                            await ctx.send(f"Succesfully loaded cog {filename}")
                        except Exception as e:
                            await ctx.send(str(e))
                return await ctx.send("Loaded all cogs")

            print(f"Trying to load cog {cog}...")
            await ctx.send(f"Loading cog \"{cog}\"")
            try:
                self.bot.load_extension(f"{self.folder}.{cog}")
                print(f"Succesfully loaded cog {cog}")
                await ctx.send(f"Succesfully loaded cog {cog}")
            except Exception as e:
                print(str(e))
                await ctx.send(str(e))
        else:
          return
            
  @commands.command()
  async def unload(self, ctx, cog):
        if ctx.message.author.id == self.vined:
            if cog == "*" or cog == "all":
                await ctx.send("Unloading all cogs...")
                for filename in os.listdir(f'{self.folder}'):
                    if filename.startswith("owner"):
                        continue
                    if filename.endswith('.py'):
                        try:
                            self.bot.unload_extension(f'{self.folder}.{filename[:-3]}')
                            await ctx.send(f"Succesfully unloaded cog {filename}")
                        except Exception as e:
                            await ctx.send(str(e))
                return await ctx.send("Unloaded all cogs!")

            if cog == "owner":
                return

            print(f"Trying to unload cog {cog}...")
            await ctx.send(f"Unloading cog \"{cog}\"")
            try:
                self.bot.unload_extension(f"{self.folder}.{cog}")
                print(f"Succesfully unloaded cog {cog}")
                await ctx.send(f"Succesfully unloaded cog {cog}")
            except Exception as e:
                print(str(e))
                await ctx.send(str(e))
        else:
          return
            
  @commands.command()
  async def reload(self, ctx, cog):
        if ctx.message.author.id == self.vined:
            if cog == "*" or cog == "all":
                await ctx.send("Reloading all cogs...")
                for filename in os.listdir(f'{self.folder}'):
                    if filename.endswith('.py'):
                        try:
                            self.bot.reload_extension(f'{self.folder}.{filename[:-3]}')
                            await ctx.send(f"Succesfully reloaded cog {filename}")
                        except Exception as e:
                            await ctx.send(str(e))
                return await ctx.send("Reloaded all cogs")
    
            print(f"Trying to reload cog {cog}...")
            await ctx.send(f"Reloading cog \"{cog}\"")
            try:
                self.bot.reload_extension(f'{self.folder}.{cog}')
                print(f"Succesfully reloaded cog {cog}")
                await ctx.send(f"Succesfully reloaded cog {cog}")
            except Exception as e:
                print(str(e))
                await ctx.send(str(e))
        else:
          return

def setup(bot):
  bot.add_cog(Owner(bot))