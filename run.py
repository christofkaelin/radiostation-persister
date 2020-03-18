import os
import yaml
import mysql.connector as mariadb
import sys
import urllib.request, json
import datetime
import time

# Define Song class
class Song:
    def __init__(self, title, interpret, duration, label, playtime, m3uURL, imageURL):
        self.title = title
        self.interpret = interpret
        self.duration = duration
        self.label = label
        self.playtime = playtime
        self.m3uURL = m3uURL
        self.imageURL = imageURL

    def __str__(self):
        return str({
            'title': self.title,
            'interpret': self.interpret,
            'duration': self.duration,
            'label': self.label,
            'playtime': self.playtime,
            'm3uURL': self.m3uURL,
            'imageURL': self.imageURL
        })

    def __eq__(self, other):
        if not isinstance(other, Song):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.title == other.title and self.interpret == other.interpret and self.playtime == other.playtime

if os.path.isfile('config.yaml'):
    with open('config.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
else:
    print('config.yaml does not exist. Save config-sample.yaml as config.yaml and adapt the file.')
    sys.exit(1)

# Instantiate Connection
try:
    conn = mariadb.connect(
        host=cfg['mysql']['host'],
        port=cfg['mysql']['port'],
        user=cfg['mysql']['user'],
        password=cfg['mysql']['passwd']
    )
except mariadb.Error as e:
    print('Error connecting to MariaDB Platform: {e}')
    sys.exit(1)

# Instantiate Cursor
cur = conn.cursor()

# Create DB and select it
cur.execute('CREATE DATABASE IF NOT EXISTS ' + cfg['mysql']['db'])
conn.connect(database=cfg['mysql']['db'])

# Create table
cur.execute('CREATE TABLE IF NOT EXISTS songs ('
            'title TINYTEXT, '
            'interpret TINYTEXT, '
            'duration TIME(0), '
            'label TINYTEXT, '
            'playtime DATETIME(0), '
            'm3uURL TINYTEXT, '
            'imageURL TINYTEXT);')

while True:
    try:
        with urllib.request.urlopen(cfg['pilatus']['url']) as url:
            currentSong = json.loads(url.read().decode())
            x = time.strptime(currentSong['live'][0]['duration'], '%M:%S')
            currentSong = Song(
                currentSong['live'][0]['title'],
                currentSong['live'][0]['interpret'],
                time.strptime(currentSong['live'][0]['duration'], '%M:%S'),
                currentSong['live'][0]['label'],
                datetime.datetime.fromisoformat(currentSong['live'][0]['playtime']),
                currentSong['live'][0]['m3uURL'],
                currentSong['live'][0]['imageURL']
            )
            print(currentSong)
            cur.execute('INSERT INTO songs (title, interpret, duration, label, playtime, m3uURL, imageURL) VALUES("'
                        + currentSong.title + '", "'
                        + currentSong.interpret + '", "'
                        + time.strftime('%M:%S', currentSong.duration) + '", "'
                        + currentSong.label + '", "'
                        + str(datetime.datetime.strftime(currentSong.playtime, '%Y-%m-%d %H:%M:%S')) + '", "'
                        + currentSong.m3uURL + '", "'
                        + currentSong.imageURL
                        + '");'
                        )
            conn.commit()
            time.sleep(60)
    except urllib.error.HTTPError as e:
        print(e.__dict__)
    except urllib.error.URLError as e:
        print(e.__dict__)

# Close Connection
conn.close()