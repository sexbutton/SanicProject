import sqlite3
import random, string
from sanic import Sanic
class Database:
    #session_id = request.cookies.get('session_id')
    #session_id = str(uuid.uuid4())
    '''
    @app.route('/login')
async def login(request):
    # В реальной ситуации аутентификация будет проводиться, и здесь
    # вы будете иметь user_id после успешной аутентификации.
    user_id = '123'  # Здесь вы должны использовать фактический user_id

    session_id = create_session(user_id)
    response = redirect('/')
    response.cookies['session_id'] = session_id
    return response
    '''
    def create_session(session_id, user_id):
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO Sessions (session_id, User) VALUES (?, ?)', (session_id, user_id)) 
        return session_id
    def get_user_id(session_id):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute('SELECT User FROM Sessions WHERE session_id = ?', (session_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
    @staticmethod
    def StartDatabase():
        with sqlite3.connect('database.db') as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS Sessions (
                         session_id TEXT PRIMARY KEY, 
                         User INTEGER NOT NULL),
                         FOREIGN KEY (User) REFERENCES Users (id)
                         ''')
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