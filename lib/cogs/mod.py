from typing import Optional
from datetime import datetime
from datetime import timedelta

import discord
from discord.ext.commands import command
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import has_permissions, bot_has_permissions, CheckFailure
from discord import Forbidden
from discord import Embed, Member

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

    # @command(name="clear", aliases=["purge", "nuke"])
    # @bot_has_permissions(manage_messages=True)
    # @has_permissions(manage_messages=True)
    # async def clear_message(self, ctx, targets: Greedy[Member], limit: Optional[int] = 0):
    #     def _check(message):
    #         return not len(targets) or message.author in targets

    #     if 0 < limit <= 100:
    #         with ctx.channel.typing:
    #             await ctx.message.delete()
    #             deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14), check=_check)
    #             # embed=Embed(title="Messages clear", colour=0xff0000, timestamp=datetime.utcnow())
    #             # embed.set_author(name=ctx.author.display_name)
    #             # embed.add_field(name="Cleared", value=f"{deleted} messages.", inline=False),
    #             # embed.add_field(name="Actioned by", value=ctx.author.display_name, inline=False),
    #             await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)
    #             # await self.logs_channel.send(embed=embed)

    #     else:
    #         await ctx.send(f"The limit provided isn't within acceptable bounds. You can clear from 1 to 100 {ctx.mention}.")

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

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
                    self.logs_channel=self.bot.get_channel(732624357762793502)
                    self.modmail_channel=self.bot.get_channel(839492062914412544)
                    self.bot.cogs_ready.ready_up("mod")

def setup(bot):
    bot.add_cog(Mod(bot))
