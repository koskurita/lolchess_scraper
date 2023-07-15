from bs4 import BeautifulSoup
import requests
import csv

r = requests.get('https://lolchess.gg/profile/na/quoll/s9/matches/ranked')
source = r.content
soup = BeautifulSoup(r.content, 'lxml')

all_data = []



games = soup.find_all('div', {"class": "profile__match-history-v2__item"})
for game in games:
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
    
    
    
    
        
        
    # print(_placement, _augments)
    