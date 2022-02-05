def role_analysis(playerStats, additional_analysis_result, errors): #роль игрока
    smoker=0
    defender=0
    helper=0
    attacker=0
    for data in ['TopAgent1Data','TopAgent2Data','TopAgent3Data']:
        agent = playerStats[data]['name']
        
        if agent=='Omen':
            smoker+=1
            
        elif agent=='Cypher':
            defender+=1
            helper+=1
            
        elif agent=='Brimstone':
            smoker+=1
            
        elif agent=='Sage':
            helper+=1
            defender+=1
            
        elif agent=='Breach':
            helper+=1
            attacker+=1
            
        elif agent=='Killjoy':
            defender+=1
            
        elif agent=='Raze':
            attacker+=1
            
        elif agent=='Yoru':
            attacker+=1
            
        elif agent=='KAY/O':
            attacker+=1
            helper+=1
            
        elif agent=='Reyna':
            attacker+=1
            
        elif agent=='Astra':
            smoker+=1
            helper+=1
            
        elif agent=='Skye':
            helper+=1
            
        elif agent=='Phoenix':
            attacker+=1
            
        elif agent=='Jett':
            attacker+=1
            
        elif agent=='Sova':
            helper+=1
            
        elif agent=='Viper':
            smoker+=1
            helper+=1
            defender+=1

        else:
            errors['count']+=1
            errors['text']+=f'Агента {agent} нету в базе\n'

    additional_analysis_result += f'Роль: Смоки: {smoker}; Атака: {attacker}; Оборона: {defender}; Поддержка: {helper}'
    role_analysis_result = f'Смоки: {smoker}; Атака: {attacker}; Оборона: {defender}; Поддержка: {helper}'
    return additional_analysis_result, errors, role_analysis_result


def skill_analysis(playerStats, additional_analysis_result, errors): #скилл игрока
    try:
        rank = (playerStats['rank'].split())[0]
        
        if rank=='Unrated' or rank=='Iron' or rank=='Bronze' or rank=='Silver':
            rank = float(1)
        elif rank=='Gold':
            rank = float(1.05)
        elif rank=='Platinum':
            rank = float(1.1)
        elif rank=='Diamond':
            rank = float(1.15)
        elif rank=='Immortal' or rank.startswith('RR'):
            rank = float(1.2)
        elif rank=='Radiant':
            rank = float(1.25)
        else:
            rank = float(1)
                 
        additional_analysis_result += f"\nУровень скилла: {round(float(playerStats['kd'])*float(playerStats['middleKillsForRound'])*float(playerStats['middleScoreForRound']), 2)}"
        skill_analysis_result = str(round(float(playerStats['kd'])*float(playerStats['middleKillsForRound'])*float(playerStats['middleScoreForRound'])*rank, 2))
    except BaseException as error:
        skill_analysis_result = '(ошибка)'
        errors['count']+=1
        errors['text']+=f'Не удалось установить уровень скилла: "{error}"\n'
    return additional_analysis_result, errors, skill_analysis_result


def additional_analysis(playerStats):
    additional_analysis_result = ''
    errors = dict(count=0, text='')
    
    additional_analysis_result, errors, role_analysis_result = role_analysis(playerStats, additional_analysis_result, errors) #роль игрока
    additional_analysis_result, errors, skill_analysis_result = skill_analysis(playerStats, additional_analysis_result, errors) #скилл игрока
    
    print('Всего ошибок во время анализа: '+str(errors['count'])+'\n'+str(errors['text']))
    return additional_analysis_result, role_analysis_result, skill_analysis_result
