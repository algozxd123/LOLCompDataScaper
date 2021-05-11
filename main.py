import requests, sys
from bs4 import BeautifulSoup

def indexTournaments(season):
    return requests.post('https://gol.gg/tournament/ajax.trlist.php', {'season': 'S{}'.format(season)}).text

def getMatchList(tournament):

    source = requests.get('https://gol.gg/tournament/tournament-matchlist/{}/'.format(tournament)).text
    soup = BeautifulSoup(source, 'html.parser')
    lines = soup.find('tbody').find_all('tr')
    response = []
    for line in lines:
        columns = line.find_all('td')
        scores = columns[2].text.split(' - ')
        match_code = columns[0].a.get('href').split('/')[3]
        obj = {'match_code': match_code,'game': columns[0].a.text, 'team_one': columns[1].text, 'team_one_score': scores[0], 'team_two': columns[3].text, 'team_two_score': scores[1], 'tournament_stage': columns[4].text, 'patch': columns[5].text, 'date': columns[6].text}

def getMatch(match_code):
    source = requests.get('https://gol.gg/game/stats/{}/page-game/'.format(match_code)).text
    soup = BeautifulSoup(source, 'html.parser')
    
    #Match spacific data
    winner_text = soup.find('div', {'class': 'col-12 blue-line-header'}).text.split(' - ')[1]
    winner = 'blue' if winner_text[1] == 'WIN' else 'red'
    date_text = soup.find('div', {'class': 'col-12 col-sm-5 text-right'}).text.split(' (')
    date = date_text[0]
    tournament_stage = date_text[1][:-1]
    duration_text = soup.find('div', {'class': 'col-6 text-center'}).h1.text.split(':')
    duration = int(duration_text[0])*60 + int(duration_text[1])
    patch = int(soup.find('div', {'class' : 'col-3 text-right'}).text[2:].replace('.',''))

    #Blue team data
    blue_team = soup.find('div', {'class': 'col-12 blue-line-header'}).a.text

    blue_scoreboard_html = soup.find('div', {'class' : 'col-12 col-sm-6'})
    blue_team_scores_html = blue_scoreboard_html.find_all('div', {'class': 'col-2'})
    blue_team_kills = int(blue_team_scores_html[0].span.text)
    blue_team_towers = int(blue_team_scores_html[1].span.text)
    blue_team_dragons = int(blue_team_scores_html[2].span.text)
    blue_team_barons = int(blue_team_scores_html[3].span.text)
    blue_team_gold = int(blue_team_scores_html[4].span.text.replace('k', '00').replace('.',''))

    blue_team_cloud_dragon = 0
    blue_team_infernal_dragon = 0
    blue_team_ocean_dragon = 0
    blue_team_mountain_dragon = 0
    blue_team_elder_dragon = 0
    dragon_types_imgs = blue_scoreboard_html.find_all('img', {'class': 'champion_icon_XS'})
    for dragon_types_img in dragon_types_imgs:
        if('Cloud' in dragon_types_img.get('alt')):
            blue_team_cloud_dragon += 1
        if('Infernal' in dragon_types_img.get('alt')):
            blue_team_infernal_dragon += 1
        if('Ocean' in dragon_types_img.get('alt')):
            blue_team_ocean_dragon += 1
        if('Mountain' in dragon_types_img.get('alt')):
            blue_team_mountain_dragon += 1
        if('Elder' in dragon_types_img.get('alt')):
            blue_team_elder_dragon += 1

    blue_team_first_blood = False
    blue_team_first_Tower = False
    if(blue_team_scores_html[0].find('img', {'class': 'champion_icon_Xlight'})):
        blue_team_first_blood = True
    if(blue_team_scores_html[1].find('img', {'class': 'champion_icon_Xlight'})):
        blue_team_first_tower = True

    blue_team_bans_imgs = blue_scoreboard_html.find_all('img', {'class': 'champion_icon_medium rounded-circle'})
    blue_team_bans = []
    for i in range(5):
        blue_team_bans.append(blue_team_bans_imgs[i].get('alt'))
    
    #Red team data 
    red_team = soup.find('div', {'class': 'col-12 red-line-header'}).a.text

    red_scoreboard_html = soup.find_all('div', {'class' : 'col-12 col-sm-6'})[1]
    red_team_scores_html = red_scoreboard_html.find_all('div', {'class': 'col-2'})
    red_team_kills = int(red_team_scores_html[0].span.text)
    red_team_towers = int(red_team_scores_html[1].span.text)
    red_team_dragons = int(red_team_scores_html[2].span.text)
    red_team_barons = int(red_team_scores_html[3].span.text)
    red_team_gold = int(red_team_scores_html[4].span.text.replace('k', '00').replace('.',''))

    red_team_cloud_dragon = 0
    red_team_infernal_dragon = 0
    red_team_ocean_dragon = 0
    red_team_mountain_dragon = 0
    red_team_elder_dragon = 0
    dragon_types_imgs = red_scoreboard_html.find_all('img', {'class': 'champion_icon_XS'})
    for dragon_types_img in dragon_types_imgs:
        if('Cloud' in dragon_types_img.get('alt')):
            red_team_cloud_dragon += 1
        if('Infernal' in dragon_types_img.get('alt')):
            red_team_infernal_dragon += 1
        if('Ocean' in dragon_types_img.get('alt')):
            red_team_ocean_dragon += 1
        if('Mountain' in dragon_types_img.get('alt')):
            red_team_mountain_dragon += 1
        if('Elder' in dragon_types_img.get('alt')):
            red_team_elder_dragon += 1

    red_team_first_blood = False
    red_team_first_tower = False
    if(red_team_scores_html[0].find('img', {'class': 'champion_icon_Xlight'})):
        red_team_first_blood = True
    if(red_team_scores_html[1].find('img', {'class': 'champion_icon_Xlight'})):
        red_team_first_tower = True

    red_team_bans_imgs = red_scoreboard_html.find_all('img', {'class': 'champion_icon_medium rounded-circle'})
    red_team_bans = []
    for i in range(5):
        red_team_bans.append(red_team_bans_imgs[i].get('alt'))

    #Gold graph data
    scripts = soup.find_all('script')
    #Extracting the necessary value from the variable 'golddatas' in the JS of the site
    gold_timeline_values = str(scripts[11]).split('data: [')[2].split(']')[0].split(',')[:-1]
    gold_timeline_values = [int(x) for x in gold_timeline_values]

    #Events timeline data
    blue_actions = []
    red_actions = []

    blue_actions_spans = soup.find_all('span', {'class': 'blue_action'})
    red_actions_spans = soup.find_all('span', {'class': 'red_action'})

    for span in blue_actions_spans:
        time = span.text.split(':')
        time_int = int(time[0])*60+int(time[1])
        blue_actions.append({'action': span.img.get('alt'), 'time': time_int})
    
    for span in red_actions_spans:
        time = span.text.split(':')
        time_int = int(time[0])*60+int(time[1])
        red_actions.append({'action': span.img.get('alt'), 'time': time_int})
    
    match_data = {'date': date, 'tournament_stage': tournament_stage, 'duration': duration, 'patch': patch, 'winner': winner, 'gold_timeline_values': gold_timeline_values}
    blue_team_data = {'team_name': blue_team, 'kills': blue_team_kills, 'towers': blue_team_towers, 'dragons': blue_team_dragons, 'barons': blue_team_barons, 'gold': blue_team_gold, 'cloud_dragons': blue_team_cloud_dragon, 'infernal_dragons': blue_team_infernal_dragon, 'ocean_dragons': blue_team_ocean_dragon, 'mountain_dragons': blue_team_mountain_dragon, 'elder_dragons': blue_team_elder_dragon, 'first_blood': blue_team_first_blood, 'first_tower': blue_team_first_tower, 'bans': blue_team_bans, 'actions': blue_actions}
    red_team_data = {'team_name': red_team, 'kills': red_team_kills, 'towers': red_team_towers, 'dragons': red_team_dragons, 'barons': red_team_barons, 'gold': red_team_gold, 'cloud_dragons': red_team_cloud_dragon, 'infernal_dragons': red_team_infernal_dragon, 'ocean_dragons': red_team_ocean_dragon, 'mountain_dragons': red_team_mountain_dragon, 'elder_dragons': red_team_elder_dragon, 'first_blood': red_team_first_blood, 'first_tower': red_team_first_tower, 'bans': red_team_bans, 'actions': red_actions}
    response = {'match_data': match_data, 'blue_team_data': blue_team_data, 'red_team_data': red_team_data}

    return response
    
getMatch('31260')