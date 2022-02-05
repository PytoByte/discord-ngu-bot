import discord
from discord.ext import commands, tasks

from datetime import datetime as dt

import DataMaster as dm
from player_parser import Parser_tracker_gg as ptgg

async def give_rank(playerStats, bot):
    try:
        saves = dm.get_saves()
        rank_data = dm.load_data('dinamic/rank_data.json')
        
        user = saves[playerStats['nickname']]['discord']

        if user==None:
            print(f'Не обнаружен пользователь дс под ником {playerStats["nickname"]}')
            return False

        else:
            data = dm.get_main_data()
            guild = bot.get_guild(data['const']['guildID'])
            user = guild.get_member(user)
            userRoles = user.roles
            rank = (playerStats['rank'].split())[0]
            print(f"Ранг: {rank}")
            
            try:
                if rank=='Unrated' or rank=='Iron' or rank=='Bronze' or rank=='Silver' or rank=='Gold'or rank=='Platinum' or rank=='Diamond' or rank=='Immortal' or rank=='Radiant':
                    if userRoles.count(guild.get_role(rank_data[rank]))==0:
                        await user.add_roles(guild.get_role(rank_data[rank]))
                        print(f"Выдан ранг {rank}")
                elif rank.startswith('RR'):
                    rank='Immortal'
                    await user.add_roles(guild.get_role(rank_data[rank]))
                    print(f"Выдан ранг {rank}")
                else:
                    print(f'Неопознанный ранг {rank}')
                    
                for i in rank_data:
                    if userRoles.count(guild.get_role(rank_data[i]))==1 and rank!=i:
                        await user.remove_roles(guild.get_role(rank_data[i]))
                        print(f'Убран ранг {i}')
                return True
            
            except BaseException as error:
                print(f'Ошибка при выдаче ранга: {error}')
                return False
    except BaseException as error:
        print(f'Внезапная ошибка при выдаче ранга: {error}')
        return False


class parsing(commands.Cog, name='Сканирование'):
    inHelp = True
    
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name='стат', description='Вывести статистику игрока', brief='[ник игрока]')
    async def parse(self, ctx, *, nickname):
        ptggResponse = ptgg.run(nickname, dm, False)
        if ptggResponse['success']:
            await give_rank(ptggResponse['newPlayerStats'], self.bot)
            embed = discord.Embed(
                title = 'Успех',
                description = 'Время проверки: '+str(dt.now())+'\n\n'+ptggResponse['result'],
                colour = discord.Colour.blue()
            )      
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = 'Ошибка',
                description = ptggResponse['error'],
                colour = discord.Colour.red()
            )      
            await ctx.send(embed=embed)
            

    @commands.command(name='скан', description='Проверить игроков из базы сканирования на наличие изменений в статистике', brief='')
    async def parse_task_now(self, ctx):
        embed = discord.Embed(
            title = 'Сканирование..',
            description = 'Сканирование началось, оно может идти довольно долго..',
            colour = discord.Colour.gold()
        )
        await ctx.send(embed=embed, delete_after=len( list( (dm.get_saves() ).keys() ) ) *3 )
        changes = await parsing.parse_task(self.bot)
        
        if changes == False:
            embed = discord.Embed(
            title = 'Итог сканирования',
            description = 'Изменения не найдены',
            colour = discord.Colour.blue()
        )
        await ctx.send(embed=embed)
        

    @tasks.loop(minutes=10.0)
    async def parse_task(bot):
        changes = False
        print('('+str(dt.now())+') Обновление статистики...\n')
        saves = dm.get_saves()
        data = dm.get_main_data()
        guild = bot.get_guild(data['const']['guildID'])
        spamChannel = guild.get_channel(data['dinamic']['spamChannelID'])
        
        if list(saves.keys())==[]:
            print('('+str(dt.now())+') Сбой обновления статистики. База пуста')
            
        else:
            for nickname in saves.keys():
                print('===== Начало '+nickname+' =====')
                ptggResponse = ptgg.run(nickname, dm, True)
                
                if ptggResponse['success']:
                    await give_rank(ptggResponse['newPlayerStats'], bot)
                    
                    if saves[nickname]['playerStats']!=ptggResponse['newPlayerStats'] and ptggResponse['convertorResult']!=None:
                        changes = True
                        newSaves = dm.load_data('saves.json')
                        newSaves[nickname]['playerStats']=ptggResponse['newPlayerStats']
                        dm.dump_data('saves.json', newSaves)
                        
                        embed = discord.Embed(
                            title = f'У вас изменение в статистике `{nickname}`!',
                            description = '**Время проверки: '+str(dt.now())+'**\n\n'+ptggResponse['convertorResult'],
                            colour = discord.Colour.blue()
                        )      
                        await spamChannel.send(embed=embed)

                    elif ptggResponse['convertorResult']==None:
                        print('Изменений не найдено')
                    
                else:
                    print(ptggResponse['error'])
                    if ptggResponse['error'] != 'Время ожидания ответа сайта истекло' and ptggResponse['error'] != 'Ошибка playerStats':
                        print('Игрок удалён из базы')
                        playersData = dm.load_data('saves.json')
                        playersData.pop(nickname)
                        dm.dump_data('saves.json', playersData)
                        
                        embed = discord.Embed(
                            title = f'Ошибка сканирования `{nickname}`',
                            description = ptggResponse['error']+'\nИгрок удалён из базы',
                            colour = discord.Colour.red()
                        )    
                        await spamChannel.send(embed=embed)
                        
                print('===== Конец '+nickname+' =====\n')
        print('('+str(dt.now())+') Обновление завершено\n')
        return changes
            
                

def setup(bot):
    bot.add_cog(parsing(bot))
    parsing.parse_task.start(bot)
