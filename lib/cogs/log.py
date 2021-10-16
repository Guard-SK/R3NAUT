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
            embed.set_footer(text=f"ID: {after.id}")
            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)


        if before.avatar_url != after.avatar_url:
            embed = Embed(title=f"Member update!",
                          description=f"{after.name} changed avatar. New image is below, old to the right.",
                          colour=0xffc800,
                          timestamp=datetime.utcnow())

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_footer(text=f"ID: {after.id}")
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
            embed.set_footer(text=f"ID: {after.id}")
            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title="Role updates",
                          colour=0xff6f00,
                          timestamp=datetime.utcnow())
            
            embed.set_author(name=f"{before.name}", url=before.avatar_url)
            embed.set_footer(text=f"ID: {after.id}")

            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                      ("After", ", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(f"{after.mention}")
            await self.logs_channel.send(embed=embed)
            
    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.id == BotID:
            if not before.author == self.bot.user:
                if not before.author.bot:
                    embed = Embed(title=f"Message **edit** by {after.author.display_name} in {after.channel}",
                                description=f"<:down:893119176749760562>**old**<:down:893119176749760562>\n{before.content}\n<:down:893119176749760562>**new**<:down:893119176749760562>\n{after.content}",
                                colour=0xff6f00,
                                timestamp=datetime.utcnow())

                    embed.set_footer(text=f"ID: {after.author.id}")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/888434526739640382/6e35ef7687065eb1e4c037781f3c4cdc_1.png")

                    await self.logs_channel.send(f"|{after.author.mention}|<#{after.channel.id}>|")
                    await self.logs_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 647170092467224646:
            embed = discord.Embed(title=f"Member join", description=f"{member.mention} alias {member.guild.name}", color=0x0bef1a, timestamp=datetime.utcnow())  
            embed.set_footer(text=f"ID: {member.id}")
            await self.logs_channel(embed=embed)
            
    @Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 647170092467224646:
            embed = discord.Embed(title=f"Member left", description=f"{member.mention} alias {member.guild.name}", color=0xff0000, timestamp=datetime.utcnow())
            embed.set_footer(text=f"ID: {member.id}")
            await self.logs_channel(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.id == BotID:
            if not message.content == "3ahelp" or "3help" or "3say" or "3dm" or "ahelp" or "help" or "say" or "dm":
                if not message.author.bot:
                    embed = Embed(title=f"Message **deletion** by {message.author.display_name} in {message.channel}",
                                description=f"Content:\n {message.content}",
                                colour=0xff6f00,
                                timestamp=datetime.utcnow())

                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/888433648490123324/trash-can-web-32257.png")

                    await self.logs_channel.send(f"{message.author.mention}")
                    await self.logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Log(bot))