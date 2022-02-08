import discord
from discord.ext import commands, tasks

from datetime import datetime as dt

from player_parser import Parser_tracker_gg
import DataMaster as dm

global data
data = dm.get_main_data()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=data['dinamic']['prefix'], intents=intents)


@bot.event
async def on_ready():
    bot.remove_command('help')
    
    print('Загрузка винтиков...')
    
    cogsList = dm.get_cogs()
    for c in cogsList:
        gap = ' '*len(c)
        print(c)
        bot.load_extension(f'cogs.{c}')
        
    print('Винтики загружены!\n')

    await (bot.get_user(data['const']['userToMention'])).send('Бот запущен\n'+str(dt.now()))


@bot.command(name='помощь')
async def help(ctx):
    cogs_dict = bot.cogs
    text = '**Встроенные команды**\n'
    text +='- '+str(bot.command_prefix)+'помощь\n- Выводит меню помощи\n\n'
    for cog_name in cogs_dict:
        cog = cogs_dict[cog_name]
        try:
            if cog.inHelp!=True:
                continue
        except AttributeError as er:
            print('Игнорирую ошибку: '+er)
        text+='**'+str(cog_name)+'**\n'
        groups = cog.get_commands()
        for group in groups:
            text+='- '+str(bot.command_prefix)+str(group.name)+' '+str(group.brief)+'\n'
            text+='- '+str(group.description)+'\n\n'
            try:
                coms = group.commands
                for com in coms:
                    text+='-- '+str(bot.command_prefix)+str(com.parent)+' '+str(com.name)+' '+str(com.brief)+'\n-- '+str(com.description)+'\n\n'
            except:
                pass
                
    embed = discord.Embed(
        title = 'Меню помощи',
        description = text,
        colour = discord.Colour.blue()
    )
    await ctx.send(embed=embed)
    

bot.run(dm.load_data('const/token.json')['TOKEN'])
