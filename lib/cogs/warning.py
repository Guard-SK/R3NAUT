import aiofiles
import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import has_permissions

class Warning(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}

    @command(name="warn", aliases=['warning', 'w'])
    @has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member=None, *, reason=None):
        if member is None:
            return await ctx.send("The provided member could not be found or you forgot to provide one.")
            
        if reason is None:
            return await ctx.send("Please provide a reason for warning this user.")

        try:
            first_warning = False
            self.bot.warnings[ctx.guild.id][member.id][0] += 1
            self.bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

        except KeyError:
            first_warning = True
            self.bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

        count = self.bot.warnings[ctx.guild.id][member.id][0]

        async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
            await file.write(f"{member.id} {ctx.author.id} {reason}\n")

        await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

    @command(name="warnings")
    @has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member=None):
        if member is None:
            return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
        embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
        try:
            i = 1
            for admin_id, reason in self.bot.warnings[ctx.guild.id][member.id][1]:
                admin = ctx.guild.get_member(admin_id)
                embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
                i += 1

            await ctx.send(embed=embed)

        except KeyError: # no warnings
            await ctx.send("This user has no warnings.")

    @Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.warnings[guild.id] = {}
        
    @Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
                pass

            self.bot.warnings[guild.id] = {}

        for guild in self.bot.guilds:
            async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
                lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    self.bot.warnings[guild.id][member_id][0] += 1
                    self.bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    self.bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 

        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("warning")        

def setup(bot):
    bot.add_cog(Warning(bot))