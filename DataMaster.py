import discord
import psycopg2

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


def get_file_saves():
    files = [discord.File(open('data/saves.json', 'rb'))]
    return saves
    

def get_main_data():
    const = load_data('const/const_data.json')
    dinamic = load_data('dinamic/dinamic_data.json')
    mainData = {'const':const, 'dinamic':dinamic}
    return mainData


async def dump_saves_from_discord_json(fileJSON):
    await fileJSON.save('data/temp.json')
    newJSON = load_data('temp.json')
    dump_data(url, newJSON)
    os.remove('data/temp.json')
            
            
def get_saves():
    conn = psycopg2.connect(database="deqlvv8fjb39m4", user="hbddisfeydelxy", password="6e4b3191594d5cf20249962a4cabf3127f5f52a4d6916069c530d2549022804c", host="ec2-54-195-76-73.eu-west-1.compute.amazonaws.com", port=5432)
    cur = conn.cursor()
    cur.execute("SELECT saves FROM saves")
    return cur.fetchall()[0][0]

def dump_saves(newJSON):
    conn = psycopg2.connect(database="deqlvv8fjb39m4", user="hbddisfeydelxy", password="6e4b3191594d5cf20249962a4cabf3127f5f52a4d6916069c530d2549022804c", host="ec2-54-195-76-73.eu-west-1.compute.amazonaws.com", port=5432)
    cur = conn.cursor()

    cur.execute("UPDATE saves SET saves = ('"+str(json.dumps(newJSON))+"')")
    conn.commit()

    
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
