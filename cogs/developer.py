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

    @commands.command(name='сохр', description=f'Отправляет базу с сохранениями в виде файла', brief='')
    async def get_saves_file(self, ctx):
        if await isAdmin(ctx):
            await ctx.send('', files=dm.get_file_saves())


    @commands.command(name='загр_сохр', description=f'Загружает сохранения по файлу json', brief='+ json файл')
    async def dump_saves_base(self, ctx):
        if await isAdmin(ctx):
            await dm.dump_saves_from_discord_json(ctx.message.attachments[0])
            await ctx.send('Готово')
       

def setup(bot):
    bot.add_cog(developer(bot))
