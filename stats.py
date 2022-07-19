class PlayerStats:

    def __init__(self, file_name):
        self.players = self.build(file_name)
        self.used_files = {file_name}

    def build(self, file_name):
        file = open(file_name)
        lines, dict = file.readlines()[1:], {}
        for line in lines:
            data = line.split()[3:]
            dict[data[0].lower()] = \
                    [float(data[1]), int(data[2][:data[2].index('-')]), int(data[2][data[2].index('-') + 1:]), \
                    int(data[4][:data[4].index('-')]), int(data[4][data[4].index('-') + 1:]), int(data[6]), \
                    float(data[7][:-1]) / 100, float(data[8]), float(data[9][:-1]) / 100] + [int(x) for x in data[10:13]] + \
                    [float(data[13][:-1]) / 100, data[14][:len(data[14]) // 2], data[15][:len(data[15]) // 2]]
            dict[data[0].lower()].append(round(dict[data[0].lower()][1] / dict[data[0].lower()][7]))
        file.close()
        return dict

    def add_data(self, file_name):
        try:
            second = self.build(file_name)
        except:
            print('That is not a valid file path.')
            return
        self.used_files.add(file_name)
        for player in second:
            if player not in self.players:
                self.players[player] = second[player]
            else:
                curr = self.players[player]
                curr[0] = round((curr[0] * curr[15] + second[player][0] * \
                        second[player][15]) / (curr[15] + second[player][15]), 2)
                for i in range(1, 6):
                    curr[i] += second[player][i]
                curr[6] = round((curr[6] * curr[15] + second[player][6] * \
                        second[player][15]) / (curr[15] + second[player][15]), 2)
                curr[7] = round((curr[7] * curr[15] + second[player][7] * \
                        second[player][15]) / (curr[15] + second[player][15]), 2)
                curr[8] = round((curr[8] * curr[15] + second[player][8] * \
                        second[player][15]) / (curr[15] + second[player][15]), 2)
                curr[9:12] = [x + y for x, y in zip(curr[9:12], second[player][9:12])]
                curr[12] = round((curr[12] * curr[15] + second[player][12] * \
                        second[player][15]) / (curr[15] + second[player][15]), 2)
                if second[player][15] > curr[15]:
                    curr[13] = second[player][13]
                    curr[14] = second[player][14]
                curr[15] += second[player][15]
                self.players = dict(sorted(self.players.items(), key = lambda x: x[1], reverse = True))

    def rating(self, player):
        return self.players[player][0]

    def KOST(self, player):
        return self.players[player][6]

    def KPR(self, player):
        return self.players[player][7]

    def survival(self, player):
        return self.players[player][8]

    def clutches(self, player):
        return self.players[player][9]

    def plants(self, player):
        return self.players[player][10]

    def disables(self, player):
        return self.players[player][11]

    def HS(self, player):
        return self.players[player][12]

    def attacker(self, player):
        return self.players[player][13]

    def defender(self, player):
        return self.players[player][14]

    def rounds(self, player):
        return self.players[player][15]

    def player_set(self):
        return set(self.players.keys())

    def KD_stats(self, player):
        kills, deaths = self.players[player][1:3]
        print(player, 'K/D stats:', str(kills) + '-' + str(deaths), \
                ('(+' if kills >= deaths else '(') + \
                str(kills - deaths) + ')', \
                str(round(kills / deaths, 2)))

    def entry_stats(self, player):
        kills, deaths = self.players[player][3:5]
        print(player, 'entry K/D stats:', str(kills) + '-' + str(deaths), \
                ('(+' if kills >= deaths else '(') + \
                str(kills - deaths) + ')', \
                str(round(kills / deaths, 2)))

    def map_stats(self, player):
        stats = self.players[player]
        print(player, 'maps played:', str(stats[5]) + ', average per map stats:', \
            str(round(stats[1] / stats[5], 2)), 'kills,', \
            str(round(stats[2] / stats[5], 2)), 'deaths,', \
            str(round(stats[3] / stats[5], 2)), 'entry kills,')
        print(str(round(stats[4] / stats[5], 2)), 'entry deaths,', \
            str(round(stats[9] / stats[5], 2)), 'clutches,', \
            str(round(stats[10] / stats[5], 2)), 'plants,', \
            str(round(stats[11] / stats[5], 2)), 'disables,', \
            str(round(stats[15] / stats[5], 2)), 'rounds')

    def view_data(self):
        print('Player:      [RTG, Ks, Ds, EKs, EDs, Maps, KOST, KPR, SRV,',
              '1vXs, Plants, Disables, HS%, ATK Op, DEF Op, Rounds]')
        for player in self.players:
            print(player + ':' + (' ' * (12 - len(player))) + str(self.players[player]))

    def commands(self):
        print('GENERAL: add_data, view_players, view_data, commands')
        print('FOR PLAYERS: rating, KD_stats, entry_stats, map_stats, KOST, KPR, survival,')
        print('             clutches, plants, disables, HS, attacker, defender, rounds')

    def get_player(self):
        player = ' '
        while player not in self.players:
            print('Enter the name of a player from the data in lower case letters.')
            print('To see the player list, enter "players".')
            player = input()
            print('')
            if player == 'players':
                    print('Players:', self.player_set())
                    print('')
            elif player not in self.players:
                    print('Try again.')
        return player


if __name__ == '__main__':
    file_set = {'data/BR 2022 Stage 2.txt', 'data/NA 2021 Stage 1.txt', \
                'data/NA 2021 Stage 2.txt', 'data/NA 2021 Stage 3.txt', \
                'data/NA 2022 Stage 1.txt', 'data/NA 2022 Stage 2.txt', 'test.txt'}
    file_name = comm = ' '
    while file_name not in file_set:
        print('Enter file name.')
        print('To see the usable files, enter "files".')
        print('To exit the program, enter "exit".')
        file_name = input('')
        print('')
        if file_name == 'exit':
            break
        if file_name == 'files':
            print(file_set)
        elif file_name not in file_set:
            print('Try again.')
    if file_name != 'exit':
        ps = PlayerStats(file_name)
        while comm != 'exit':
            print('What would you like to do?')
            print('For a list of options, enter "commands".')
            print('To exit the program, enter "exit".')
            comm = input()
            print('')
            if comm == 'commands':
                ps.commands()
            elif comm == 'view_players':
                print(ps.player_set())
            elif comm == 'view_data':
                ps.view_data()
            elif comm == 'add_data':
                file_name = ' '
                while file_name not in file_set:
                    print('Enter file name.')
                    print('To see the usable files, enter "files".')
                    print('To enter a different command, enter "exit".')
                    file_name = input()
                    if file_name == 'exit':
                        break
                    else:
                        print('')
                    if file_name == 'files':
                        print('Files:', file_set)
                    elif file_name in ps.used_files:
                        print('That file is already in use.')
                        file_name = ' '
                    elif file_name not in file_set:
                        print('Try again.')
                ps.add_data(file_name)
            elif comm == 'rating':
                player = ps.get_player()
                print(player, 'rating:', ps.rating(player))
            elif comm == 'KD_stats':
                player = ps.get_player()
                ps.KD_stats(player)
            elif comm == 'entry_stats':
                player = ps.get_player()
                ps.entry_stats(player)
            elif comm == 'map_stats':
                player = ps.get_player()
                ps.map_stats(player)
            elif comm == 'KOST':
                player = ps.get_player()
                print(player, 'KOST %:', ps.KOST(player))
            elif comm == 'KPR':
                player = ps.get_player()
                print(player, 'kill per round:', ps.KPR(player))
            elif comm == 'survival':
                player = ps.get_player()
                print(player, 'survival %:', ps.survival(player))
            elif comm == 'clutches':
                player = ps.get_player()
                print(player, 'clutches:', ps.clutches(player))
            elif comm == 'plants':
                player = ps.get_player()
                print(player, 'plants:', ps.plants(player))
            elif comm == 'disables':
                player = ps.get_player()
                print(player, 'disables:', ps.disables(player))
            elif comm == 'HS':
                player = ps.get_player()
                print(player, 'headshot %:', ps.HS(player))
            elif comm == 'attacker':
                player = ps.get_player()
                print(player, 'most played* attacking operator:', ps.attacker(player))
                print('*most played from the data in which they have the most rounds played')
            elif comm == 'defender':
                player = ps.get_player()
                print(player, 'most played* defender:', ps.defender(player))
                print('*most played from the data in which they have the most rounds played')
            elif comm == 'rounds':
                player = ps.get_player()
                print(player, 'rounds played:', ps.rounds(player))
            print('')
