import discord
from discord.ext import commands, tasks

import DataMaster as dm
from player_parser import Parser_tracker_gg as ptgg

class data_commands(commands.Cog, name='База сканирования'):
    inHelp = True
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='рейтинг', description=f'Выводит рейтинг игроков', brief='')
    async def rating(self, ctx):
        playersData = dm.get_saves()
        ratings = []
        ratings_players = {}
        for nickname in playersData:
            ratings.append(float(playersData[nickname]['playerStats']['skill_analysis_result']))
            ratings_players[float(playersData[nickname]['playerStats']['skill_analysis_result'])] = nickname
        ratings.sort()
        ratings.reverse()
        text = ''
        place = 1
        for r in ratings:
            text+=str(place)+') '+ratings_players[r]+' ('+str(r)+')'+'\n'
            place+=1
        embed = discord.Embed(
            title = 'Рейтинг игроков',
            description = text,
            colour = discord.Colour.blue()
        )
        await ctx.send(embed=embed)
    

    @commands.group(name='бс', description=f'Манипуляция данными в базе сканирования', invoke_without_command=True, brief='[дейсвие]')
    async def scan_data(self, ctx):
        embed = discord.Embed(
            title = 'Команда введена не полностью',
            description = 'Чтобы узнать синтаксис команды, обратитесь к команде `помощь`',
            colour = discord.Colour.gold()
        )
        await ctx.send(embed=embed)


    @scan_data.command(name='дп', description=f'Добавить игрока в базу сканирования с привязкой к дискорду', brief='[@пользователь] [ник игрока]')
    async def add_connect(self, ctx, mention, *, nickname):
        discordID = mention.replace('<@!', '')
        discordID = discordID.replace('>','')
        
        playersData = dm.get_saves()

        success, error, result, newPlayerStats, convertorResult = ptgg.run(nickname, dm, False)
        if success:
            if playersData.get(nickname)==None:
                playersData[nickname] = {'discord':None, 'playerStats':None}
                dm.dump_saves(playersData)
                
                embed = discord.Embed(
                    title = 'Успех',
                    description = f'Игрок `{nickname}` добавлен в базу',
                    colour = discord.Colour.green()
                )
                await ctx.send(embed=embed)
                    
            else:
                embed = discord.Embed(
                    title = 'Ошибка',
                    description = f'Игрок `{nickname}` уже был добавлен в базу',
                    colour = discord.Colour.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = 'Ошибка',
                description = error,
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)

        if discordID.isdigit()==False:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Введёный ID: `{discordID}` содержит символы помимо цифр\nВы точно правильно ввели ID пользователя?',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return


        discordID = int(discordID)
        playersData = dm.get_saves()
        
        if playersData.get(nickname)!=None:
            if playersData[nickname]['discord']!=None:
                data = dm.get_main_data()
                guild = self.bot.get_guild(data['const']['guildID'])
                userBefore = guild.get_member(playersData[nickname]['discord'])
                embed = discord.Embed(
                    title = 'Ошибка',
                    description = f'Игрок `{nickname}` уже обладает привязкой к дискорду\nВладелец: `{userBefore}`',
                    colour = discord.Colour.red()
                )
                await ctx.send(embed=embed)
                return
            
            data = dm.get_main_data()
            guild = self.bot.get_guild(data['const']['guildID'])
            user = guild.get_member(discordID)

            if user==None:
                embed = discord.Embed(
                    title = 'Ошибка',
                    description = f'Пользователя с ID: `{discordID}` не сушествует\nВы точно правильно ввели ID пользователя?',
                    colour = discord.Colour.red()
                )
                await ctx.send(embed=embed)
                return

            playersData[nickname]['discord'] = discordID
            dm.dump_saves(playersData)

            embed = discord.Embed(
                title = 'Успех',
                description = f'Пользователь `{user}` успешно привязан к игроку `{nickname}`',
                colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)

    

    @scan_data.command(name='доб', description=f'Добавить игрока в базу сканирования', brief='[ник игрока]')
    async def add(self, ctx, *, nickname):
        playersData = dm.get_saves()

        success, error, result, newPlayerStats, convertorResult = ptgg.run(nickname, dm, False)
        if success:
            if playersData.get(nickname)==None:
                playersData[nickname] = {'discord':None, 'playerStats':None}
                dm.dump_saves(playersData)
                
                embed = discord.Embed(
                    title = 'Успех',
                    description = f'Игрок {nickname} добавлен в базу',
                    colour = discord.Colour.green()
                )
                await ctx.send(embed=embed)
                    
            else:
                embed = discord.Embed(
                    title = 'Ошибка',
                    description = f'Игрок {nickname} уже был добавлен в базу',
                    colour = discord.Colour.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = 'Ошибка',
                description = error,
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)


    @scan_data.command(name='уд', description=f'Удалить игрока из базы сканирования', brief='[ник игрока]')
    async def remove(self, ctx, *, nickname):
        playersData = dm.get_saves()
        
        if playersData.get(nickname)==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Игрока `{nickname}` нету в базе',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            
        else:
            playersData.pop(nickname)
            dm.dump_saves(playersData)

            embed = discord.Embed(
                title = 'Успех',
                description = f'Игрок `{nickname}` удалён из базы',
                colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)


    @scan_data.command(name='прив', description=f'Привязать игрока из базу сканирования к аккаунту дискорд', brief='[@пользователь] [ник игрока]')
    async def connect(self, ctx, mention, *, nickname):
        discordID = mention.replace('<@', '')
        discordID = discordID.replace('>','')
        
        if discordID.isdigit()==False:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Введёный ID: `{discordID}` содержит символы помимо цифр\nВы точно правильно ввели ID пользователя?',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        discordID = int(discordID)
        playersData = dm.get_saves()
        
        if playersData.get(nickname)==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Игрока `{nickname}` нету в базе',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return
        
        elif playersData[nickname]['discord']!=None:
            data = dm.get_main_data()
            guild = self.bot.get_guild(data['const']['guildID'])
            userBefore = guild.get_member(playersData[nickname]['discord'])
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Игрок `{nickname}` уже обладает привязкой к дискорду\nВладелец: `{userBefore}`',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return
        
        data = dm.get_main_data()
        guild = self.bot.get_guild(data['const']['guildID'])
        user = guild.get_member(discordID)

        if user==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Пользователя с ID: `{discordID}` не сушествует\nВы точно правильно ввели ID пользователя?',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        playersData[nickname]['discord'] = discordID
        dm.dump_saves(playersData)

        embed = discord.Embed(
            title = 'Успех',
            description = f'Пользователь `{user}` успешно привязан к игроку `{nickname}`',
            colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)


    @scan_data.command(name='отв', description=f'Отвязать дискорд аккаунт, привязанный к игроку в базе сканирования', brief='[ник игрока]')
    async def disconnect(self, ctx, *, nickname):
        playersData = dm.get_saves()
        
        if playersData.get(nickname)==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Игрока `{nickname}` нету в базе',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        elif playersData[nickname]['discord']==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'У игрока `{nickname}` ещё нет привязки к дискорду',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        playersData[nickname]['discord'] = None
        dm.dump_saves(playersData)

        embed = discord.Embed(
            title = 'Успех',
            description = f'Игроку `{nickname}` отключена привязку к дискорду',
            colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)


    @scan_data.command(name='обн', description=f'Изменить дискорд аккаунт, привязанный к игроку в базе сканирования', brief='[@пользователь] [ник игрока]')
    async def reconnect(self, ctx, mention, *, nickname):
        discordID = mention.replace('<@!', '')
        discordID = discordID.replace('>','')
        
        if discordID.isdigit()==False:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Введёный ID: `{discordID}` содержит символы помимо цифр\nВы точно правильно ввели ID пользователя?',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        discordID = int(discordID)
        playersData = dm.get_saves()
        
        if playersData.get(nickname)==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Игрока `{nickname}` нету в базе',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        elif playersData[nickname]['discord']==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'У игрока `{nickname}` ещё нет привязки к дискорду',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        data = dm.get_main_data()
        guild = self.bot.get_guild(data['const']['guildID'])
        user = guild.get_member(discordID)
        userBefore = guild.get_member(playersData[nickname]['discord'])

        if user==None:
            embed = discord.Embed(
                title = 'Ошибка',
                description = f'Пользователя с ID: `{discordID}` не сушествует\nВы точно правильно ввели ID пользователя?',
                colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return
        
        playersData[nickname]['discord'] = discordID
        dm.dump_saves(playersData)
        embed = discord.Embed(
            title = 'Успех',
            description = f'Для игрока `{nickname}` успешно изменена привязка\nВладелец `{userBefore}` => изменился на => `{user}`',
            colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)

        
    @scan_data.command(name='спис', description=f'Вывести список игроков из базы сканирования', brief='')
    async def saves_list(self, ctx):
        playersData = dm.get_saves()

        if len(playersData.keys())==0:
            embed = discord.Embed(
                title = 'Список игроков в базе сканирования',
                description = 'База пуста',
                colour = discord.Colour.blue()
            )
            await ctx.send(embed=embed)
            return
        
        text = ''
        place = 1
        places = ''
        nicknames = ''
        connects = ''
        
        for nickname in list(playersData.keys()):
            places=places+str(place)+'\n'
            nicknames=nicknames+nickname+'\n'
            
            if playersData[nickname]['discord']!=None:
                data = dm.get_main_data()
                guild = self.bot.get_guild(data['const']['guildID'])
                user = guild.get_member(playersData[nickname]['discord'])
                
                connects=connects+f'привязан к {user}\n'
            else:
                connects=connects+f'нет привязки\n'
            place+=1

        embed = discord.Embed(
            title = 'Список игроков в базе сканирования',
            description = text,
            colour = discord.Colour.blue()
        )
        
        embed.add_field(name='№', value=places, inline=True)
        embed.add_field(name='Ник', value=nicknames, inline=True)
        embed.add_field(name='Привязка', value=connects, inline=True)

        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(data_commands(bot))
