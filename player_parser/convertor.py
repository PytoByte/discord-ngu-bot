def convertor(playerStats, playerStatsBefore):
    text=''
    result = ''
    GroupsAndStats = {'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ':'', 'ОСНОВНАЯ ИНФОРМАЦИЯ':'', 'ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ':'', 'ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ':'', 'НЕИЗВЕСТНЫЕ ПАРАМЕТРЫ':''}
    for psbKey in playerStatsBefore:
        statName = ''
        if playerStatsBefore[psbKey]!=playerStats[psbKey]:

            StatGroup = None

            if psbKey == 'url':
                statName= 'Ссылка'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'nickname':
                statName= 'Ник'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'rank':
                statName= 'Ранг'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'playTime':
                statName= 'Игровое время'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'matches':
                statName= 'Количество с игранный матчей'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'kd':
                statName= 'К/Д'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'middleDamageForRound':
                statName= 'Средний урон за раунд'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'winRate':
                statName= 'Процент побед'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'middleScoreForRound':
                statName= 'Средний счёт за раунд'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'middleKillsForRound':
                statName= 'Среднее количество убийств за раунд'
                StatGroup = 'ОСНОВНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'bestRank':
                statName= 'Лучший ранг'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'wins':
                statName= 'Количество побед'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'clutches':
                statName= 'Количество клатчей'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'flawless':
                statName= 'Количетсво командных эйсов'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'kills':
                statName= 'Количество убийств'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'deaths':
                statName= 'Количество смертей'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'assists':
                statName= 'Количество помощи в убийствах'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'deaths':
                statName= 'Количество смертей'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'headshots':
                statName= 'Количество попаданий в голову'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'percentHeadshots':
                statName= 'Процент попаданий в голову'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'deaths':
                statName= 'Количество смертей'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'maxKillsForMatch':
                statName= 'Рекорд убийств за матч'
                StatGroup = 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ'

            elif psbKey == 'role_analysis_result':
                statName= 'Роль игрока'
                StatGroup = 'ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ'

            elif psbKey == 'skill_analysis_result':
                statName= 'Уровень скилла'
                StatGroup = 'ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ'
            
            elif psbKey == 'TopAgent1Data' or psbKey == 'TopAgent2Data' or psbKey == 'TopAgent3Data' or psbKey == 'additional_analysis':
                continue

            else:
                StatGroup = 'НЕИЗВЕСТНЫЕ ПАРАМЕТРЫ'
                print(f'Замечены изменения НЕИЗВЕСТНОЙ статистики {psbKey}')
                GroupsAndStats[StatGroup]+=f'**Изменение параметра неизвестного параметра**\n{playerStatsBefore[psbKey]} => изменился на => {playerStats[psbKey]}\n\n'

            if StatGroup == 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ':
                print(f'Замечены изменения ДОПОЛНИТЕЛЬНОЙ статистики {psbKey}')
                GroupsAndStats[StatGroup]+=f'**Изменение параметра "{statName}"**\n{playerStatsBefore[psbKey]} => изменился на => {playerStats[psbKey]}\n\n'
                
            elif StatGroup == 'ОСНОВНАЯ ИНФОРМАЦИЯ':
                print(f'Замечены изменения ОСНОВНОЙ статистики {psbKey}')
                GroupsAndStats[StatGroup]+=f'**Изменение параметра "{statName}"**\n{playerStatsBefore[psbKey]} => изменился на => {playerStats[psbKey]}\n\n'

            elif StatGroup == 'ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ':
                print(f'Замечены изменения ДОПОЛНИТЕЛЬНОГО АНАЛИЗА статистики {psbKey}')
                GroupsAndStats[StatGroup]+=f'**Изменение параметра "{statName}"**\n{playerStatsBefore[psbKey]} => изменился на => {playerStats[psbKey]}\n\n'


    for topAgent in ['TopAgent1Data', 'TopAgent2Data', 'TopAgent3Data']:
        if playerStatsBefore[topAgent] != playerStats[topAgent]:
            print('Замечены изменения статистики агентов')
            
            if topAgent == 'TopAgent1Data':
                GroupsAndStats['ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ']+=f'**Изменения топ 1 агента ({playerStats[topAgent]["name"]}):**\n'
                
            elif topAgent == 'TopAgent2Data':
                GroupsAndStats['ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ']+=f'**Изменения топ 2 агента ({playerStats[topAgent]["name"]}):**\n'
                
            elif topAgent == 'TopAgent3Data':
                GroupsAndStats['ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ']+=f'**Изменения топ 3 агента ({playerStats[topAgent]["name"]}):**\n'
                
            for psbAgentKey in playerStatsBefore[topAgent]:
                statAgentName=''
                if playerStatsBefore[topAgent][psbAgentKey] != playerStats[topAgent][psbAgentKey]:
                    
                    if psbAgentKey=='name':
                        statAgentName = 'Имя агента'

                    elif psbAgentKey=='time':
                        statAgentName = 'Время игры на агенте'

                    elif psbAgentKey=='matches':
                        statAgentName = 'Количество матчей, сыгранных на агенте'

                    elif psbAgentKey=='WinRate':
                        statAgentName = 'Процент побед за агента'

                    elif psbAgentKey=='KD':
                        statAgentName = 'К/Д за агента'

                    elif psbAgentKey=='ADR':
                        statAgentName = 'Средний урон за агента за раунд'
                        
                    GroupsAndStats['ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ']+=f'**- Изменение параметра агента "{statAgentName}"**\n-- {playerStatsBefore[topAgent][psbAgentKey]} => изменился на => {playerStats[topAgent][psbAgentKey]}\n\n'
                            
    if GroupsAndStats['ОСНОВНАЯ ИНФОРМАЦИЯ']!='':
        result+='**ОСНОВНАЯ ИНФОРМАЦИЯ**\n'+GroupsAndStats['ОСНОВНАЯ ИНФОРМАЦИЯ']
        
    if GroupsAndStats['ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ']!='':
        result+='**ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ**\n'+GroupsAndStats['ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ']

    if GroupsAndStats['ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ']!='':
        result+='**ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ**\n'+GroupsAndStats['ПРЕДПОЧИТАЕМЫЕ АГЕНТЫ']

    if GroupsAndStats['ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ']!='':
        result+='**ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ**\n'+GroupsAndStats['ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ']
    
    return result
