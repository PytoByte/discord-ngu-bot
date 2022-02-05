import discord
from discord.ext import commands, tasks
import DataMaster as dm

import os

async def isAdmin(ctx):
    yes = False
    for role in ctx.author.roles:
        if role.id==dm.get_main_data()['dinamic']['adminRoleID']:
            yes=True
            break
    if yes==False:
        embed = discord.Embed(
            title = 'Ошибка',
            description = 'Оказано в доступе',
            colour = discord.Colour.red()
        )
        await ctx.send(embed=embed)
    return yes

class developer(commands.Cog, name='Для разработчика'):
    inHelp = True #Вывести ли команды в меню помощи?
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='версия', description=f'Выводит версию бота', brief='')
    async def version(self, ctx):
        if await isAdmin(ctx):
            mainData = dm.get_main_data()
            await ctx.send('Версия бота: '+mainData['const']['version'])

    @commands.command(name='базы', description=f'Отправляет все базы данных имеющиеся в боте', brief='')
    async def get_bases(self, ctx):
        if await isAdmin(ctx):
            mainData = dm.get_main_data()
            await ctx.send('', files=dm.get_all_data())


    @commands.command(name='загрузить_базу', description=f'загружает базу по файлу json (НЕ ПРАВИЛЬНО ЗАГРУЖЕННЫЙ ФАЙЛ ПОВРЕДИТ РАБОТУ БОТА)', brief='[путь к базе] + json файл')
    async def dump_base(self, ctx, url):
        if await isAdmin(ctx):
            await dm.dump_from_discord_json(url, ctx.message.attachments[0])
       

def setup(bot):
    bot.add_cog(developer(bot))
