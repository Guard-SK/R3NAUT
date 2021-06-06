import asyncio

from discord.ext.commands import has_permissions, MissingPermissions
from typing import Optional

from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime

from ..db import db

#####	Old help command	####

# def syntax(command):
# 	cmd_and_aliases = "|".join([str(command), *command.aliases])
# 	params = []

# 	for key, value in command.params.items():
# 		if key not in ("self", "ctx"):
# 			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

# 	params = " ".join(params)

# 	return f"`{cmd_and_aliases} {params}`"


# class HelpMenu(ListPageSource):
# 	def __init__(self, ctx, data):
# 		self.ctx = ctx

# 		super().__init__(data, per_page=4)

# 	async def write_page(self, menu, fields=[]):
# 		offset = (menu.current_page*self.per_page) + 1
# 		len_data = len(self.entries)

# 		embed = Embed(title="Help",
# 					  description="Welcome to the R3NAUT help dialog! For furthure command description type: help <command>.",
# 					  colour=0x1abc9c)
# 		embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
# 		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

# 		for name, value in fields:
# 			embed.add_field(name=name, value=value, inline=False)

# 		return embed

# 	async def format_page(self, menu, entries):
# 		fields = []

# 		for entry in entries:
# 			fields.append((entry.brief or "------------------------", syntax(entry)))

# 		return await self.write_page(menu, fields)


# class Help(Cog):
# 	def __init__(self, bot):
# 		self.bot = bot
# 		self.bot.remove_command("help")

# 	async def cmd_help(self, ctx, command):
# 		embed = Embed(title=f"Help with `{command}`",
# 					  description=syntax(command),
# 					  colour=ctx.author.colour)
# 		embed.add_field(name="Command description", value=command.help)
# 		await ctx.send(embed=embed)

# 	@command(name="help")
# 	async def show_help(self, ctx, cmd: Optional[str]):
# 		if cmd is None:
# 			menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
# 							 delete_message_after=True,
# 							 timeout=60.0)
# 			await menu.start(ctx)

# 		else:
# 			if (command := get(self.bot.commands, name=cmd)):
# 				await self.cmd_help(ctx, command)

# 			else:
# 				await ctx.send("That command does not exist.")

####	New help command	####

class Help(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command("help")

	#help command for normal users
	@command(name="help")
	async def cmd_help(self, ctx):

		#help embed
		embed=Embed(title="HELP", description="Welcome to the R3NAUT help dialog! \n Prefix = 3", color=0x15cb55, timestamp=datetime.utcnow())
		embed.add_field(name="-----Fun-----", value=f"```hi|hello|sup``` - greetings\n```fact <animal>``` - fact about dog, cat, panda, fox, bord or koala \n ```dice|roll <number of dices>d<highest number on the dice>``` - rolls dices of your choice \n ```say|echo <content>``` - repeat content of your message \n ```slap|hit <member> <reason>``` - slaps someone for some reason \n ```dm|direct message|send <member> <content>``` - sends a dm to someone", inline=False)
		embed.add_field(name="-----Info-----", value=f" ```serverinfo|si|guildinfo|gi``` - info about the server \n ```userinfo|ui <member>``` - gives you info about the user you mentioned\n```ping``` - pong\n```botinfo``` - info about R3NAUT")
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/845639956008534046/R3NAUT.png")

		#delete message you written to call help embed
		await ctx.message.delete()

		#delete help embed after 60 seconds
		msg = await ctx.send(embed=embed)
		await asyncio.sleep(60)
		await msg.delete()

	#a-team help command
	@command(name="ahelp")
	@has_permissions(manage_messages=True)
	async def cmd_help_admin(self, ctx):

		#ahelp embed
		embed=Embed(title="A-team HELP", description="Welcome to the R3NAUT a-team help dialog! \n Here you can see commands which you can use as you are one of the A-team", 
													  color=0xca1c1c, timestamp=datetime.utcnow())
		embed.add_field(name="Commands", value=f"```addprofanity|addswears|addcurses <words>``` - add forbidden words. **Permissions: Admin and higher** \n ```delprofanity|delswears|delcurses <words>``` - delete forbidden words. **Permissions: Admin and higher** \n ```mute <member> <time in minutes(optional)>``` - deletes all roles from mentioned user and adds a mute role. If you typed time as well, bot will delete the roles and add the old once back. **Permissions: Moderator and higher** \n ```unmute <member>``` - deletes muted role and adds old roles back. **Permissions: Moderator and higher** \n ```clear|purge|nuke <number> <member(s)(optional)>``` - clears number of messages you typed. If you mentioned user, the bot will clear all messages within the number you typed that are written by user(s) you mentioned. **Permissions: Moderator and higher** \n ```kick <member>``` - kick user you mentioned. **Permission: Moderator and above** \n ```ban <member>``` - bans member you mentioned. **Permission: Staff and higher**")
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/845639956008534046/R3NAUT.png")

		#delete message you written to call the help embed
		await ctx.message.delete()

		#sends embed through dm and sends message to chat that action is completed. The message 
		await ctx.author.send(embed=embed)
		msg2 = await ctx.send("Help command sent through DM! If message didn't arrived, turn on that users can DM you!")
		await asyncio.sleep(5)
		await msg2.delete()
		
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("help")

def setup(bot):
    bot.add_cog(Help(bot))