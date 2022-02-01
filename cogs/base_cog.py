import discord
from discord.ext import commands, tasks
import DataMaster as dm

class base(commands.Cog):
    inHelp = False #Вывести ли команды в меню помощи?
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nothing(self, ctx, *, nickname):
        d = dm.load_data('saves.json')
        d[nickname] = {'discord':None, 'playerStats':None}
        dm.dump_data('saves.json', d)
        

def setup(bot):
    print('*base_cog лишь пример и не используется как рабочий винтик')
    #bot.add_cog(base(bot))

