"""Support for fingerprint Wordpress."""
from lib1.request import *
from modules1.fingerprint.cms import *
from modules1.fingerprint.headers import *
from modules1.fingerprint.server import *
from modules1.fingerprint.waf import *


class fingerprint(Request):
	def __init__(self,url,data,kwargs):
		self.url = url
		self.data = data
		Request.__init__(self,kwargs)

	def run(self):
		req = self.send(url=self.url)
		_cms_ = cms(req.headers,req.content)
		if 'wordpress' not in _cms_:exit(print('That site not running WordPress'))
		_server_ = server(req.headers)
		if _server_:print('Server: %s'%_server_)
		_waf_ = waf(req.content)
		for w in _waf_:
			if w != None: print('WAF: %s'%w)
		headers(req.headers)
