import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


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

	for g in range(1, (len(teams) // 2) +1):
		games = {}
		for t,s in zip(teams, results):
			name = 'Game' + str(g)
			tup = (t , s)
			games[name] = tup  # PROBLEMS 
			# Switch to an object from a dict, that way each game can be in a coustion data set obj
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
	URL = 'https://www.espn.com/nba/scoreboard'  # ESPN URL
	data = scrape(URL)
	for key in data.keys():  # Driver
		print(key)
	
	return


if __name__ == '__main__':
	main()
