#import modules.discovery.plugins as plug
#import modules.discovery.generic as generic
#import modules.discovery.themes as themes
import modules1.discovery.users.wpusers as users
import modules1.fingerprint.fingerprint as fingerprint
import modules1.fingerprint.cms as cms
import modules1.fingerprint.waf as waf
import modules1.fingerprint.headers as header
import modules1.fingerprint.server as server
import modules1.discovery.generic.wpversion as wpver
import lib1.ragent as rand_agent
import lib1.check as gen_check
import lib1.request as request

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

# To Obtain information about the server
print("\nThe Server Information:")
_server_ = server.server(req.headers)
if _server_:
    print("Server: %s"%(_server_))

#To find any wordpress security system is enables(famous one)
print("\nAny security system at the target website:")
_waf_ = waf.waf(req.content)
for w in _waf_:
    if w != None:
        print("WAF:%s"%(w))
# To figure out if there is any uncommon headers
header.headers(req.headers)


print("\nThe target site is running Wordpress CMS")

#Performing a user enumeration on the website 
print("\nPerforming a full verbose check on the targeted url: ",url)
print("\nEnumerating all the users in the wordpress server:")
users.wpusers(url,None,kwargs).run()

#Performing a version check:
wpver.wpversion(url,None,kwargs).run()
