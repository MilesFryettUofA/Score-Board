# Code that gets live nba teams and scores from espn.com
# By miles Fryett
#TODO switch from PhantomJS to headless web driver
#TODO IMplement adrino logic
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import threading, time
import sys  # For exit
import serial  # For adrino


global data
global d


class game():
	def __init__(self, teamh, teama, scoreh, scorea):
		self.away = teama  # Away team
		self.home = teamh
		self.awayscore = int(scorea)
		self.homescore = int(scoreh)
		# Add time maybe?

	def __str__(self):
		return "%s has %s \n%s has %s" % (self.home, self.homescore, self.away, self.awayscore)


def scrape(URL):
	'''
	go to website that has live stats
	arg(URL): a string that is the URL of the website
	returns(driver): A list of object of games that have matchup and score
	'''
	driver = webdriver.PhantomJS()  # Open PhantomJS to supress browser
	driver.get(URL)  # Go to URL
	driver.refresh();
	return(driver)


def score(driver):
	'''
	gets data from a website for the live stats
	arg(driver): The webdriver
	returns(games): A list of object of games that have matchup and score
	'''
	# The Live changes dont come up on time, span style?
	r = driver.page_source
	soup = BeautifulSoup(r, 'html.parser')  # Raw html obj
	teams = soup.find_all('span', attrs={'class':'sb-team-abbrev'})  # html teams
	results = soup.find_all('td', attrs={'class':'total'})  # html scores

	# Get raw list of strings
	teams = getteam(teams)
	results = getscore(results)

	if len(teams) != len(results):  # Possible error down the road
		print("UH OH espn changed html format likely")

	games = []

	for g in range(0, len(results), 2):
		games += [game(teams[g], teams[g+1], results[g], results[g+1])]
	return(games)


def getteam(team):
	'''
	Gets a list of 
	arg(team): the obj of teams
	returns(text): The string of team aberviations(LIST) (3 letter)
	'''
	text = []
	for i in team:
		text += [i.get_text()]
	return(text)
		

def getscore(score):
	'''
	gets score
	arg(score): the obj of the game score
	returns(text): the string of scores(LIST)
	'''
	text = []
	for i in score:
		text += [i.get_text()]
	return(text)


def get():
	'''
	Inital open web driver and get first data
	Returns(d): Web driver
	'''
	global data
	URL = 'https://www.espn.com/nba/scoreboard'  # ESPN URL
	# URL = 'https://www.espn.com/nba/scoreboard/_/date/20201228'  # Temp
	d = scrape(URL)
	data = score(d)
	print('Data ready')  # just a temp flag
	return(d)


def update(d):
	'''
	updates the scores in data
	args(d): web driver
	'''
	global data
	while True:
		data = score(d)
		time.sleep(2)  # Gets score every 2 seconds, might be worth an arg in future
	return


def printscore():
	'''
	Prints score of all games today
	'''
	global data
	for j in data:
		print('Game')
		print(j)
		print('\n')
	return



def getscorethread(threads = 1):
	'''
	Initalizes thread
	args(threads): number of threads
	returns
		thr: list of all threads
		d: web driver
	'''
	thr = []
	for i in range(0, threads):
		d = get()
		t = threading.Thread( target=update, args =(d,))
		t.daemon = True
		t.start()
		thr.append(t)
	return(thr, d)


def main():
	'''
	Institutes a command line front end
	'''
	on = True
	cmds = ["get - starts getting scores", "stop - exits program", 
	"help - lists all comands", "print - Prints current scores of games today"]
	while on:
		print("input a command")
		command = input()
		command = command.lower()  # Lowecase inputs
		if command == "get":
			thr, d = getscorethread(1)
		elif command == 'stop':
			on = False
			d.quit()  # Ends web driver
			sys.exit()  # Ends program and daemon
		elif command == 'help':
			print("\n")
			print("Commands are ....")
			print("\n")
			for i in cmds:
				print(i)
			print("\n")
		elif command == 'print':
			printscore()
		elif command == 'hide':  # WILL NOT WORK
			print("Shhhh")
			# Do next thing for new command
		else:
			print("command not recognised")
			print('Type help for a list of commands')
	return


if __name__ == '__main__':
	main()
