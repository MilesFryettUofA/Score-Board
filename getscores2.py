import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def scrape(URL):

	driver = webdriver.Chrome()
	driver.get(URL)
	r = driver.page_source
	soup = BeautifulSoup(r, 'html.parser')
	teams = soup.find_all('span', attrs={'class':'sb-team-abbrev'})
	results = soup.find_all('td', attrs={'class':'total'})
	print(len(teams))
	print(len(results))
	return


def main():
	URL = 'https://www.espn.com/nba/scoreboard'
	data = scrape(URL)
	return


if __name__ == '__main__':
	main()
