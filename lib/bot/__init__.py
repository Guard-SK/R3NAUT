from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions


from discord import Intents

from ..db import db

PREFIX = "3"
OWNER_IDS = [544573811899629568]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

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
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        intents = Intents.default()
        intents.members = True

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS
            #intents=Intents.all(), #doesnt work
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

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
        print("R3NAUT connected")

    async def on_dissconnect(self):
        print("R3NAUT disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        else:
            await self.stdout.send("An error occured!")
        raise
        

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Wrong command, try again!")
        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(647170092467224646)
            self.stdout = self.get_channel(818107256213471242)
            self.scheduler.add_job(self.print_message, CronTrigger(second=0))
            self.scheduler.start()

            await self.stdout.send("Online!")

            #user = self.get_user(431116940568952842)
            #await user.send('Ak vidis tuto spravu napis mi')
            
            #embed = Embed(title="I m online!", description="This is a test for embeds!", color=0xFF0000, timestamp=datetime.utcnow())
            #fields = [("Name", "Value", True),
                     #("Another field", "2nd field", True),
                     #("A non-inline field", "whatever is this", False)]
            #for name, value, inline in fields:
                #embed.add_field(name=name, value=value, inline=inline)
            #embed.set_author(name="𝓖𝓪𝓶𝓲𝓷𝓰 𝓵𝓪𝓲𝓻", icon_url=self.guild.icon_url)
            #embed.set_footer(text="just a footer!")
            #embed.set_thumbnail(url=self.guild.icon_url)
            #embed.set_image(url=self.guild.icon_url)
            #await channel.send(embed=embed)

            #channel = self.get_channel(694513486880964608)
            #await channel.send("VI VON ZULUL")

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("R3NAULT ready")

        else: 
            print("R3NAULT reconnected")


    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)
 


bot = Bot()