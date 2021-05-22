from typing import Optional
from datetime import datetime
from datetime import timedelta
from asyncio import sleep

from better_profanity import profanity
import discord
from discord.ext.commands import command
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import has_permissions, bot_has_permissions, CheckFailure
from discord import Forbidden
from discord import Embed, Member

from ..db import db

profanity.load_censor_words_from_file("./data/profanity.txt")

class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot
            
    async def kick_members(self, ctx, targets, reason):
        if not len(targets):
            await ctx.send("One or more required arguments are missing.")
        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator:
                    try:
                        await target.send(f"You were kicked by {ctx.author.display_name} because {reason}")
                    except Forbidden:
                        pass
                    await target.kick(reason=reason)
                    embed=Embed(title="Member kicked", colour=0xff0000, timestamp=datetime.utcnow())
                    embed.set_author(name=ctx.author.display_name)
                    embed.set_thumbnail(url=target.avatar_url)
                    embed.add_field(name="Member", value=f"{target.name} a.k.a. {target.display_name}", inline=False),
                    embed.add_field(name="Actioned by", value=ctx.author.display_name, inline=False),
                    embed.add_field(name="Reason", value=reason, inline=False)
                    await self.logs_channel.send(embed=embed)

                else:
                    await ctx.send(f"Somehow {target.display_name} could not be kicked.")
    
    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing.")

        else:
            await self.kick_members(ctx.message, targets, reason)
            await ctx.send("Action complete.")
    
    @kick_command.error
    async def kick_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You don't have permission for that.")

###############################################################################################

    async def ban_members(self, ctx, targets, reason):
        if not len(targets):
            await ctx.send("One or more required arguments are missing.")
        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator:
                    try:
                        await target.send(f"You were banned by {ctx.author.display_name} because {reason}")
                    except Forbidden:
                        pass
                    await target.ban(reason=reason)
                    embed=Embed(title="Member banned", colour=0xff0000, timestamp=datetime.utcnow())
                    embed.set_author(name=ctx.author.display_name)
                    embed.set_thumbnail(url=target.avatar_url)
                    embed.add_field(name="Member", value=f"{target.name} a.k.a. {target.display_name}", inline=False),
                    embed.add_field(name="Actioned by", value=ctx.author.display_name, inline=False),
                    embed.add_field(name="Reason", value=reason, inline=False)
                    await self.logs_channel.send(embed=embed)

                else:
                    await ctx.send(f"Somehow {target.display_name} could not be banned.")
    
    @command(name="ban")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing.")

        else:
            await self.ban_members(ctx.message, targets, reason)
            await ctx.send("Action complete.")
    
    @ban_command.error
    async def ban_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You don't have permission for that.")

##############################################################################################################################################

    @command(name="clear", aliases=["purge", "nuke"])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
                                                  check=_check)

                await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)

        else:
            await ctx.send("The limit provided isn't within acceptable bounds. You can clear from 1 to 100.")

##############################################################################################################################################

    async def mute_members(self, message, targets, hours, reason):
        unmutes = []

        for target in targets:
            if not self.mute_role in target.roles:
                if message.guild.me.top_role.position > target.top_role.position:
                    role_ids = ",".join([str(r.id) for r in target.roles])
                    end_time = datetime.utcnow() + timedelta(seconds=hours) if hours else None

                    db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
                            target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())

                    await target.edit(roles=[self.mute_role])

                    embed = Embed(title="Member muted",
                                colour=0xDD2222,
                                timestamp=datetime.utcnow())

                    embed.set_thumbnail(url=target.avatar_url)

                    fields = [("Member", target.display_name, False),
                            ("Actioned by", message.author.display_name, False),
                            ("Duration", f"{hours:,} hour(s)" if hours else "Indefinite", False),
                            ("Reason", reason, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.logs_channel.send(embed=embed)

                    if hours:
                        unmutes.append(target)

        return unmutes

    @command(name="mute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_messages=True)
    async def mute_command(self, ctx, targets: Greedy[Member], hours: Optional[int], *,
                           reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing.")

        else:
            unmutes = await self.mute_members(ctx.message, targets, hours, reason)
            await ctx.send("Action complete.")

            if len(unmutes):
                await sleep(hours)
                await self.unmute_members(ctx.guild, targets)

    @mute_command.error
    async def mute_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform that task.")

    async def unmute_members(self, guild, targets, *, reason="Mute time expired."):
        for target in targets:
            if self.mute_role in target.roles:
                role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
                roles = [guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]

                db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)

                await target.edit(roles=roles)

                embed = Embed(title="Member unmuted",
                              colour=0xDD2222,
                              timestamp=datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [("Member", target.display_name, False),
                          ("Reason", reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.logs_channel.send(embed=embed)

    @command(name="unmute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_messages=True)
    async def unmute_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments is missing.")

        else:
            await self.unmute_members(ctx.guild, targets, reason=reason)

##############################################################################################################################################

    @command(name="addprofanity", aliases=["addswears", "addcurses"])
    @has_permissions(manage_guild=True)
    async def add_profanity(self, ctx, *words):
        with open("./data/profanity.txt", "a", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in words]))

        profanity.load_censor_words_from_file("./data/profanity.txt")
        embed=discord.Embed(title="Profanity added", description="Word was added to the list", color=0x05e131)
        await ctx.send(embed=embed)

    @command(name="delprofanity", aliases=["delswears", "delcurses"])
    @has_permissions(manage_guild=True)
    async def remove_profanity(self, ctx, *words):
        with open("./data/profanity.txt", "r", encoding="utf-8") as f:
            stored = [w.strip() for w in f.readlines()]

        with open("./data/profanity.txt", "w", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in stored if w not in words]))

        profanity.load_censor_words_from_file("./data/profanity.txt")
        embed=discord.Embed(title="Profanity deleted", description="Word was deleted from the list", color=0xc91313)
        await ctx.send(embed=embed)


    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            if message.author.guild_permissions.manage_guild:
                if profanity.contains_profanity(message.content):
                    await message.delete()
                    await message.channel.send("You can't use that word here!")
                else:
                    pass
            else:
                pass
        else:
            pass


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.logs_channel = self.bot.get_channel(732624357762793502)
            self.modmail_channel = self.bot.get_channel(839492062914412544)
            self.mute_role = self.bot.guild.get_role(688499497894281370)

            self.bot.cogs_ready.ready_up("mod")

def setup(bot):
    bot.add_cog(Mod(bot))
