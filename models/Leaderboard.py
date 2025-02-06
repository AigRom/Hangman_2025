import os.path

from models.Score import Score


class Leaderboard:
    def __init__(self):
        self.__file_path = os.path.join('databases', 'leaderboard.txt')
        self.check_file()

    def check_file(self):
        if not os.path.exists(self.__file_path):
            self.create_leaderboard()

    def create_leaderboard(self):
        header = ['name', 'word', 'letters', 'game_length', 'game_time']
        with open(self.__file_path, 'a', encoding='utf-8') as f:
            f.write(';'.join(header) + '\n')

    def read_leaderboard(self):
        leaderboard = [] #kõik read listi
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines() #ridu ei ole failis

            if not lines:
                return[] #tühi list

            for line in lines[1:]: #alates teisest reast
                line = line.strip()
                name, word, letters, game_length, game_time = line.split(';')
                leaderboard.append(Score(name, word, letters, int(game_length), game_time))

            leaderboard=sorted(leaderboard, key=lambda x: (x.game_length, len(x.letters.split(', '))))

        return leaderboard


    @property
    def file_path(self):
        return self.__file_path # failinimi koos kaustaga satabases/leaderboard.txt
