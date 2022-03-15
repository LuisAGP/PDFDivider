import sqlite3



class DB:
    def __init__(self):
        self.con = sqlite3.connect('pdfsplitter.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

        exists = self.cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='last_url'")

        if exists.fetchone()[0] == 0:
            self.cur.execute('CREATE TABLE last_url (id_last_url INTEGER PRIMARY KEY, url TEXT NOT NULL);')
            self.cur.execute('INSERT INTO last_url (id_last_url, url) VALUES(1, "/");')

            self.con.commit()





    '''
    Function to get the last url for the filemanager
    @author Luis GP
    @return String
    '''
    def getLatUrl(self):
        self.cur.execute('SELECT url FROM last_url WHERE id_last_url')
        return self.cur.fetchone()['url']





    '''
    Function to update the last url for
    @author Luis GP
    @param String
    @return None
    '''
    def setLastUrl(self, url):
        self.cur.execute(f'UPDATE last_url SET url="{url}"')
        self.con.commit()
        return None


        