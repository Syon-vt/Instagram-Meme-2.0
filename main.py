#imports
from praw import Reddit
from requests import get
from time import sleep, strftime
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
num = 0
hashtags = "#meme #funny #dankmemes \
            #reddit #memepage #memesdaily \
            #memeshourly #redditmeme #redditmemes \
            #redditmemesdaily #redditrepost #redditfunny \
            #funnymemes #funnymeme #funnyposts \
            #funnypictures #funnypics"

#live timer
def timer():
	sec = 1800
	while sec >= 0:
		print(f"Next Upload In: {sec} seconds", end='\r')
		sec = sec - 1
		sleep(1)
	print()

#get current date and time
def current_time():
	return strftime(r'%A, %d %B %Y, %I:%M:%S')

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

		elif func == None:
			print("Enter a function!")

		else:
			print("Invalid Input")

#resize image to 1080x1080
def resize(path):
	img = Image.open(path)
	img.convert('RGB').resize([1080, 1080]).save('tmp/resize.jpg')

#clear tmp file
def clear_tmp(type):
	for file in listdir('tmp'):

		if type == "img":

			if file.endswith('.jpg') or file.endswith('.jpeg'):
				remove(f"tmp/{file}")

		elif type == 'all':
			remove(file)


#load settings and login 
try:
	insta.load_settings('tmp/dump.json')
	print("Settings Loaded")
except:
	print("Settings Failed to Load")

try:
	insta.login(user,passwd)
	print("Logged In")
except:
	print("Failed to Log In")
	quit()

#main loop
while True:
	try:
		reddit("image", memes)
		resize("tmp/meme.jpg")
		insta.photo_upload("tmp/resize.jpg", caption=f"{reddit('title', memes)} \n \n \
		 via Reddit: {reddit('author', memes)} \n \n {hashtags}")
		num = num+1
		print(f"{num}. Meme Uploaded on {current_time()}")
		
	except:
		print(f"Meme Upload Failed on {current_time()}")
	clear_tmp('img')
	timer()

	try:
		reddit("image", dankmemes)
		resize("tmp/meme.jpg")
		insta.photo_upload("tmp/resize.jpg", caption=f"{reddit('title', dankmemes)} \n \n \
		     via Reddit: {reddit('author', dankmemes)} \n \n {hashtags}")
		num = num+1
		print(f"{num}. Dankmeme Uploaded on {current_time()}")
		
	except:
		print(f"Dankmeme Upload Failed on {current_time()}")
		
	clear_tmp('img')
	timer()