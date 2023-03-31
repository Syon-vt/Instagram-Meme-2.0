#imports
from instagrapi import Client
from configparser import ConfigParser
from os import mkdir

#init
config = ConfigParser()
insta = Client()

#create files
mkdir('tmp')
open('tmp/dump.json', 'w').close()

#login and dump settings
config.read('config.ini')
insta.login(config['Instagram']['user'], config['Instagram']['passwd'])
insta.dump_settings('tmp/dump.json')