import discord
from discord.ext import commands, tasks
import DataMaster as dm

class test_cog(commands.Cog):
    inHelp = False
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mention_test(self, ctx, mention):
        discordID = mention.replace('<@!', '')
        discordID = discordID.replace('>','')
        await ctx.send(discordID)
        

def setup(bot):
    bot.add_cog(test_cog(bot))

