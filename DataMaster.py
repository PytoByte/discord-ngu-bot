import json

import os
import re

def dump_data(url, newJSON):
    with open('data/'+url, 'w', encoding="utf-8") as write_file:
        json.dump(newJSON, write_file, indent=4)

def load_data(url):
    with open('data/'+url, 'r', encoding="utf-8") as read_file:
        data = json.load(read_file)
        return data

def get_files(dirURL):
    allFiles = os.listdir('data/'+dirURL)
    return allFiles


def get_cogs():
    allFiles = os.listdir('cogs')

    cogsList = []
    for f in allFiles:
        if f.endswith('.py'):
            cogsList.append(f[0:len(f)-3])
        else:
            continue
        
    return cogsList


def get_main_data():
    const = load_data('const/const_data.json')
    dinamic = load_data('dinamic/dinamic_data.json')
    mainData = {'const':const, 'dinamic':dinamic}
    return mainData
            
            
def get_saves():
    return load_data('saves.json')

#d = {'player':{'discord':'id', 'playerStats':{'data1':1, 'data2':2}}}
#dump_data('saves.json', d)
    

'''
print('Отвечаю на загрузку данных...')
    
print('Загрузка данных из data/const_data.json')
with open('data/const_data.json', 'r', encoding="utf-8") as read_file:
    const_data = json.load(read_file)


print('Загрузка данных из data/dinamic_data.json')
with open('data/dinamic_data.json', 'r', encoding="utf-8") as read_file:
    dinamic_data = json.load(read_file)

    
prefix = dinamic_data['prefix']    
spamChannelID = int(dinamic_data['channelID'])
joinRoleID = int(dinamic_data['joinRoleID'])
TOKEN = tuple_data['token'] 
guildID = int(tuple_data['guildID'])

global guild
guild = bot.get_guild(guildID)
if guild==None:
    print('Гильдия не найдена')
    print(f'{guildID} -> {guild}')
    input('Enter, чтобы закрыть программу')
    exit()
else:
    print(f'Гильдия: "{guildID}"')

global spamChannel
spamChannel = guild.get_channel(spamChannelID)
if spamChannel==None:
    print('Канал не найден')
    print(f'{spamChannelID} -> {spamChannel}')
    input('Enter, чтобы закрыть программу')
    exit()
else:
    print(f'Канал в гильдии: "{spamChannelID}"')

global joinRole
joinRole = (bot.get_guild(guildID)).get_role(joinRoleID)
if joinRole == None:
    print('Роль не найдена')
    print(f'{joinRoleID} -> {joinRole}')
    input('Enter, чтобы закрыть программу')
    exit()
else:
    print(f'Вступительная роль гильдии: "{joinRoleID}"')
'''
