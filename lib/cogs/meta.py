import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from time import time

class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ping")
    async def ping(self, ctx):
        start = time()
        message = await ctx.send(f"Pong! DWSP latency is: {self.bot.latency*1000:,.0f} ms.")
        end = time()

        await message.edit(content=f"Pong! DWSP latency is: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("meta")

def setup(bot):
    bot.add_cog(Meta(bot))