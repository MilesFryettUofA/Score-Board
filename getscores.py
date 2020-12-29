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
	stats = game.BoxScore(game_id).players_stats()
	return(stats)

def getscore():
	score = scoreboard.Scoreboard(12,28,2020)
	return(score.line_score())
	


def getID():
	pass

ID= '0022000041'

print(getbox(ID))
print(getscore)