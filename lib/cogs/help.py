import asyncio

from discord.ext.commands import has_permissions

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime

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
		embed.add_field(name="Commands", value=f"```addprofanity|addswears|addcurses <words>``` - add forbidden words. **Permissions: Admin and higher** \n ```delprofanity|delswears|delcurses <words>``` - delete forbidden words. **Permissions: Admin and higher** \n ```mute <member> <time in minutes(optional)>``` - deletes all roles from mentioned user and adds a mute role. If you typed time as well, bot will delete the roles and add the old once back. **Permissions: Moderator and higher** \n ```unmute <member>``` - deletes muted role and adds old roles back. **Permissions: Moderator and higher** \n ```clear|purge|nuke <number> <member(s)(optional)>``` - clears number of messages you typed. If you mentioned user, the bot will clear all messages within the number you typed that are written by user(s) you mentioned. **Permissions: Moderator and higher** \n ```kick <member> <reason>``` - kick user you mentioned. **Permission: Moderator and above** \n ```ban <member> <reason>``` - bans member you mentioned. **Permission: Staff and higher**")
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