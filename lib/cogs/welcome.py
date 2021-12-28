from discord.ext.commands import Cog
from discord import Forbidden
from discord.ext.commands import command
import discord
from discord import Embed
from datetime import datetime
from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome = self.bot.get_channel(688497338347552774)
        self.bot_welcome = self.bot.get_channel(835169929249947651)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener() 
    async def on_member_join(self, member):
        if member.guild.id == 647170092467224646:
            db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
            embed = discord.Embed(title=f"Welcome to **{member.guild.name}** <:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>", description=f"{member.mention}", color=0xff0000, timestamp=datetime.utcnow()) 
            embed.set_author(name="R3NAUT", url="https://cdn.discordapp.com/attachments/835185429497380965/835187630576107550/Dizajn_bez_nazvu_3.png", icon_url="https://cdn.discordapp.com/attachments/835185429497380965/835187630576107550/Dizajn_bez_nazvu_3.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/912364879258742824/ezgif.com-gif-maker_13.gif")
            embed.add_field(name="Rules", value="don't forget to go to <#647170266568327179>, read the rules and **click on the reaction!**", inline=True)
            embed.add_field(name="Come", value="and head over to <#694513486880964608> to say hi!", inline=True)
            embed.set_footer(text=" ")
            await self.bot.get_channel(688497338347552774).send(f"Welcome {member.mention}!")
            await self.bot.get_channel(688497338347552774).send(embed=embed)

            try:
                embed=discord.Embed(title=f"Welcome {member.mention} to **{member.guild.name}** <:peepohey:806962515152994406>", description=f"We are glad you came!", color=0x66a136, timestamp=datetime.utcnow())

                #await member.send(f"Welcome to **{member.guild.name}**! We are glad you came!")

            except Forbidden:
                pass

        else:
            embed = discord.Embed(title=f"Welcome to **{member.guild.name}** <:pepeLaught:812263170911240214><a:TeaTime:806197564302819359>", description=f"{member.mention}", color=0xff0000, timestamp=datetime.utcnow()) 
            embed.set_author(name="R3NAUT", url="https://cdn.discordapp.com/attachments/835185429497380965/835187630576107550/Dizajn_bez_nazvu_3.png", icon_url="https://cdn.discordapp.com/attachments/835185429497380965/835187630576107550/Dizajn_bez_nazvu_3.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/912364879258742824/ezgif.com-gif-maker_13.gif")
            embed.add_field(name="Rules", value="don't forget to go to <#647170266568327179>, read the rules and **click on the reaction!**", inline=True)
            embed.add_field(name="Come", value="and head over to <#694513486880964608> to say hi!", inline=True)
            embed.set_footer(text=" ")
            await self.bot.get_channel(835169929249947651).send(f"Welcome {member.mention}!")
            await self.bot.get_channel(835169929249947651).send(embed=embed)
            await member.add_roles(member.guild.get_role(826846732271878155))

        #await member.add_roles(member.guild.get_role(826846732271878155))



    @Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 647170092467224646:
            db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
            embed=discord.Embed(title="Bye", description=f"{member.mention} has left {member.guild.name} <:sadge:806195778565570580>", color=0xff0000, timestamp=datetime.utcnow())
            embed.set_author(name="R3NAUT", icon_url="https://cdn.discordapp.com/attachments/835185429497380965/835187630576107550/Dizajn_bez_nazvu_3.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/626418163042746380/841302882984394772/ezgif.com-gif-maker_3.gif")
            await self.bot.get_channel(688497338347552774).send(f"Bye {member.mention}!")
            await self.bot.get_channel(688497338347552774).send(embed=embed)

        else:
            embed=discord.Embed(title="Bye", description=f"{member.mention} has left {member.guild.name} <:sadge:806195778565570580>", color=0xff0000, timestamp=datetime.utcnow())
            embed.set_author(name="R3NAUT", icon_url="https://cdn.discordapp.com/attachments/835185429497380965/835187630576107550/Dizajn_bez_nazvu_3.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/629382706299666432/912364879258742824/ezgif.com-gif-maker_13.gif")
            await self.bot.get_channel(835169929249947651).send(f"Bye {member.mention}!")
            await self.bot.get_channel(835169929249947651).send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))

    #835169929249947651