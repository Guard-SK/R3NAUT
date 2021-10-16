
from random import choice, randint
from re import search
from typing import Optional
from discord.errors import HTTPException
from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
from re import search
from better_profanity import profanity
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from time import time
from datetime import datetime
import discord


profanity.load_censor_words_from_file("./data/profanity.txt")

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.logs_channel = self.bot.get_channel(732624357762793502)
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    @cog_ext.cog_slash(name='botinfo', 
                    description='Tells you interesting information about R3NAUT.', 
                    guild_ids=[807971983081472000, 647170092467224646])
    async def R3NAUT_info(self, ctx: SlashContext):
        embed=Embed(title="INFO ABOUT R3NAUT", description="This is a info about me", timestamp=datetime.utcnow())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/845639956008534046/R3NAUT.png")
        embed.add_field(name="Born in", value="6/3/2021 14:38:09", inline=False)
        embed.add_field(name="Created by", value="<@544573811899629568>", inline=False)
        embed.add_field(name="ID", value="817768019086016543", inline=True)
        embed.add_field(name="Programed in", value="Visual Studio Code|Python 3.9.2 64-bit", inline=True)
        embed.add_field(name="Database", value="SQLite", inline=True)
        embed.add_field(name="Stored in", value="Github = https://github.com/Guard-SK/R3NAUT", inline=False)
        embed.add_field(name="Hosted", value="localy on Raspberry pi 3B+", inline=True)  
        await ctx.send(embed=embed) 

    @cog_ext.cog_slash(name='ping', 
                    description='Tells you DWPS latency and overall response time.', 
                    guild_ids=[807971983081472000, 647170092467224646])
    async def ping(self, ctx: SlashContext):
        start = time()
        message = await ctx.send(f"Pong! DWSP latency is: {self.bot.latency*1000:,.0f} ms.")
        end = time()

        await message.edit(content=f"Pong! DWSP latency is: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")
    
    @cog_ext.cog_slash(name='test', 
    description='hehehehee', 
    guild_ids=[807971983081472000], 
    options=[
        create_option(
            name="option", 
            description="something", 
            required=True,
            option_type=3, 
            choices=[
                create_choice(
                    name="Word",
                    value="word"
                ),
                create_choice(
                    name="Word2",
                    value="word2"
                )
            ]
        )    
    ]
)
    async def test(self, ctx: SlashContext, option: str):
        await ctx.send(option)

    @cog_ext.cog_slash(name='hi', 
                       description='say hello to R3NAUT', 
                       guild_ids=[807971983081472000, 647170092467224646])
    async def hi(self, ctx: SlashContext):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya', 'Sup', 'Ciao', '<:peepohey:806962515152994406>'))} {ctx.author.mention}!")

    @cog_ext.cog_slash(name='hello', 
                       description='say hello to R3NAUT', 
                       guild_ids=[807971983081472000, 647170092467224646])
    async def hello(self, ctx: SlashContext):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya', 'Sup', 'Ciao', '<:peepohey:806962515152994406>'))} {ctx.author.mention}!")

    @command(name="hello", aliases=["hi", "sup"])
    @cooldown(1, 1, BucketType.user)
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya', 'Sup', 'Ciao', '<:peepohey:806962515152994406>'))} {ctx.author.mention}!")

    @command(name="ahoj", aliases=["čau", "cav", "cau"])
    @cooldown(1, 1, BucketType.user)
    async def povedz_ahoj(self, ctx):
        await ctx.send(f"{choice(('<:peepohey:806962515152994406>', 'Ahoj', 'Čau', 'Hej', 'Cav', 'Sup', 'Ciao'))} {ctx.author.mention}!") #'My name is Jeff', 'Hello, my name is R3NAUT, and Im developed by Guard_SK', 'Hello, my name is R3NAUT', 'Whats going on?', 'I wasnt ready for that..'     

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
        if not profanity.contains_profanity(message):
            await ctx.message.delete()
            await ctx.send(message)

        else:
            await message.channel.send("You can't use that word here!", delete_after=10)

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

    @command(name="dm", aliases=["direct message", "send"])
    @cooldown(1, 60, BucketType.user)
    async def send_dm(self, ctx, member: discord.Member, *, content):
        if not search(self.url_regex, content):
            channel = await member.create_dm()
            await channel.send(f"{content} \n \n Message sent by: {ctx.author.mention}")
            await ctx.send("Message was sent")

        else:
            await ctx.send("You cannot send links with this command!", delete_after=10)
            embed=discord.Embed(title="Link in dm", description="Someone send link to with dm command. Look at that!", color=0xff0000)
            embed.add_field(name="Content:", value=f"{content}", inline=False)
            await ctx.send(embed=embed)



    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
        

def setup(bot):
    bot.add_cog(Fun(bot))