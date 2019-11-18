import fire
import sys
import subprocess
import re
import requests
import json
import eyed3
from urllib.request import urlopen
import time
from PIL import Image
from io import BytesIO
import os.path
from os import path
import unidecode
from colorama import init
from colorama import Fore, Back, Style


class YouTag(object):
    def __init__(self):
        self.current_song_name = ""
        self.current_song_url = ""
        self.image_name = ""
        self.validation = Validate()

    def get_video(self, url):
        if not self.validation.url_is_valid(url):
            sys.exit(Fore.RED + "Please provide a valid URL and try again")
        else:
            subprocess.call(['youtube-dl', '--extract-audio', '--audio-format',
                             'mp3', url])
            song_name = subprocess.check_output(
                ['youtube-dl', '-e', url])
            ready_song_name = self.clean_song_name(song_name)
            self.current_song_url = url.split("=",1)[1]
            self.get_song_data(ready_song_name)

    def get_videos(self, urls):
        song_list = urls.split(",")

        for song in song_list:
            self.get_video(song)


    def clean_song_name(self, song_name):
        if song_name.isascii():
            # Regex would work better but I hate regex.
            song_name = song_name.decode('unicode_escape').encode('utf-8')
            song_name = song_name.decode("utf-8")
            song_name = unidecode.unidecode(song_name)
            self.current_song_name = song_name.strip()
            firstDelPos = song_name.find("(")
            secondDelPos = song_name.find(")")
            song_name = song_name.replace(
                song_name[firstDelPos:secondDelPos+1], "")
            return song_name.replace(" - ", " ")
        else:
            sys.exit(Fore.YELLOW + """Sorry, only ascii characters are supported right now.""")

    def get_song_data(self, ready_song_name):
        response = requests.get(
            f'https://api.deezer.com/search?q={ready_song_name}&limit=2')
        if response:
            data = json.loads(response.content)
            if self.validation.valid_from_deezer(data) is True:
                album_art_url = data['data'][0]['album']['cover_medium'].strip(
                )
                response = requests.get(album_art_url)
                img = Image.open(BytesIO(response.content))
                self.image_name = f'{self.current_song_name}-{self.current_song_url}'
                img = img.save(f'{self.image_name}.jpg')
                self.tag_file(data)
                self.remove_album_art()
                sys.exit(Fore.GREEN + "Download and tag completed successfully!")
            else:
                sys.exit(Fore.YELLOW + "Deezer was unable to provide any data for the provided file. However, the song has still been downloaded")

        else:
            sys.exit(Fore.RED + "An unexpected error occured. Please try again.")

    def remove_album_art(self):
        if path.exists(f'{self.image_name}.jpg'):
            os.remove(f'{self.image_name}.jpg')
        else:
            print('Nothing to remove')

    def tag_file(self, data):
        try:
            audiofile = eyed3.load(
                f"{self.current_song_name}-{self.current_song_url}.mp3")
            print(Fore.BLUE + "Successfully loaded file")
        except FileNotFoundError:
            raise

        audiofile.tag.artist = data['data'][0]['artist']['name']
        print(Fore.GREEN + f"Setting artist name => {data['data'][0]['artist']['name']}")
        audiofile.tag.album = data['data'][0]['album']['title']
        print(Fore.GREEN + f"Setting album name => {data['data'][0]['album']['title']}")
        audiofile.tag.title = data['data'][0]['title_short']
        print(Fore.GREEN + f"Setting song title => {data['data'][0]['title_short']}")
        image_data = open(f'{self.image_name}.jpg', "rb").read()
        audiofile.tag.images.set(
            3, image_data, "image/jpeg", u"you can put a description here")
        print(Fore.GREEN + "Setting album art")
        audiofile.tag.save()


class Validate():
    def url_is_valid(self, url):
        if len(url) > 0 and 'https://www.youtube' in url:
            return True
        else:
            return False

    def valid_from_deezer(self, data):
        if not data['total']:
            return False
        else:
            return True


# https://youtu.be/a02Nz7TJExI
if __name__ == '__main__':
    init(autoreset=True)
    fire.Fire(YouTag)
