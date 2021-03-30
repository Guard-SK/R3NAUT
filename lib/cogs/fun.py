
from random import choice, randint
from typing import Optional
from discord.errors import HTTPException
from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi", "sup"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya', 'Sup', 'Ciao', '<:peepohey:806962515152994406>'))} {ctx.author.mention}!")

    @command(name="ahoj", aliases=["čau", "cav", "cau"])
    async def povedz_ahoj(self, ctx):
        await ctx.send(f"{choice(('<:peepohey:806962515152994406>', 'Ahoj', 'Čau', 'Hej', 'Cav', 'Sup', 'Ciao'))} {ctx.author.mention}!") #'My name is Jeff', 'Hello, my name is R3NAUT, and Im developed by Guard_SK', 'Hello, my name is R3NAUT', 'Whats going on?', 'I wasnt ready for that..'     



    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 100:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
        
        else: 
            await ctx.send("Too many dice rolled. Please try lower number.")

    @roll_dice.error
    async def roll_dice_error(self, ctx, exc):
        if isinstance(exc.original, HTTPException):
            await ctx.send("Too many dice rolled. Please try lower number.")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("Can't find the memeber you mentioned.")

    @command(name="say", aliases=["echo"])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))