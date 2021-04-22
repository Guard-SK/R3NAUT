
from random import choice, randint
from typing import Optional
from discord.errors import HTTPException
from aiohttp import request
from discord.ext import commands, tasks
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

    #@command(name="ahoj", aliases=["čau", "cav", "cau"])
    #async def povedz_ahoj(self, ctx):
        #await ctx.send(f"{choice(('<:peepohey:806962515152994406>', 'Ahoj', 'Čau', 'Hej', 'Cav', 'Sup', 'Ciao'))} {ctx.author.mention}!") #'My name is Jeff', 'Hello, my name is R3NAUT, and Im developed by Guard_SK', 'Hello, my name is R3NAUT', 'Whats going on?', 'I wasnt ready for that..'     

     

    @command(name="dice", aliases=["roll"])
    @cooldown(1, 10, BucketType.user)
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
    @cooldown(1, 5, BucketType.user)
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("Can't find the memeber you mentioned.")

    @command(name="say", aliases=["echo"])
    @cooldown(1, 5, BucketType.user)
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @command(name="fact")
    @cooldown(1, 10, BucketType.user)
    async def animal_fact(self, ctx, animal:str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):

            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'bird' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} fact",
                                  description=data["fact"],
                                  color=ctx.author.color)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are available for that animal.")

    @animal_fact.error
    async def animal_fact_error(self, ctx, animal:str):
        pass

    @command(name="hail", aliases=["heil"])
    async def hail(self, ctx):
        await ctx.send(f"<:Jebaited:821339691760222208>fuq you I wont do that<:pepeLaught:812263170911240214>. Your mum gay <a:yourmom:808076848188751874> {ctx.author.mention}.")

    @command(name="nudes", aliases=["horny"])
    async def nudes(self, ctx):
        await ctx.send(f"<:Jebaited:821339691760222208>fuq you I wont do that<:pepeLaught:812263170911240214>. Go to horny jail <a:yourmom:808076848188751874> {ctx.author.mention}.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
        

def setup(bot):
    bot.add_cog(Fun(bot))