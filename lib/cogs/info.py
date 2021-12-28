from typing import Optional
from datetime import datetime

from discord.ext.commands import Cog
from discord import Forbidden
from discord.ext.commands import command
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord import Embed, Member
import discord

class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="userinfo", aliases=["ui"])
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed=Embed(title="User information", color=target.colour, timestamp=datetime.utcnow())
        embed.set_thumbnail(url=target.avatar_url)
        embed=discord.Embed(title="User information")
        embed.add_field(name="ID", value=target.id, inline=False)
        embed.add_field(name="Name", value=str(target), inline=True)
        embed.add_field(name="Bot?", value=target.bot, inline=True)
        embed.add_field(name="Top role", value=target.top_role.mention, inline=True)
        embed.add_field(name="Status", value=str(target.status).title(), inline=True)
        embed.add_field(name="Activity", value=f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", inline=True)
        embed.add_field(name="Created at", value=target.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Joined at", value=target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Boosted", value=bool(target.premium_since), inline=True)
        await ctx.send(embed=embed)

    @command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    async def server_info(self, ctx):
        embed = Embed(title="Server information",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835170005200011345/835187033936363601/Black_and_Red_Gaming_Logo.gif")

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, False),
				  ("Owner", ctx.guild.owner, True),
				  ("Region", ctx.guild.region, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", False),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="botinfo", aliases=["bi"])
    async def R3NAUT_info(self, ctx):
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
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("info")

def setup(bot):
    bot.add_cog(Info(bot))