"""Support for discovering Wordpress plugins."""
from os.path import exists, join, realpath
from json import loads
from re import I, findall, search
from lib1.request import *

def decode(string):
	return string.encode('utf-8')


class wpplugins(Request):
	def __init__(self, url, data, kwargs):
		self.url = url
		self.data = data
		self.kwargs = kwargs
		self.files = {}

		files = {
    "changelogs": [
        "changelog.txt", "changelog.md", "CHANGELOG.txt", "changelog",
        "CHANGELOG.md", "ChangeLog.txt", "ChangeLog.md", "CHANGELOG"
    ],
    "fpd": [
        "404.php", "archive.php", "author.php", "comments.php",
        "footer.php", "functions.php", "header.php", "image.php",
        "page.php", "search.php", "single.php", "archive.php"
    ],
    "license": [
        "license.txt", "license.md", "LICENSE.md", "LICENSE.txt",
        "LICENSE"
    ],
    "dirs": [
        "js", "css", "images", "inc", "admin", "src", "widgets", "lib",
        "assets", "includes", "logs", "vendor", "core"
    ],
    "readme": [
        "readme.txt", "readme.md", "README.md", "README.txt", "README",
        "readme"
    ]
}

		
		Request.__init__(self, kwargs)

	def changelog(self, plugin):
		if self.kwargs['verbose'] is True:
			print('Checking plugins changelog...')
		for file in self.files.get('changelogs', []):
			url = Path(self.url, '/wp-content/plugins/%s/%s' % (plugin, file))
			resp = self.send(url=url, method="GET")
			if resp.status_code == 200 and resp.content != ("" or None):
				if resp.url == url:
					print('Changelog: %s' % (resp.url))
					break

	def fpd(self, plugin):
		if self.kwargs['verbose'] is True:
			print('Checking plugins full path disclosure...')

		for file in self.files.get('fpd', []):
			url = Path(self.url, '/wp-content/plugins/%s/%s' % (plugin, file))
			resp = self.send(url=url, method="GET")
			if resp.status_code == 200 and resp.content != ("" or None):
				if resp.url == url:
					if search(decode('<b>Fatal error</b>:'), resp.content, I):
						path_d = findall(decode('<b>(/\S*)</b>'), resp.content)[0]
						print('FPD (Full Path Disclosure): %s' % (path_d.decode('utf-8')))
						break

	def license(self, plugin):
		if self.kwargs['verbose'] is True:
			print('Checking plugins license...')

		for file in self.files.get('license', []):
			url = Path(self.url, '/wp-content/plugins/%s/%s' % (plugin, file))
			resp = self.send(url=url, method="GET")
			if resp.status_code == 200 and resp.content != ("" or None):
				if resp.url == url:
					print('License: %s' % (resp.url))
					break

	def listing(self, plugin):
		if self.kwargs['verbose'] is True:
			print('Checking plugins directory listing...')

		for dir_ in self.files.get('dirs', []):
			url = Path(self.url, '/wp-content/plugins/%s/%s' % (plugin, dir_))
			resp = self.send(url=url, method="GET")
			if resp.status_code == 200 and resp.content != ("" or None):
				if search(decode('<title>Index of'), resp.content, I):
					print('Listing: %s' % (resp.url))

	def readme(self, plugin):
		if self.kwargs['verbose'] is True:
			print('Checking plugins readme...')

		for file in self.files.get('readme', []):
			url = Path(self.url, '/wp-content/plugins/%s/%s' % (plugin, file))
			resp = self.send(url=url, method="GET")
			if resp.status_code == 200 and resp.content != ("" or None):
				if resp.url == url:
					print('Readme: %s' % (resp.url))
					break

	def run(self):
		print('Passive enumeration plugins...')
		plugins = self.s_plugins()
		if plugins != []:
			for plugin in plugins:
				print('Name: %s' % (plugin.decode('utf-8')))
				self.changelog(plugin)
				self.fpd(plugin)
				self.license(plugin)
				self.readme(plugin)
				self.listing(plugin)
				self.dbwpscan(plugin)
		else:
			printwar('Not found plugins with passive enumeration')

	def s_plugins(self):
		plugin = []
		resp = self.send(url=self.url, method="GET")
		plugins = findall(decode('/wp-content/plugins/(.+?)/'), resp.content)
		for pl in plugins:
			if pl not in plugin:
				plugin.append(pl)
		return plugin

	def dbwpscan(self, plugin):
		if self.kwargs['verbose'] is True:
			print('Checking plugin vulnerabilities...')
		plugin = plugin.decode('utf-8')
		url = "https://www.wpvulndb.com/api/v2/plugins/%s"%(plugin)
		resp = self.send(url=url,method="GET")
		if resp.headers['Content-Type'] == 'application/json; charset=utf-8':
			json = loads(resp.content)
			if json.get(plugin,False):
				if json[plugin]['vulnerabilities']:
					for x in range(len(json[plugin]['vulnerabilities'])):
						print('Title: %s'%(json[plugin]['vulnerabilities'][x]['title']))
						if json[plugin]['vulnerabilities'][x]['references'] != {}:
							if json[plugin]['vulnerabilities'][x]['references']['url']:
								for y in range(len(json[plugin]['vulnerabilities'][x]['references']['url'])):
									print('Reference: %s'%(json[plugin]['vulnerabilities'][x]['references']['url'][y]))
						print('Fixed in: %s'%(json[plugin]['vulnerabilities'][x]['fixed_in']))
				else: print('Not found vulnerabilities')
			else: print('Not found vulnerabilities')
		else: print('Not found vulnerabilities')
		print('')
