from HTMLParser import HTMLParser
from urllib import unquote
import requests


class Parser(HTMLParser):
	def __init__(self,user=None,passwd=None,url=None,logger=None):
		HTMLParser.__init__(self)

		self.logger = logger
		self.user = user
		self.passwd = passwd
		self.url = [url]

		self.urls = []

		if self.user and self.passwd and self.url:
			self.request()

	def request(self):
		_url = self.getUrl()
		self.logger.debug(_url)
		self.urls = []

		self.r = requests.get(_url, auth=(self.user, self.passwd))
		self.feed(self.r.text)

	def clean_urls(self):
		self.urls = []
	
	def getUrl(self):
		if len(self.url) > 1:
			dirs = '/'.join(self.url)
			_url = 'http://%s/' % (dirs)
		else:
			_url = 'http://%s' % self.url[0]
		return _url

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					self.urls.append(attr[1])

	def getPlayerUrl(self,_file):
		url = '/'.join(self.url)
		return ('http://%s:%s@%s/%s' % (self.user,self.passwd,url,_file))

	def goUpper(self):
		if len(self.url) > 1:
			self.url.pop()
			self.request()
			return self.urls

	def goToDir(self,dir):
		self.url.append(dir)
		try:
			self.request()
			return self.urls
		except Exception as err:
			self.logger.warning(err)
			self.url.pop()
			return self.urls

	def get(self):
		return self.urls