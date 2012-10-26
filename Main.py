import curses
import requests
import subprocess
import logging
import ConfigParser

import Parser
import Screen

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('app')

config = ConfigParser.ConfigParser()
config.read('defaults.cfg')

user = config.get('config','user')
passwd = config.get('config','passwd')
srv = config.get('config','srv')
player = config.get('config','player')

parser = Parser.Parser(user,passwd,srv,logger)
screen = Screen.Screen()

try:
	screen.setNewScreen(parser.urls)
except Exception as err:
	logger.error(err)

while True:
	char = screen.screen.getch()
	if char == 113: 
		break
	elif char == curses.KEY_UP:
		screen.moveCursorUp()
	elif char == curses.KEY_DOWN:
		screen.moveCursorDown()
	elif char == 10:
		filename = screen.getCurrentFilename()
		if filename == '../':
			_url = parser.goUpper()
			if _url:
				screen.setNewScreen(_url)
		else:
			if filename[len(filename) - 1] == '/':
				screen.setNewScreen(parser.goToDir(filename.strip('/')))
			else:
				playerUrl = parser.getPlayerUrl(filename)
				logger.debug(playerUrl)
				try:
					thread = subprocess.Popen([player,playerUrl],stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
				except Exception as err:
					logger.error(err)

