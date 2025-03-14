import os
import sqlite3
import random
from models.Score import Score

class Database:
    def __init__(self, db_path="databases/hangman_2025.db"):
        self.db_path = db_path

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Andmebaasifaili ei leitud! Otsiti: {os.path.abspath(self.db_path)}")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.check_tables()

    def check_tables(self):
        """Kontrollib, kas vajalikud tabelid on olemas, ja loob puuduva edetabeli."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in self.cursor.fetchall()}

        print("Leitud tabelid andmebaasis:", tables)  # Kontrollime olemasolevaid tabeleid

        if 'words' not in tables:
            print("Tabel 'words' puudub! Palun loo see käsitsi või lisa sõnad.")

        self.cursor.execute("SELECT COUNT(*) FROM words")
        if self.cursor.fetchone()[0] == 0:
            print("Tabel 'words' on tühi! Lisa sinna sõnu!")

        if 'leaderboard' not in tables:
            print("Tabel 'leaderboard' puudub, luuakse uus tabel...")
            self.create_leaderboard()

    def create_leaderboard(self):
        """Loob leaderboard tabeli, kui seda pole olemas."""
        print("Loon leaderboard tabeli...")  # Kontrollin, kas meetod üldse käivitub
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                word TEXT NOT NULL,
                letters TEXT NOT NULL,
                game_length INTEGER NOT NULL,
                game_time TEXT NOT NULL
            )
        """)
        self.conn.commit()
        print("Leaderboard tabel loodud!")

    def get_unique_categories(self):
        """Tagastab unikaalsed kategooriad."""
        self.cursor.execute("SELECT DISTINCT category FROM words")
        return [row[0] for row in self.cursor.fetchall()]

    def get_random_word(self, category=None):
        """Võtab juhusliku sõna andmebaasist valitud kategooria alusel."""
        query = "SELECT word FROM words"
        params = ()
        if category:
            query += " WHERE category=?"
            params = (category,)

        self.cursor.execute(query, params)
        words = self.cursor.fetchall()
        return random.choice(words)[0] if words else None

    def add_score(self, name, word, letters, game_length, game_time):
        """Lisab mängija tulemuse leaderboardi."""
        self.cursor.execute("""
            INSERT INTO leaderboard (name, word, letters, game_length, game_time)
            VALUES (?, ?, ?, ?, ?)
        """, (name, word, letters, game_length, game_time))
        self.conn.commit()


    def get_leaderboard(self):
        """Tagastab järjestatud edetabeli Score objektidena."""
        self.cursor.execute("""
            SELECT name, word, letters, game_length, game_time
            FROM leaderboard
            ORDER BY game_length ASC, LENGTH(letters) ASC
        """)
        result = self.cursor.fetchall()

        return [Score(*row) for row in result]

    def close(self):
        """Sulgeb andmebaasi ühenduse."""
        self.conn.close()
