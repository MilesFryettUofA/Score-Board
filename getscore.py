# Code that gets live nba teams and scores from espn.com
# By miles Fryett

'''
Todo

- Add loop so scores are updated live
- Close or hide browser driver
- Decide on format of data and format it
- GUI?

''' 
# Global variables end(stops threads) d(driver)
# TODO clean up driver d global at least
# The printing on the thread is weird and still wont close correctly.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import threading, time
import pandas as pd  # Not in use curently 


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
	driver = webdriver.Chrome()  # Open chrome
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



def driver( first = False):
	'''
	driver function for thread
	end(end) boolian if end is 
	first(bool) Only opens driver on first run
	'''
	if first is True:
		global d
		URL = 'https://www.espn.com/nba/scoreboard'  # ESPN URL
		# URL = 'https://www.espn.com/nba/scoreboard/_/date/20201228'  # Temp
		d = scrape(URL)
	data = score(d)
	print(data)
	for j in data:
		print('Game')
		print(j)
		print('\n')
	if end is False:
		time.sleep(1)
		driver(False)
	return

def getscorethread(threads = 1):
	thr = []
	for i in range(0, threads):
		global end
		end = False
		stop = False
		t= threading.Thread( target=driver, args =(True,))
		t.start()
		thr.append(t)
	return(thr)

def jointhr(thr):
	'''
	Joins threads
	arg(thr) list of threads to be joined
	returns None
	'''
	for t in thr:
		end = True
		t.join()
	return



def main():
	thr = getscorethread(1)
	time.sleep(60)
	jointhr(thr)

	input()
	return



if __name__ == '__main__':
	main()
