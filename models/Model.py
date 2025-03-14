

import glob
import os
import random
from datetime import datetime

#from models.FileObject import FileObject #vaja kui kasutada tekstipõhist andmebaasi
from models.Database import Database
#from models.Leaderboard import Leaderboard


class Model:
    def __init__(self):
        self.__image_files = [] # tühi list piltide jaoks
        self.load_images('images')
        #self.__file_object = FileObject('databases', 'words.txt') #vaja kui kasutada tekstipõhist andmebaasi


        self.db = Database()
        #self.__categories = self.__file_object.get_unique_categories() #võtab kategooriad tekstifailist
        self.__categories = self.db.get_unique_categories() #võtab kategooriad andmebaasist
        #self.__scoreboard = Leaderboard()
        self.titles = ['Poomismäng 2025', 'Kas jäid magama?', 'Ma ootan su käiku!', 'Sisesta juba see täht!', 'Zzzzz....']

        #Mängu muutujad
        self.__new_word = None #juhuslik sõna mängu jaoks
        self.__user_word = [] #kõik kasutaja leitud tähed
        self.__counter = 0 #vigade loendur
        self.__all_user_chars = [] #valesti sisestatud tähed





    def load_images(self, folder):
        if not os.path.exists(folder):
            raise FileNotFoundError(f'Kausta {folder} ei ole.')

        images = glob.glob(os.path.join(folder, '*.png'))
        if not images:
            raise FileNotFoundError(f'Kausta {folder} ei ole PNG laiendiga faile.')

        self.__image_files = images

    def start_new_game(self, category_id, category):
        if category_id == 0:
            category = None


        #self.__new_word = self.__file_object.get_random_word(category) #võtab sõnad teksti failist
        self.__new_word = self.db.get_random_word(category)  # Võta juhuslik sõna ja kategooria
        self.__user_word = [] #algseis
        self.__counter = 0 #algseis
        self.__all_user_chars = [] #algseis

        #Asenda kõik tähed allkriipsuga M A J A => _ _ _ _
        for x in range(len(self.__new_word)):
            self.__user_word.append('_')

    def get_user_input(self, user_input):
        if user_input:
            user_char = user_input[:1] #esimene märk sisestusest
            if user_char.lower() in self.__new_word.lower():
                self.change_user_input(user_char) #leiti täht
            else: #ei leitud tähte
                self.__counter += 1
                self.__all_user_chars.append(user_char.upper())



    def change_user_input(self, user_char):
        current_word = self.char_to_list(self.__new_word)
        x = 0
        for c in current_word:
            if c.lower() == user_char.lower():
                self.__user_word[x] = user_char.upper()
            x += 1

    def get_all_user_chars(self):
        return ', '.join(self.__all_user_chars)




    @staticmethod
    def char_to_list(word):
        #Str to List test => ['t', 'e', 's', 't']
        chars = []
        chars[:0] = word
        return chars

    def save_player_score(self, name, seconds):
        today=datetime.now().strftime('%Y-%m-%d %T')

        if not name.strip(): #Nime ei ole
            name = random.choice(['Tundmatu', 'Teadmata', 'Unknown'])

        #with open(self.__scoreboard.file_path, 'a', encoding='utf-8') as f:
           # line = ';'.join([name.strip(), self.__new_word, self.get_all_user_chars(), str(seconds), today])
            #f.write(line+ '\n')
        self.db.cursor.execute("""
                INSERT INTO leaderboard (name, word, letters, game_length, game_time)
                VALUES (?, ?, ?, ?, ?)
            """, (name.strip(), self.__new_word, self.get_all_user_chars(), seconds, today))

        self.db.conn.commit()
        print("Tulemused salvestatud!")

    # GETTERS

    @property
    def categories(self):
        """Tagastab kategooriate listi"""
        return self.__categories


    @property
    def image_files(self):
        """Tagastab piltide listi"""
        return self.__image_files
    @property
    def user_word(self):
        return self.__user_word

    @property
    def counter(self):
        return self.__counter
