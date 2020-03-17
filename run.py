import urllib.request, json
import mysql.connector as mariadb
import yaml
import datetime
import time

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

    mariadb_connection = mariadb.connect(
        host=cfg['mysql']['host'],
        port=cfg['mysql']['port'],
        user=cfg['mysql']['user'],
        password=cfg['mysql']['passwd'],
        database='mysql'
    )
    cursor = mariadb_connection.cursor()

    mariadb_connection.close()

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



s1 = Song("Shake it off", "Taylor Swift", "00:00", "", "2020-03-17T10:14:55+01:00",
          "s",
          "s"
          )
"""
while True:
    try:
        with urllib.request.urlopen(cfg['pilatus']['url']) as url:
            currentSong = json.loads(url.read().decode())
            x = time.strptime(currentSong['live'][0]['duration'], '%M:%S')
            currentSong = Song(
                currentSong['live'][0]['title'],
                currentSong['live'][0]['interpret'],
                currentSong['live'][0]['duration'],
                currentSong['live'][0]['label'],
                datetime.datetime.fromisoformat(currentSong['live'][0]['playtime']),
                currentSong['live'][0]['m3uURL'],
                currentSong['live'][0]['imageURL']
            )
            print(currentSong)

            time.sleep(5)
    except urllib.error.HTTPError as e:
        print(e.__dict__)
    except urllib.error.URLError as e:
        print(e.__dict__)
"""