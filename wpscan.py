import modules.discovery.plugins as plug
import modules.discovery.generic as generic
import modules.discovery.themes as themes
import modules.discovery.users.wpusers as users
import modules.fingerprint.fingerprint as fingerprint
import modules.fingerprint.cms as cms
import modules.fingerprint.waf as waf
import modules.fingerprint.headers as header
import modules.fingerprint.server as server
import lib.ragent as rand_agent
import lib.check as gen_check
import lib.request as request

kwargs = {
			 'agent':rand_agent.ragent(),'ragent':False,'redirect':True,
			  'cookie':None,'proxy':None,'timeout':None,'verbose':True,'headers':{}
         }

url = input("Enter a url to scan for:")

#For properly formatting the url
url = gen_check.urlCheck(url)

#Preparing a request object, that manages the request to the website
req_obj = request.Request(kwargs)
req = req_obj.send(url)

# To check for wordpress site
_cms_ = cms.cms(req.headers,req.content)
if 'wordpress' not in _cms_:
    exit(print("That site not running WordPress"))

print("The target site is running Wordpress CMS")
#Performing a user enumeration on the website 
print("Performing a full verbose check on the targeted url: ",url)
print("Enumerating all the users in the wordpress server:")
users.wpusers(url,None,kwargs).run()
