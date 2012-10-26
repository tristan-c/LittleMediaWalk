import curses
from urllib import unquote

class Screen():
	def __init__(self):
		#init screen
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.screen.keypad(1)

		#get y/x
		self.height,self.width = self.screen.getmaxyx()
		self.height = self.height - 2

		#screen manipulation var
		self.whole_screen = None
		self.current_screen = None
		self.screen_interval = None
		self.cursor = 0

	def refresh(self):
		self.screen.refresh()

	def setNewScreen(self,_array):
		self.whole_screen = _array
		if len(_array) <= self.height:
			self.current_screen = _array
			self.screen_interval = (0,len(_array))
			self.drawScreen()
		else:
			self.current_screen = _array[0:self.height]
			self.screen_interval = (0,self.height)
			self.drawScreen()
	
	def drawScreen(self):
		self.screen.clear()
		self.screen.border(0)
		for i,line in enumerate(self.current_screen):
			if i == self.cursor:
				self.screen.addstr(i+1, 2,' %s' % unquote(self.current_screen[i]),curses.A_REVERSE)
			else:
				self.screen.addstr(i+1, 2,' %s' % unquote(self.current_screen[i]))
		self.refresh()

	def moveCursorUp(self):
		if self.cursor == 0:
			if self.screen_interval[0] != 0:
				self.screen_interval = (self.screen_interval[0] - 1, self.screen_interval[1] - 1)
				self.current_screen = self.whole_screen[self.screen_interval[0]:self.screen_interval[1]]	
				self.drawScreen()
				highlightLine(screen,cursor,screen_array)

		else:
			self.cursor = self.cursor -1
			self.drawScreen()

	def moveCursorDown(self):
		if self.cursor == self.height -1:
			if self.screen_interval[1] < len(self.whole_screen):
				self.screen_interval = (self.screen_interval[0] + 1, self.screen_interval[1] + 1)
				self.current_screen = self.whole_screen[self.screen_interval[0]:self.screen_interval[1]]	
				self.drawScreen()

		elif self.cursor != len(self.whole_screen) - 1:
			self.cursor = self.cursor + 1
			self.drawScreen()

	def getCurrentFilename(self):
		return self.whole_screen[self.screen_interval[0] + self.cursor]

	def __del__(self):
		curses.nocbreak()
		curses.echo()
		curses.endwin()

		self.screen.keypad(0)