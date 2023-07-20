from bs4 import BeautifulSoup
import requests
import csv
import ast
import time

# start_time = time.time()

def scrape(summoner_name):
    # ts = start_time -time.time()
    # print("started scraping", summoner_name, ": ", ts)
    all_data = []
    _url = 'https://lolchess.gg/profile/na/{}/s9/matches/ranked'.format(summoner_name)
    _page_number =[ '', '/2']
    for i in range(2):
        r = requests.get(_url+_page_number[i])
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
            
    filename = '{}.csv'.format(summoner_name)
    # ts = start_time -time.time()
    # print("finished scraping", summoner_name, ": ", ts)
    write_csv_file(filename, all_data)
    return 
    
    
def write_csv_file(filename, data):
    # ts = start_time -time.time()
    # print("started writing in file: ", ts)
    with open (filename, 'w') as new_file:
        fieldnames = ['placement', 'augments', 'traits', 'champions']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for pl, au, tr, ch in data:
            csv_writer.writerow({'placement': pl, 'augments': au, 'traits': tr, 'champions': ch})
    # ts = start_time -time.time()
    # print("finished writing in file: ", ts)
    return 
            
def find_top_players():        
    # ts = start_time -time.time()
    # print("finding top players: ", ts)
    player_list = []

    top_players = requests.get('https://lolchess.gg/leaderboards?mode=ranked&region=na')
    soup = BeautifulSoup(top_players.content, 'lxml')
    games = soup.find_all('td', {"class": "summoner"})
    for game in games:
        player = game.find('a')
        summonername = player.get_text()
        # summoner name has white spaces which produces error when creating file
        player_list.append(summonername.strip())
    # ts = start_time -time.time()
    # print("finsihed finding top players: ", ts)
    return player_list

def scrape_all(player_list):
    # ts = start_time -time.time()
    # print("started scraping: ", ts)
    for player in player_list:
        scrape(player)


    
    
    
# with open ('matches.csv', 'w') as new_file:
#     fieldnames = ['placement', 'augments', 'traits', 'champions']
#     csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
#     csv_writer.writeheader()
#     for pl, au, tr, ch in all_data:
#         csv_writer.writerow({'placement': pl, 'augments': au, 'traits': tr, 'champions': ch})






def augment_stat():
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
            csv_writer.writerow({'augment': au, 'placement': pl, 'games_played': gm})


# find the list of csv files using a list of player names and combine it into combined.csv
def combine_files(player_list):
    with open("combined.csv", 'w') as new_file:
        fieldnames = ['placement', 'augments', 'traits', 'champions']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for p in player_list:
            pcsv = "{}.csv".format(p)
            with open(pcsv, 'r') as readfile:
                csv_reader = csv.DictReader(readfile)
                for line in csv_reader:
                    csv_writer.writerow(line)


def print_stat(num):
    with open("result.csv", 'r') as readfile:
        csv_reader = csv.DictReader(readfile)
        for line in csv_reader:
            if int(line['games_played']) >= num:
                print('{:<40} {:^30} {:>40}'.format(line['augment'], line['placement'], line['games_played']))


def run():
    player_list = find_top_players()
    scrape_all(player_list)
    combine_files(player_list)
    augment_stat()
    print_stat(30)


run()



    