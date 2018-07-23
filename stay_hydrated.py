import discord
import threading
from discord.ext import commands

class StayHydrated:
  def __init__(self, bot):
      self.bot = bot
      self.do_preach = threading.Event()

  async def stay_hydrated(self):
    if self.do_preach.is_set():
      await self.bot.say("Friendly reminder to drink some water!")
    threading.Timer(60*60, self.stay_hydrated, [self]).start()

  @commands.command()
  async def preach(self):
    if not self.preach:
      await self.bot.say("I will now preach the gospel of Poseidon!")
      self.stay_hydrated()
      self.do_preach.set()
    else:
      await self.bot.say("You are a heritic and an all-around bad person. You should be ashamed of yourself.")
      self.do_preach.clear()

def setup(bot):
    bot.add_cog(StayHydrated(bot))
