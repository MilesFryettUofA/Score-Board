from nbapy import game
from nbapy import scoreboard
import pandas as pd

def getbox(ID):
	'''
	Gets box score of any game
	In: Game id(int) Game id to get boxscore
	Retuns: Score 
	'''
	game_id = str(ID)  # taken from 'https://stats.nba.com/game/0021900017/'
	stats = game.BoxScore(game_id).team_stats()
	return(stats)

def getscore():
	score = scoreboard.Scoreboard(12,28,2020)
	return(score.line_score())
	


def getID():
	pass

def gameselect(scores):
	teamsplaying = scores["TEAM_ABBREVIATION"]
	print(teamsplaying)
	ID = scores["GAME_ID"]

	return(ID[0])


def main():
	scores = getscore()
	ID = gameselect(scores)
	print(scores)
	print(getbox(ID))
	# Select games to be displayed
	
main()



