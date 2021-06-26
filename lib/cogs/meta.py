import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Activity, ActivityType
from apscheduler.triggers.cron import CronTrigger
from time import time

class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.message = "playing 3help | 3ahelp | Moderating {users:,} users on 𝓖𝓪𝓶𝓲𝓷𝓰 𝓵𝓪𝓲𝓻"

        bot.scheduler.add_job(self.set, CronTrigger(second=0))

    @property
    def message(self):
        return self._message.format(users=len(self.bot.users))

    @message.setter
    def message(self, value):
        if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
            raise ValueError("Invalid activity type.")
        self._message = value
        

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)

        await self.bot.change_presence(activity=Activity(
            name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
        ))

    @command(name="setactivity")
    async def set_activity_message(self, ctx, *, text: str):
        self.message = text
        await self.set()
        await ctx.send(f"Setting activity to *{text}*", delete_after=10)

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