"""Support for discovering Wordpress listings."""
from os.path import realpath
from re import I, search

from lib1.readfile import *
from lib1.request import *


def decode(string):
	return string.encode('utf-8')

class wplisting(Request):
	def __init__(self,url,data,kwargs):
		self.url = url 
		self.data = data
		self.kwargs = kwargs
		Request.__init__(self,kwargs)

	def run(self):
		if self.kwargs['verbose'] is True:
			print("Checking directory listing...")
		common_files = ['/wp-admin/','/wp-admin/css','/wp-admin/images','/wp-admin/includes','/wp-admin/js','/wp-admin/network','/wp-admin/user','/wp-content/','/wp-content/uploads'
				,'/wp-content/plugins','/wp-content/themes','/wp-includes/','/wp-includes/js','/wp-includes/Text','/wp-includes/css','/wp-includes/images','/wp-includes/pomo','/wp-includes/theme-compat']
		for dir_ in common_files:
			url = Path(self.url,dir_)
			resp = self.send(url=url,method="GET")
			if search(decode('<title>Index of /'),resp.content,I):
				print("Dir \"%s\" listing enable at: %s"%(dir_,resp.url))
