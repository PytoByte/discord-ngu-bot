import requests
from bs4 import BeautifulSoup as bs

import re

from . import additional_analysis
from . import convertor

def getSoup(nick, tag):
    url = 'https://tracker.gg/valorant/profile/riot/'+nick.replace(' ', '%20')+'%23'+tag+'/overview?playlist=competitive&season=all'
    try:
        r = requests.get(url, timeout=10)
    except:
        return False, 'Время ожидания ответа сайта истекло', None, None
    soup = bs(r.content, 'html.parser')
    return True, None, soup, url


def doesPlayerExist(soup, nickname):
    text = soup.find(class_='lead')
    text = text.text
    item = soup.find_all(class_='notice')
    try:
        item = item[0].text
    except:
        item='информация есть'

    if item== 'No stats to show.':
        return False, f'У игрока `{nickname}` отсутствуют данные'
    
    elif text== 'This profile is private.':
        return False, f'У игрока `{nickname}` закрытый профиль'
    
    elif text == f'We could not find the player {nickname}.':
        return False, f'Игрока `{nickname}` не существует'

    elif text == f'{nickname} has not played Valorant.':
        return False, f'Игрок `{nickname}` никогда не играл в Valorant'
    
    else:
        return True, None


def Parser(soup, url, nickname):
    
    item = (soup.find(class_='playtime')).text
    playTime=item.replace(' Play Time', '')
    playTime=playTime.replace('\n', '')

    item = (soup.find(class_='matches')).text
    text = ((re.search('.*M', item)).group(0)).split()
    matches = text[0]
    
    items = soup.find_all(class_='value')
    
    for place in range(len(items)):
        item = (items[place].text).split()
            
        if place==2 or place==3 or place==4:
            continue
        
        if len(item)==1:
            text = item[0]
        else:
            text = item[0]+' '+item[1]
            
        if place==0:
            rank=text
        elif place==1:
            bestRank=text
        elif place==5:
            middleDamageForRound=text
        elif place==6:
            kd=text
        elif place==7:
            percentHeadshots=text
        elif place==8:
            winRate=text
        elif place==9:
            wins=text
        elif place==10:
            kills=text
        elif place==11:
            headshots=text
        elif place==12:
            deaths=text
        elif place==13:
            assists=text
        elif place==14:
            middleScoreForRound=text
        elif place==15:
            middleKillsForRound=text
        elif place==16:
            clutches=text
        elif place==17:
            flawless=text
        elif place==18:
            maxKillsForMatch=text
            
    items=''
    item=''
    text=''

    topAgents = soup.find(class_='top-agents__table-container')
    
    topAgentsName = topAgents.find_all(class_='agent__name')

    for place in range(len(topAgentsName)):
        text = topAgentsName[place].text

        if place==0:
            topAgentsName1=text
        elif place==1:
            topAgentsName2=text
        elif place==2:
            topAgentsName3=text
    items=''
    item=''
    text=''

    topAgentsStats = topAgents.find_all(class_='name')

    for place in range(len(topAgentsStats)):
        text = topAgentsStats[place].text

        if place==0:
            topAgentTime1=text
        elif place==1:
            topAgentMatches1=text
        elif place==2:
            topAgentWinRate1=text
        elif place==3:
            topAgentKD1=text
        elif place==4:
            topAgentADR1=text
            
        elif place==5:
            topAgentTime2=text
        elif place==6:
            topAgentMatches2=text
        elif place==7:
            topAgentWinRate2=text
        elif place==8:
            topAgentKD2=text
        elif place==9:
            topAgentADR2=text
            
        elif place==10:
            topAgentTime3=text
        elif place==11:
            topAgentMatches3=text
        elif place==12:
            topAgentWinRate3=text
        elif place==13:
            topAgentKD3=text
        elif place==14:
            topAgentADR3=text
    items=''
    item=''
    text=''

    TopAgent1 = topAgentsName1+'\n-Время: '+topAgentTime1+'\n-Матчи: '+topAgentMatches1+'\n-Процент побед: '+topAgentWinRate1+'\n-Соотношение убийств/смертей: '+topAgentKD1+'\n-Средний урон за раунд: '+topAgentADR1
    TopAgent2 = topAgentsName2+'\n-Время: '+topAgentTime2+'\n-Матчи: '+topAgentMatches2+'\n-Процент побед: '+topAgentWinRate2+'\n-Соотношение убийств/смертей: '+topAgentKD2+'\n-Средний урон за раунд: '+topAgentADR2
    TopAgent3 = topAgentsName3+'\n-Время: '+topAgentTime3+'\n-Матчи: '+topAgentMatches3+'\n-Процент побед: '+topAgentWinRate3+'\n-Соотношение убийств/смертей: '+topAgentKD3+'\n-Средний урон за раунд: '+topAgentADR3

    TopAgent1Data = dict(name=topAgentsName1, time=topAgentTime1, matches=topAgentMatches1, WinRate=topAgentWinRate1, KD=topAgentKD1, ADR=topAgentADR1)
    TopAgent2Data = dict(name=topAgentsName2, time=topAgentTime2, matches=topAgentMatches2, WinRate=topAgentWinRate2, KD=topAgentKD2, ADR=topAgentADR2)
    TopAgent3Data = dict(name=topAgentsName3, time=topAgentTime3, matches=topAgentMatches3, WinRate=topAgentWinRate3, KD=topAgentKD3, ADR=topAgentADR3)

    try:
        playerStats = {'url':url, 'nickname':nickname, 'rank':rank, 'playTime':playTime, 'matches':matches, 'kd':kd, 'middleDamageForRound':middleDamageForRound, 'winRate':winRate, 'middleScoreForRound':middleScoreForRound, 'middleKillsForRound':middleKillsForRound, 'TopAgent1Data':TopAgent1Data, 'TopAgent2Data':TopAgent2Data, 'TopAgent3Data':TopAgent3Data, 'bestRank':bestRank, 'wins':wins, 'clutches':clutches, 'flawless':flawless, 'kills':kills, 'deaths':deaths, 'assists':assists, 'headshots':headshots, 'percentHeadshots':percentHeadshots, 'maxKillsForMatch':maxKillsForMatch}   
    except BaseException as er:
        error = 'Ошибка playerStats'
        return None, None
    _additional_analysis, role_analysis_result, skill_analysis_result = additional_analysis.additional_analysis(playerStats)
    additional_analysis_data = {'additional_analysis':_additional_analysis, 'role_analysis_result':role_analysis_result, 'skill_analysis_result':skill_analysis_result}
    playerStats.update(additional_analysis_data)
    
    output = [
        'Ссылка: '+url,
        '\nОСНОВНАЯ ИНФОРМАЦИЯ',
        'Ник: '+nickname,
        'Ранг: '+rank,
        'Игровое время: '+playTime,
        'Сыграно '+matches+' матчей',
        'Соотношение убийств/смертей: '+kd,
        'Средний урон за раунд: '+middleDamageForRound,
        'Процент побед: '+winRate,
        'Средний счёт за раунд: '+middleScoreForRound,
        'В среднем убийств за раунд: '+middleKillsForRound,
        '\nДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ',
        _additional_analysis,
        '\nПРЕДПОЧИТАЕМЫЕ АГЕНТЫ',
        '1) '+TopAgent1,
        '2) '+TopAgent2,
        '3) '+TopAgent3,
        '\nДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ',
        'Лучший ранг: '+bestRank,
        'Количество побед: '+wins,
        'Количетсво клатчей: '+clutches,
        'Количетсво командных эйсов: '+flawless,
        'Количество убийств: '+kills,
        'Количество смертей: '+deaths,
        'Количество помощи в убийствах: '+assists,
        'Количество попаданий в голову: '+headshots,
        'Процент попадания в голову за все игры: '+percentHeadshots,
        'Рекорд убийств за матч: '+maxKillsForMatch,
    ]

    result=''
    for x in output:
        result+=x+'\n'
    result = result[0:-1]

    return result, playerStats

def run(nickname, dm, with_bs):
    try:
        nick = ((re.search(r'.*#', nickname)).group(0))[0:-1]
        tag = ((re.search(r'#.*', nickname)).group(0))[1:]
    except:
        error = f'Игрока `{nickname}` не существует'
        return {'success':False, 'error':error, 'result':None, 'newPlayerStats':None, 'convertorResult':None}
    
    success, error, soup, url = getSoup(nick, tag)
    
    if success:
        success, error = doesPlayerExist(soup, nickname)

        if success:
            result, playerStats = Parser(soup, url, nickname)
            
            if result==None:
                error = 'Ошибка playerStats'
                return {'success':False, 'error':error, 'result':None, 'newPlayerStats':None, 'convertorResult':None}
            else:
                if with_bs:
                    playerStatsBefore = (dm.get_saves())[nickname]['playerStats']
                    
                    if playerStatsBefore==None:
                        playerStatsBefore=playerStats
                        newSaves = dm.load_data('saves.json')
                        newSaves[nickname]['playerStats']=playerStats
                        dm.dump_data('saves.json', newSaves)
                        
                    if playerStatsBefore!=playerStats and success:
                        convertorResult = convertor.convertor(playerStats, playerStatsBefore)
                        
                    else:
                        convertorResult = None
                else:
                    convertorResult = None
                        
                return {'success':True, 'error':None, 'result':result, 'newPlayerStats':playerStats, 'convertorResult':convertorResult}
        
        else:
            return {'success':False, 'error':error, 'result':None, 'newPlayerStats':None, 'convertorResult':None}
        
    else:
        return {'success':False, 'error':error, 'result':None, 'newPlayerStats':None, 'convertorResult':None}
