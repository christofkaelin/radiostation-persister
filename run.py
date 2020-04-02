
import os
import yaml
import mysql.connector as mariadb
import sys
import urllib.request, json
import ssl
import certifi
import datetime
import dateutil.parser
import time
from pytz import timezone

# Define Song class
class Song:
    def __init__(self, title, interpret, playtime, imageURL):
        self.title = title
        self.interpret = interpret
        self.playtime = playtime
        self.imageURL = imageURL

    def __str__(self):
        return str({
            'title': self.title,
            'interpret': self.interpret,
            'playtime': self.playtime,
            'imageURL': self.imageURL
        })

    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        elif self is None or other is None:
            return False
        return self.title == other.title and self.interpret == other.interpret

    def save_to_db(self):
        cur.execute('INSERT INTO '
                    + cfg['db']['table'] +
                    ' (title, interpret, playtime, imageURL) VALUES("'
                    + self.title + '", "'
                    + self.interpret + '", "'
                    + str(datetime.datetime.strftime(self.playtime, '%Y-%m-%d %H:%M:%S')) + '", "'
                    + self.imageURL
                    + '");'
                    )

if os.path.isfile('config.yaml'):
    with open('config.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
else:
    print('config.yaml does not exist. Save config-sample.yaml as config.yaml and adapt the file.')
    sys.exit(1)


# Startup, connect to server and create DB and table
try:
    conn = mariadb.connect(
        host=cfg['db']['host'],
        port=cfg['db']['port'],
        user=cfg['db']['user'],
        password=cfg['db']['passwd']
    )
except mariadb.Error as e:
    print('Error connecting to MariaDB Platform: {e}')
    sys.exit(1)
cur = conn.cursor()
cur.execute('CREATE DATABASE IF NOT EXISTS ' + cfg['db']['db'] + ';')
conn.connect(database=cfg['db']['db'])
cur.execute('CREATE TABLE IF NOT EXISTS '
            + cfg['db']['table'] + ' ('
            'id int NOT NULL PRIMARY KEY AUTO_INCREMENT, '
            'title TINYTEXT, '
            'interpret TINYTEXT, '
            'playtime DATETIME(0), '
            'imageURL TINYTEXT'
            ');'
            )
conn.close()

# Set time zone
time_zone = timezone(cfg['radio']['timezone'])

# Construct previousSong object for first run
previousSong = Song(None, None, datetime.datetime(1970, 1, 1, 0, 0, 0, 0, time_zone), None)

while True:
    try:
        # Get current song and create Song object
        with urllib.request.urlopen(
                cfg['radio']['url'] + '?' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S%f'),
                context=ssl.create_default_context(cafile=certifi.where())) as url:
            currentSong = json.loads(url.read().decode())
            print (currentSong)
            if (currentSong['data']['audioPlayer']['stream']['live']['title'] is not None and
                currentSong['data']['audioPlayer']['stream']['live']['interpret'] is not None and
                currentSong['data']['audioPlayer']['stream']['live']['playtime'] is not None and
                currentSong['data']['audioPlayer']['stream']['live']['image']['imageUrl'] is not None):
                if (currentSong['data']['audioPlayer']['stream']['live']['image'] != 'None' or
                   currentSong['data']['audioPlayer']['stream']['live']['image'] is not None):
                    currentSong = Song(
                        currentSong['data']['audioPlayer']['stream']['live']['title'],
                        currentSong['data']['audioPlayer']['stream']['live']['interpret'],
                        time_zone.localize(
                            dateutil.parser.isoparse(currentSong['data']['audioPlayer']['stream']['live']['playtime'])
                                .replace(tzinfo=None)
                        ),
                        currentSong['data']['audioPlayer']['stream']['live']['image']['imageUrl']
                    )
                else:
                    currentSong = Song(
                        currentSong['data']['audioPlayer']['stream']['live']['title'],
                        currentSong['data']['audioPlayer']['stream']['live']['interpret'],
                        time_zone.localize(
                            dateutil.parser.isoparse(currentSong['data']['audioPlayer']['stream']['live']['playtime'])
                                .replace(tzinfo=None)
                        ),
                        ''
                    )
            else:
                time.sleep(5)
            if currentSong.__eq__(previousSong) is False:
                if currentSong.playtime > previousSong.playtime:
                    try:
                        conn = mariadb.connect(
                            host=cfg['db']['host'],
                            port=cfg['db']['port'],
                            user=cfg['db']['user'],
                            password=cfg['db']['passwd'],
                            database=cfg['db']['db']
                        )
                    except mariadb.Error as e:
                        print('Error connecting to MariaDB Platform: {e}')
                        sys.exit(1)
                    cur = conn.cursor()
                    currentSong.save_to_db()
                    conn.commit()
                    conn.close()
                    previousSong = currentSong
                    conn.close()
        time.sleep(15)

    except urllib.error.HTTPError as e:
        print(e.__dict__)
    except urllib.error.URLError as e:
        print(e.__dict__)
