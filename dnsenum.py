
'''
***************************************************************************************************************************************************************************
header files for the dnsenum.py
this program will take input from the arguments using argparse
program should be present inside dnspython folder
***************************************************************************************************************************************************************************
Code written and executed By- Akhil Upadhyay PESU Cybersecurity group Head R&D dept. Head 
For any queries contact me on github- username akhil1010
'''

from __future__ import print_function

import os
import platform															#if color class has to be implemented
import re															#for regular expression
import sys															#system library
import threading														#threading class is used to implement thread concept
import time															#to get system time 

'''
**********************************************************************************************************************************************************************
The program body starts here
**********************************************************************************************************************************************************************
'''

try:																#  attempt because Python3  renames Queue to queue
   	import Queue
except ImportError:
	import queue as Queue

try:		# Python2 & Python3 have different IP address libraries
	from ipaddress import ip_address as ipaddr
except ImportError:
	from  netaddr import IPAddress as ipaddr
																#argparse will be used in this program to take input 
try:
	import argparse
except:
	print("FATAL: Module argparse missing (python-argparse)")
	sys.exit(1)

try:
	import dns.query
	import dns.resolver
	import dns.zone														#libraries of dnspython
except:
	print("FATAL: Module dnspython missing (python-dnspython)")
	sys.exit(1)


'''in this program a Queue is defined to use the threads effectively'''


'''
thread class start here													
in this program Thread library is used for creating threads
	
'''

class scanner(threading.Thread):
	def __init__(self,queue):												#function to initialize the thread
		global wildcard
		threading.Thread.__init__(self)
		self.queue=queue

																#to get the name of the thread
	def get_name(self,domain):
		global wildcard,addresses
		
		try:
			if sys.stdout.isatty():											#to check whether it is connected to tty
				sys.stdout.write(domain+"                      \r")
				sys.stdout.flush()
			res = lookup(domain, recordtype)
			if args.tld and res:
				nameservers=sorted(list(res))
				ns0=str(nameservers[0])[:-1]									#first name of nameserver
				print(domain+"  ----  "+ns0)
			if args.tld:												#for top level domain servers
				if res:
					print(domain+"  ----  "+res)
				return
			for rdata in res:											#to print the result
				address=rdata.address
				if wildcard:											
					if address==wildcard:									#if it is wildcard
						return
				if args.domain_first:										#if domain first 
					print(domain+"  ----  "+address)
				else:
					print(address+"  ----  "+domain)							
				try:
					addresses.add(ipaddr(unicode(address)))							#to check the ipaddress
				except NameError:
					addresses.add(ipaddr(str(address)))
			if domain!=target and args.recurse:
				add_target(domain)			#recursive scan subdomains		
		except:
			pass


	def run(self):														#function to run the thread
		while True:
			try:
				domain=self.queue.get(timeout=1)
			except:
				return
			self.get_name(domain)
			self.queue.task_done()



class output:															#class for giving output message
	def status(self,message):
		print("[*]"+message)


	def good(self,message):
		print("[+]"+message)
	

	def verbose(self,message):
		print("[V]"+message)


	def warn(self,message):
		print("[-]"+message)


	def fatal(self,message):
		print("\n"+"FATAL-"+message)


def lookup(domain,recordtype):													#function for lookup of a domain related to a particular recordtype
	try:
		res=resolver.query(domain,recordtype)
		return res
	except:
		return
def get_wildcard(target):													#to check for wildcard
	epochtime=str(int(time.time()))
	res=lookup("a"+epochtime+"."+target,recordtype)
	if res:
		address=res[0].address
		out.good("Wildcard domain found-"+address)
		return address
	else:
		out.verbose("No Wildcard domain found")


def get_nameservers(target):													#function to get ns
	try:
		ns=resolver.query(target,'NS')
		return ns
	except:
		return


def get_v6(target):														#to convert in ipv6
	out.verbose("Getting ipv6 {AAAA} Records ")
	try:
		res=lookup(target,"AAAA")
		if res:
			out.good("ipv6 (AAAA) record found. Try running enumeration with the -6 option" )
		for v6 in res:
			print(str(v6)+"\n")
	except:
		return


def get_txt(target):														#to get txt records from dns
	out.verbose("Getting TXT records")
	try:
		res=lookup(target,"TXT")
		if res:
			out.good("TXT records found")
		for txt in res:
			print(txt)
		print()
	except:
		return
def get_mx(target):														#to get mx record
	out.verbose("Getting MX records")
	try:
		res=lookup(target,"MX")
	except:
		return
	if not res:
		return
	
	out.good("MX records found, added to target list")
	for mx in res:
		print(mx.to_text())
		mxsub=re.search("([a-z0-9\.\-]+)\."+target,mx.to_text(),re.IGNORECASE)
	
		try:
			if mxsub.group(1) and mxsub.group(1) not in wordlist:
				queue.put(mxsub.group(1) + "." + target)
		except AttributeError:
			pass
	print()
def zone_transfer(domain,ns):													#to request for zone transfer
	out.verbose("Trying zone transfer against "+ str(ns))
	try:
		zone=dns.zone.from_xfr(dns.query.xfr(str(ns),domain,relativize=False),relativize=False)
		out.good("Zone Transfer successful using nameserver "+str(ns))
		names=list(zone.nodes,keys())
		names.sort()
		for n in names:
			print(zone[n].to_text(n))
		sys.exit(0)
	except Exception:
		pass


def add_tlds(domain):
	for tld in wordlist:
		queue.put(domain+"."+tld)


def add_target(domain):														#to add target 
	for word in wordlist:
		queue.put(word+"."+domain)

'''*******************************************************************************************************************************************************
to get to know about the argparse in python 
visit this link->  https://docs.python.org/3/howto/argparse.html

**********************************************************************************************************************************************************
'''
def get_args():															#taking the inputs in one line
	global args
	parser = argparse.ArgumentParser('dnsenum.py', formatter_class=lambda prog:argparse.HelpFormatter(prog,max_help_position=40))
	target = parser.add_mutually_exclusive_group(required=True)
	target.add_argument('-d', '--domain', help='Target domain', dest='domain', required=False)
	target.add_argument('-l', '--list', help='File containing list of target domains', dest='domain_list', required=False)
	parser.add_argument('-w', '--wordlist', help='Wordlist', dest='wordlist', required=False)
	parser.add_argument('-t', '--threads', help='Number of threads', dest='threads', required=False, type=int, default=8)
	parser.add_argument('-6', '--ipv6', help='Scan for AAAA records', action="store_true", dest='ipv6', required=False, default=False)
	parser.add_argument('-z', '--zonetransfer', action="store_true", default=False, help='Only perform zone transfers', dest='zonetransfer', required=False)
	parser.add_argument('-r', '--recursive', action="store_true", default=False, help="Recursively scan subdomains", dest='recurse', required=False)
	parser.add_argument('-R', '--resolver', help="Use the specified resolver instead of the system default", dest='resolver', required=False)
	parser.add_argument('-T', '--tld', action="store_true", default=False, help="Scan for TLDs", dest='tld', required=False)
	parser.add_argument('-D', '--domain-first', action="store_true", default=False, help='Output domain first, rather than IP address', dest='domain_first', required=False)
	parser.add_argument('-v', '--verbose', action="store_true", default=False, help='Verbose mode', dest='verbose', required=False)
	args = parser.parse_args()


def setup():														#function for making setup of different inputs given as arguments to the program
	global targets,wordlist,queue,resolver,recordtype
	if args.domain:
		targets=[args.domain]
	if args.tld and not args.wordlist:
		args.wordlist=os.path.join(os.path.dirname(os.path.realpath(__file__)), "tlds.txt")
	else:
		if not args.wordlist:
			args.wordlist=os.path.join(os.path.dirname(os.path.realpath(__file__)),"subdomains.txt")
	try:
		wordlist=open(args.wordlist).read().splitlines()
	except:
		out.fatal("could not open wordlist "+args.wordlist)
		sys.exit(1)
	

	if args.threads<1:												#threads can only range between 1 to 32
		args.threads=1
	elif args.threads>32:
		args.threads=32
	queue=Queue.Queue()
	resolver=dns.resolver.Resolver()
	resolver.timeout=1
	resolver.lifetime=1
	if args.resolver:
		resolver.nameservers=[args.resolver]
															#record type setup AAAA for v6, A for v4, MX for mail exchanger, NS for name servers	
	if args.ipv6:
		recordtype='AAAA'
	elif args.tld:
		recordtype='NS'
	else:
		recordtype='A'

'''********************************************************************************************************************************************************************
main starts here
***********************************************************************************************************************************************************************'''
if __name__=="__main__":
	global wildcard, addresses, outfile_ips
	addresses=set([])
	out=output()													#constructor for output
	get_args()													#for getting the inputs from arguments
	setup()														#for setting up the input
	try:
		resolver.query('.','NS')										#first of all try to get ns records
	
	except dns.exception.Timeout:
		out.fatal("No valid DNS resolver. Set a custom resolver with -R <resolver> \n")
		sys.exit(1)
	except:
		pass
	if args.domain_list:
		out.verbose("Domain list provided parse {} for domains.".format(args.domain_list))
		if not os.path.isfile(args.domain_list):
			out.fatal("Domain List doesnt exist!".format(args.domain_list))
			sys.exit(1)
		with open(args.domain_list,'r') as domain_list:
			try:
				targets=list(filter(bool,domain_list.read().split('\n')))
			except Exception as e:
				out.fatal("couldnt read {},{}".format(args.domain_list,e))
				sys.exit(1)
	for subtarget in targets:											#to get all taargts
		global target
		target=subtarget
		out.status("Processing domain {} ".format(target))
		if args.resolver:
			out.status("using specified resolver{}".format(args.resolver))
		else:
			out.status("using system resolvers {} ".format(resolver.nameservers))
		if args.tld:
			if "." in target:
				out.warn("Warning!!! TLD scanning works best with just the domain root")
			out.good("TLD scan")
			add_tlds(target)
		else:
			queue.put(target)
			nameservers=get_nameservers(target)
			out.good("Getting nameservers")
			targetns=[]
			try:
				for ns in nameservers:
					ns=str(ns)[:-1]
					res=lookup(ns,"A")
					for rdata in res:
						targetns.append(rdata.address)
						print("rdata.address"+" - "+ns)
					zone_transfer(target,ns)
			except SystemExit:
				sys.exit(0)
			except:
				out.warn("Getting nameservers failed")


			out.warn("Zone transfer failed")
			if args.zonetransfer:
				sys.exit(0)
			get_v6(target)
			get_txt(target)
			get_mx(target)
			wildcard=get_wildcard(target)
			if wildcard:
				try:
					addresses.add(ipaddr(unicode(wildcard)))
				except NameError:
					addresses.add(ipaddr(str(wildcard)))
			out.status("Scanning "+target+" for "+recordtype+" records ")
			add_target(target)
		for i in range(args.threads):
			t=scanner(queue)
			t.setDaemon(True)
			t.start()
		try:
			for i in range(args.threads):
				t.join(1024)
		except KeyboardInterrupt:
			out.fatal("Caught KeyboardInterrupt, quitting....")
			sys.exit(1)
		print("                            ")
'''
*********************************************************************************************************************************
End of the program here
*********************************************************************************************************************************
'''
