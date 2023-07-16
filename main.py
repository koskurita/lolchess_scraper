from bs4 import BeautifulSoup
import requests
import csv
import ast




def scrape(summoner_name, req):
    all_data = []
    part2 = '/2'
    for i in range(2):
        if i == 0:
            r = requests.get(req)
        elif i == 1:
            r = requests.get(req+part2)
        source = r.content
        soup = BeautifulSoup(r.content, 'lxml')
        games = soup.find_all('div', {"class": "profile__match-history-v2__item"})
        for game in games:
            match_data = []
            
            # class has last char as the placement
            _placement = game.get('class')[1][-1]
            
            _augments = []
            augs = game.find_all('div', {"class": "augment"})
            for aug in augs:
                _augments.append(aug.find('img').attrs['alt'])
            
            _champions = []
            units = game.find_all('div', {"class": "unit"})
            for unit in units:
                x = unit.find('img', {"class": "stars"})
                # special case for apex turret
                if x:
                    # stars is the [-5] char in src
                    _star = x.get('src')[-5]
                else:
                    _star = 0
                y = unit.find ('div', {"class": "tft-champion"})
                _champion = (y.find('img').attrs['alt'])
                _champions.append((_champion, _star))
                
            _traits = []
            traits = game.find_all('div', {"class": "tft-hexagon-image"})
            for trait in traits:
                # lolchess format ex. trait = "1 Darkin"
                t_cnt = trait.find('img').attrs['alt'][0]
                t = trait.find('img').attrs['alt'][2:]
                _traits.append((t, t_cnt))
            
            match_data = [_placement, _augments, _traits, _champions]
            all_data.append(match_data)
    filename = summoner_name+'.csv'
    with open (filename, 'w') as new_file:
        fieldnames = ['placement', 'augments', 'traits', 'champions']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for pl, au, tr, ch in all_data:
            csv_writer.writerow({'placement': pl, 'augments': au, 'traits': tr, 'champions': ch})
    
            
        
        
# req1 = 'https://lolchess.gg/profile/na/'
# summonername = ""
# req2 = '/s9/matches/ranked'

# top_players = requests.get('https://lolchess.gg/leaderboards?mode=ranked&region=na')
# soup = BeautifulSoup(top_players.content, 'lxml')
# games = soup.find_all('td', {"class": "summoner"})
# for game in games:
#     player = game.find('a')
#     summonername = player.get_text()
#     scrape(summonername, req1 + summonername+req2)



    
    
    
    
    
    
    
    
# with open ('matches.csv', 'w') as new_file:
#     fieldnames = ['placement', 'augments', 'traits', 'champions']
#     csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
#     csv_writer.writeheader()
#     for pl, au, tr, ch in all_data:
#         csv_writer.writerow({'placement': pl, 'augments': au, 'traits': tr, 'champions': ch})
        

dic = {}
with open ('combined.csv', 'r') as read_file:
    csv_reader = csv.DictReader(read_file)
    for line in csv_reader:
        placement = int(line['placement'])
        augments = ast.literal_eval(line['augments'])
        for aug in augments:
            if aug in dic:
                dic[aug].append(placement)
            else:
                dic[aug] = [placement]
    

store = []

for key, val in dic.items():
    res = 0
    for v in val:
        res += v
    res = round(res/len(val), 2)
    store.append((key, res, len(val) ))

store = sorted(store, key=lambda x: x[1])

with open ('result.csv', 'w') as new_file:
    fieldnames = ['augment', 'placement', 'games_played']
    csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for au, pl, gm in store:
        print(au, pl, gm)
        csv_writer.writerow({'augment': au, 'placement': pl, 'games_played': gm})

xd = ["augment", "avg placement", "games played"]
print('{:<40} {:^30} {:>40}'.format(*xd))

for line in store:
    print('{:<40} {:^30} {:>40}'.format(*line))
    
    # f"{'Trades:':<15}{cnt:>10}",