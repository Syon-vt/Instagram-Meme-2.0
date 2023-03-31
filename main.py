#imports
from praw import Reddit
from requests import get
from time import sleep, time
from instagrapi import Client
from PIL import Image
from os import remove, listdir
from configparser import ConfigParser

#read ini file
cred = ConfigParser()
cred.read('config.ini')

read = Reddit(
	client_id=cred['Reddit']['client_id'],
	client_secret=cred['Reddit']['client_secret'],
	user_agent=cred['Reddit']['user_agent']
)
user = cred['Instagram']['user']
passwd = cred['Instagram']['passwd']

#misc
insta = Client()
memes = read.subreddit("memes")
dankmemes = read.subreddit("dankmemes")

hashtags = "#meme #funny #dankmemes \
            #reddit #memepage #memesdaily \
            #memeshourly #redditmeme #redditmemes \
            #redditmemesdaily #redditrepost #redditfunny \
            #funnymemes #funnymeme #funnyposts \
            #funnypictures #funnypics"

#live timer
def timer(sec:int, text:str="Timer"):
	start = time()
	while time()-start >= 0:
		print(f"{text}: {sec}", end='\r')
		sec = sec - 1
		sleep(1)

#reddit interaction
def reddit(func:str, sub):
	for post in sub.top(time_filter="hour", limit=1):

		if func == "title":
			return post.title
		
		elif func == "author":
			return post.author
		
		elif func == "image":
			with open(f"tmp/meme.jpg", "wb") as img:
				img.write(get(post.url).content)
				return "tmp/meme.jpg"

		elif func == None:
			print("Enter a function!")

		else:
			print("Invalid Input")

#resize image to 1080x1080
def resize(path:str):
	img = Image.open(path)
	img.convert('RGB').resize([1080, 1080]).save('tmp/resize.jpg')
	return "tmp/resize.jpg"

#clear tmp file
def clear_tmp(type):
	for file in listdir('tmp'):

		if type == "img":

			if file.endswith('.jpg') or file.endswith('.jpeg'):
				remove(f"tmp/{file}")

		elif type == 'all':
			remove(file)

####Start Program####

#load settings and login 
try:
	insta.load_settings('tmp/dump.json')
	print("Settings Loaded")
except:
	print("Settings Failed to Load	")

try:
	insta.login(user,passwd)
	print("Logged In")
except:
	print("Failed to Log In")

#main loop
while True:
	try:
		insta.photo_upload(resize(reddit("image", memes)), caption=f"{reddit('title', memes)} \n \n \
	     via Reddit: {reddit('author', memes)} \n \n {hashtags}")
		print("Meme Uploaded")
	except:
		print("Meme Upload Failed")
	clear_tmp('img')
	timer(sec=1800, text="Next Upload In")

	try:
		insta.photo_upload(resize(reddit("image", dankmemes)), caption=f"{reddit('title', dankmemes)} \n \n \
		     via Reddit: {reddit('author', dankmemes)} \n \n {hashtags}")
		print("Dankmeme Uploaded")
		
	except:
		print("Dankmeme Upload Failed")
		
	clear_tmp('img')
	timer(sec=1800, text="Next Upload In")