import discord
from discord.ext import commands, tasks
import DataMaster as dm

class omens(commands.Cog):
    inHelp = False #Вывести ли команды в меню помощи?
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_voice_state_update')
    async def on_voice_state_update(self, newMember, before, after):
        if (before.channel != after.channel) and (after.channel != None):
            if after.channel != None:
                floodRoleID = dm.get_main_data()['dinamic']['flood']
                backgroundRoleID = dm.get_main_data()['dinamic']['background']
                
                newHaveOmen = False
                newDescription = ''
                
                for role in newMember.roles:
                    if role.id == floodRoleID:
                        newDescription += f'**Пользователь {str(newMember.mention)} был помечен как флудер**\nДанный тип игроков вредит дисциплине команды, но в несерьёзной игре некоторые из них способны поднять настроение\n\n'
                        newHaveOmen = True
                    elif role.id == backgroundRoleID:
                        newDescription += f'**У пользователя {str(newMember.mention)} был отмечен шум на заднем фоне**\nДанный тип игроков вредит концентрации команды, но в несерьёзной игре это можно игнорировать\n\n'
                        newHaveOmen = True

                for member in after.channel.members:
                    if newMember!=member:
                        
                        if newHaveOmen:
                            embed = discord.Embed(
                                title = 'Осторожно опасный игрок!',
                                description = newDescription,
                                colour = discord.Colour.gold()
                            )
                            await member.send(embed=embed)
                        
                        haveOmen = False
                        description = ''
                        
                        for role in member.roles:
                            if role.id == floodRoleID:
                                description += f'**Пользователь {member.mention} был помечен как флудер**\nДанный тип игроков вредит дисциплине команды, но в несерьёзной игре некоторые из них способны поднять настроение\n\n'
                                haveOmen = True
                            elif role.id == backgroundRoleID:
                                description += f'**У пользователя {str(member.mention)} был отмечен шум на заднем фоне**\nДанный тип игроков вредит концентрации команды, но в несерьёзной игре это можно игнорировать\n\n'
                                haveOmen = True

                        if haveOmen:
                            embed = discord.Embed(
                                title = 'Осторожно опасный игрок!',
                                description = description,
                                colour = discord.Colour.gold()
                            )
                            await newMember.send(embed=embed)
        

def setup(bot):
    bot.add_cog(omens(bot))

