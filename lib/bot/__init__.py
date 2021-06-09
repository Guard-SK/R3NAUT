from asyncio import sleep
from datetime import datetime
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions
from discord.ext import commands
from discord import Intents
import discord
from discord.ext.commands.errors import MissingPermissions

from ..db import db

OWNER_IDS = [544573811899629568]
COGS = [path[:-3] for path in os.listdir('./lib/cogs') if path[-3:] == '.py']
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot, message):
	prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
	return when_mentioned_or(prefix)(bot, message)



# target_channel_id = 694513486880964608

# @tasks.loop(hours=2)
# async def called_every_hour():
#     message_channel = bot.get_channel(694513486880964608)
#     print(f"Got channel {message_channel} for teatime") 
#     await message_channel.send(f"{choice(('<:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>', '<a:yourmom:808076848188751874><:OMEGALUL:797814371609739275>', '<:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>   <:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>   <:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>', '<a:hackerCD:835166860239568947>'))}")

# @called_every_hour.before_loop
# async def before():
#     await bot.wait_until_ready()
#     print("Finished waiting")

# called_every_hour.start()

# target_channel_id = 778562691810852884 #818107256213471242

# @tasks.loop(hours=2)
# async def called_every_hour():
#     message_channel = bot.get_channel(778562691810852884)
#     print(f"Got channel {message_channel} for teatime")
#     await message_channel.send(f"{choice(('<:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>', '<a:yourmom:808076848188751874><:OMEGALUL:797814371609739275>', '<:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>   <:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>   <:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>'))}")

# @called_every_hour.before_loop
# async def before():
#     await bot.wait_until_ready()
#     print("Finished waiting")

# called_every_hour.start()

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler(timezone='Europe/Bratislava')


        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=get_prefix, 
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)", 
                    ((guild.id,) for guild in self.guilds))

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf--8") as tf:
            self.TOKEN = tf.read()

        print("Running project R3NAUT...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if self.ready:
            if ctx.command is not None and ctx.guild is not None:
                await self.invoke(ctx)

        else:
            await ctx.send("I'm not ready to recieve commands. Please wait...")

    async def print_message(self):
        channel = self.get_channel(826362524713615370)
        await channel.send("Saving database...")

    async def on_connect(self):
        self.update_db()
        print("R3NAUT connected")

    async def on_dissconnect(self):
        print("R3NAUT disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error occured.")
        raise
        

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"<a:no_entry:826849755916140574>Cool down man <a:melting_ice:826761004980764702>. Try again in {exc.retry_after:,.2f} secs.<a:no_entry:826849755916140574>")

        elif isinstance(exc.original, HTTPException):
            await ctx.send("Unable to send message.")

        elif isinstance(exc.original, Forbidden):
            await ctx.send("I am not allowed to do that.")

        elif isinstance(exc, MissingPermissions):
            await ctx.send("You don't have permission to do that.")

        else:
            raise exc

    send_time='09:30'
    message_channel_id='818107256213471242'

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(647170092467224646)
            self.stdout = self.get_channel(818107256213471242)
            self.scheduler.add_job(self.print_message, CronTrigger(second=0, timezone='Europe/Bratislava'))
            self.scheduler.start()
            await bot.change_presence(activity=discord.Game(name="League of Developers|3help"))

            self.update_db()
            
            # embed = Embed(title="I m online!", description="This is a test for embeds!", color=0xFF0000, timestamp=datetime.utcnow())
            # fields = [("Name", "Value", True),
            #          ("Another field", "2nd field", True),
            #          ("A non-inline field", "whatever is this", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name="𝓖𝓪𝓶𝓲𝓷𝓰 𝓵𝓪𝓲𝓻", icon_url=self.guild.icon_url)
            # embed.set_footer(text="just a footer!")
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # await self.stdout.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Online!")
            self.ready = True
            print("R3NAUT ready")

        else: 
            print("R3NAUT reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            if isinstance(message.channel, DMChannel):
                if len(message.content) < 50:
                    await message.channel.send("Your message should be more then 50 characters long.")

                elif len(message.content) >= 1024:
                    await message.channel.send("Your message can't be more than 1024 charasters long, because fields in embed can't be longer than 1024 characters.")

                else:
                    embed=Embed(title="Modmail", colour=message.author.colour, timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=message.author.avatar_url)
                    embed.add_field(name="Member", value=message.author.display_name, inline=False)
                    embed.add_field(name="Message", value=message.content, inline=False)
                    mod = self.get_cog("Mod")
                    await mod.modmail_channel.send(embed=embed)
                    await message.channel.send("Message relayed to moderators.")
            else:  
                await self.process_commands(message)
 


bot = Bot()