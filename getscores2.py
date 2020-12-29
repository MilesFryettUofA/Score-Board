import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
class game():

	def __init__(self, teamh, teama, scoreh, scorea):
		self.away = teama
		self.home = teamh
		self.awayscore = scorea
		self.homescore = scoreh

	def __str__(self):

		return "%s has %s \n%s has %s" % (self.home, self.homescore, self.away, self.awayscore)


def scrape(URL):
	'''
	gets data from a website for the live stats
	arg(URL): a string that is the URL of the website
	returns(games): A list of object of games that have matchup and score
	'''

	driver = webdriver.Chrome()  # Open chrome
	driver.get(URL)  # Go to URL
	r = driver.page_source
	soup = BeautifulSoup(r, 'html.parser')  # Raw html obj
	teams = soup.find_all('span', attrs={'class':'sb-team-abbrev'})  # html teams
	results = soup.find_all('td', attrs={'class':'total'})  # html scores

	# Get raw list of strings
	teams = getteam(teams)
	results = getscore(results)

	if len(teams) != len(results):  # Possible error down the road
		print("UH OH espn changed html format likely")
		quit()

	games = []
	for g in range(0, len(teams), 2):
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




def main():
	# URL = 'https://www.espn.com/nba/scoreboard'  # ESPN URL
	URL = 'https://www.espn.com/nba/scoreboard/_/date/20201228'
	data = scrape(URL)
	print(data)
	print(data[0])
	
	return


if __name__ == '__main__':
	main()
