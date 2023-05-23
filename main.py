#[Imports]#
from praw import Reddit
from requests import get
from time import sleep, strftime
from instagrapi import Client
from PIL import Image
from os import remove, listdir
from configparser import ConfigParser
from urllib.request import urlopen

#[Initialize]#
#read ini files
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

#[Funtions]#
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
	return strftime(r'%A, %d %B %Y, %I:%M %p')

#reddit interaction
def reddit(sub):

	global title
	global author

	for post in sub.top(time_filter="hour", limit=1):

		title =  post.title
	
		author =  post.author
	
		with open(f"tmp/meme.jpg", "wb") as img:
			img.write(get(post.url).content)

#resize image to 1080x1080
def resize(path):
	img = Image.open(path)
	img.convert('RGB').resize([1080, 1080]).save('tmp/resize.jpg')

#clear tmp folder
def clear_tmp():
	for file in listdir('tmp'):

			if file.endswith('.jpg') or file.endswith('.jpeg'):
				remove(f"tmp/{file}")

#check if wifi is connected
def wifi():
	try:
		urlopen("https://google.com")
		return True
	except:
		print(f"Wifi is not connected!{current_time()}")
		return False
	
#upload meme
def upload():
		while wifi()==False:
			sleep(600)
			wifi()
		insta.photo_upload("tmp/resize.jpg", caption=f"{title} \n \n \
		 via Reddit: {author} \n \n {hashtags}")


#[Program Start]#
while wifi()==False:
	sleep(600)
	wifi()

try:
	insta.load_settings('tmp/dump.json')
	print("Settings Loaded")
except:
	print("Settings Failed to Load")

try:
	insta.login(user,passwd)
	print("Logged In")
except:
	input("Failed to Log In")
	

#main loop
while True:
	try:
		reddit(memes)
		resize("tmp/meme.jpg")
		upload()
		num = num+1
		print(f"{num}. Meme Uploaded on {current_time()}\n")
	except:
		input(f"Meme Upload Failed on {current_time()}")

	timer()

	try:
		reddit(dankmemes)
		resize("tmp/meme.jpg")
		upload()
		num = num+1
		print(f"{num}. Dankmeme Uploaded on {current_time()}\n")
	except:
		input(f"Dankmeme Upload Failed on {current_time()}")
		quit()

	clear_tmp()
	timer()