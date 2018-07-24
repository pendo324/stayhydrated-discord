import discord
import threading
import asyncio
from discord.ext import commands

import pprint
pp = pprint.PrettyPrinter(indent=4)

class StayHydrated:
  def __init__(self, bot):
      self.bot = bot
      self.do_preach = threading.Event()
      self.do_preach.clear()
      self.channels = []

  async def stay_hydrated(self, ctx):
    channel = ctx['channel']
    delay = ctx['delay']
    do_preach = ctx['do_preach']
    pp.pprint("preaching in channel {} with delay {}!".format(channel.id, delay))
    while do_preach.is_set():
      try:
        await self.bot.send_message(channel, "Friendly reminder to drink some water!")
      except Exception as e:
        pp.pprint(e)
      await asyncio.sleep(delay)

  @commands.command(pass_context=True)
  async def preach(self, ctx, delay=60*60, channel: discord.Channel=None):
    if channel == None:
      channel = ctx.message.channel

    channel_list_entries = [i for i in self.channels if i['ctx']['channel'].id == channel.id]
    channel_list_entry = None
    if len(channel_list_entries) == 1:
      channel_list_entry = channel_list_entries[0]
    elif len(channel_list_entries) == 0:
      do_preach = threading.Event()
      do_preach.clear()
      ctx = {
        'channel': channel,
        'delay': delay,
        'do_preach': do_preach
      }
      task = asyncio.ensure_future(self.stay_hydrated(ctx))
      new_list_entry = {
        'ctx': ctx,
        'task': task,
      }
      self.channels.append(new_list_entry)
      channel_list_entry = new_list_entry

    if channel_list_entry['ctx']['do_preach'].is_set():
      channel_list_entry['ctx']['do_preach'].clear()
    else:
      channel_list_entry['ctx']['do_preach'].set()

    if channel_list_entry['ctx']['do_preach'].is_set():
      await self.bot.say("I will now preach the gospel of Poseidon!")
    else:
      await self.bot.say("You are a heritic and an all-around bad person. You should be ashamed of yourself.")
      channel_list_entry['ctx']['do_preach'].clear()
      channel_list_entry['task'].cancel()
      self.channels.remove(channel_list_entry)


def setup(bot):
    bot.add_cog(StayHydrated(bot))
