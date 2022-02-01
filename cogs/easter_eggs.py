import discord
from discord.ext import commands, tasks
import DataMaster as dm
from random import randint as ri

class easter_eggs(commands.Cog, name='Пасхалки'):
    inHelp = False
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author==self.bot.user:
            return

        if message.content.count('иди нахуй')>0 or message.content.count('Иди нахуй')>0:
            await message.channel.send(f'Нет ты иди нахуй {message.author.name}!', delete_after=5)
            await message.delete()
            return

    @commands.command(name='скам')
    async def scam(self, ctx, mention):
        luck = ri(0,1)
        if luck==1:
            discordID = mention.replace('<@!', '')
            discordID = discordID.replace('>','')
            if discordID.isdigit()==False:
                return
            else:
                discordID = int(discordID)
            scamPrice = ri(10, 100000)
            user = self.bot.get_user(discordID)
            senderMention= ctx.author.mention
            if user==None or senderMention==None:
                return
            money = ['валорант поинтов', 'гривен', 'рублей', 'долларов', 'белорусских рублей', 'бравл гемов', 'кредитов']
            embed = discord.Embed(
                title = 'Скам удался!',
                description = f'Вы заскамили `{user}`',
                colour = discord.Colour.green()
            )
            await ctx.send(embed=embed, delete_after=10)
            
            embed = discord.Embed(
                title = f'О нет!',
                description = f'Вас заскамил {senderMention} на **{scamPrice} {money[ri(0, len(money)-1)]}**',
                colour = discord.Colour.gold()
            )
            await user.send(embed=embed)
        else:
            defenders = ['ФСБ', 'ЦРУ', 'ФБР', 'РосКомНадзор', 'Интернет провайдер', 'Президент России', 'Президент Украины', 'Президент Казахстана', 'Президент Белоруссии', 'Орден иллюминатов', 'Здравый смысл', 'Мемасик из 2007', 'Инстапик джетки']
            embed = discord.Embed(
                title = 'Скам провалился!',
                description = f'{defenders[ri(0, len(defenders)-1)]} предотвратил скам',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete()
        
        
def setup(bot):
    bot.add_cog(easter_eggs(bot))

