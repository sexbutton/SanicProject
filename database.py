import sqlite3
import random, string
class Database:
    @staticmethod
    def StartDatabase():
        with sqlite3.connect('database.db') as conn:
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Login TEXT NOT NULL,
                    Password TEXT NOT NULL,
                    Name TEXT NOT NULL,
                    Description TEXT,
                    PfpPath TEXT NOT NULL
                   )
                ''')
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Path TEXT NOT NULL,
                    Description TEXT NOT NULL,
                    OwnerId INTEGER NOT NULL,
                    DateTime DATETIME NOT NULL,
                    FOREIGN KEY (OwnerId) REFERENCES Users (id)
                   )
                ''')
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS VideoReactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    VideoId INTEGER NOT NULL,
                    ReactorId INTEGER NOT NULL,
                    IsLike INTEGER NOT NULL,
                    FOREIGN KEY (VideoId) REFERENCES Videos (id)
                    FOREIGN KEY (ReactorId) REFERENCES Users (id)
                   )
                ''')
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS VideoWatches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    WatcherId INTEGER NOT NULL,
                    VideoId INTEGER NOT NULL,
                    FOREIGN KEY (WatcherId) REFERENCES Users (id)
                    FOREIGN KEY (VideoId) REFERENCES Videos (id)
                   )
                ''')
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    CommentatorId INTEGER NOT NULL,
                    VideoId INTEGER NOT NULL,
                    Text TEXT NOT NULL,
                    DateTime DATETIME NOT NULL,
                    FOREIGN KEY (CommentatorId) REFERENCES Users (id)
                   )
                ''')
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS CommentReactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    CommentId INTEGER NOT NULL,
                    ReactorId INTEGER NOT NULL,
                    IsLike INTEGER NOT NULL,
                    FOREIGN KEY (CommentId) REFERENCES Comments (id)
                    FOREIGN KEY (ReactorId) REFERENCES Users (id)
                   )
                ''')
Database.StartDatabase()