from discord import Embed, Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime
import discord

BotID = 817768019086016543

class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.logs_channel = self.bot.get_channel(732624357762793502)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed=discord.Embed(title="Member update!", description="Username change", color=0xffc800, timestamp=datetime.utcnow())
            embed.set_author(name=f"{before.name}", url=before.avatar_url)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/837700710539591740/6e35ef7687065eb1e4c037781f3c4cdc.png")
            embed.add_field(name="Before", value=f"{before.name}", inline=False)
            embed.add_field(name="After", value=f"{after.name}", inline=False)
            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)


        if before.avatar_url != after.avatar_url:
            embed = Embed(title=f"Member update!",
						  description=f"{after.name} changed avatar. New image is below, old to the right.",
						  colour=0xffc800,
						  timestamp=datetime.utcnow())

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed=discord.Embed(title="Member update!", description="Discriminator change", color=0xffc800, timestamp=datetime.utcnow())
            embed.set_author(name=f"{before.name}", url=before.avatar_url)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/837700710539591740/6e35ef7687065eb1e4c037781f3c4cdc.png")
            embed.add_field(name="Before", value=f"{before.discriminator}", inline=False)
            embed.add_field(name="After", value=f"{after.discriminator}", inline=False)
            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)


    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed=discord.Embed(title="Member update!", description="Nickname change", color=0xffc800, timestamp=datetime.utcnow())
            embed.set_author(name=f"{before.name}", url=before.avatar_url)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/837700710539591740/6e35ef7687065eb1e4c037781f3c4cdc.png")
            embed.add_field(name="Before", value=f"{before.display_name}", inline=False)
            embed.add_field(name="After", value=f"{after.display_name}", inline=False)
            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title="Role updates",
						  colour=0xff6f00,
						  timestamp=datetime.utcnow())
            
            embed.set_author(name=f"{before.name}", url=before.avatar_url)

            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
					  ("After", ", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)
            
    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                embed = Embed(title="Message edit",
							  description=f"Edit by {after.author.display_name}.",
							  colour=0xff6f00,
							  timestamp=datetime.utcnow())

                fields = [("Before", before.content, False),
						  ("After", after.content, False)]

                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/837700710539591740/6e35ef7687065eb1e4c037781f3c4cdc.png")

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.logs_channel.send(f"{after.mention}")
                await self.logs_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == BotID:
            if message.author.bot:
                embed = Embed(title="Message deletion",
                            description=f"Deleted by {message.author.display_name} in {message.channel}.",
                            colour=0xff6f00,
                            timestamp=datetime.utcnow())

                fields = [("Content", message.content, False)]

                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/837723544863244338/unnamed_3.png")

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.logs_channel.send(f"{message.author.mention}")
                await self.logs_channel.send(embed=embed)
            else:
                pass
        else:
            pass

def setup(bot):
    bot.add_cog(Log(bot))