import os
import pyfiglet 
import subprocess as sp
import n_map
import sql
import crips
import dnsenum
import wpscan
import myweeman
import hashcat.hashcat as hashcat
import denos
def page2():
		os.system('clear')
		result = pyfiglet.figlet_format("MENU")
		print(result) 
		print("			Information Gathering Part............1\n")
		print("			Password Attack.......................2\n")
		print("			Web Exploit...........................3\n")
		print("			Social Engineering....................4\n")
		print("			exit..................................0\n")
		ch=int(input())
		if ch==1:
			page2_1()
		elif ch==2:
			page2_2()
		elif ch==3:
			page2_3()
		elif ch==4:
			page2_4()
		elif ch==0:
			exit(0)
		else:
			page1()

def page2_1():
	os.system('clear')
	result = pyfiglet.figlet_format("INFO GATHERING")
	print(result)
	#print("Hello user this is Information Gathering Page")
	print("			n_map................1\n")
	print("			sql injection........2\n")
	print("			wordpress scan.......3\n")
	print("			crips................4\n")
	print("			dnsenum..............5\n")
	print("			Back.................99\n")
	print("			Exit.................0\n")
	ch=int(input())
	if ch==1:
		page2_1_1()
	elif ch==2:
		page2_1_2()
	elif ch==3:
		page2_1_3()
	elif ch==4:
		page2_1_4()
	elif ch==5:
		page2_1_5()
	elif ch==0:
		exit(0)
	else:
		page2()
def page2_1_1():
	os.system('clear')
	result = pyfiglet.figlet_format("NMAP")
	print(result)
	n_map.scan()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_1()
	else:
		exit(0)	
def page2_1_2():
	os.system('clear')
	result = pyfiglet.figlet_format("SQL INJECTION")
	print(result)
	sql.sql()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_1()
	else:
		exit(0)	

	
def page2_1_3():
	os.system('clear')
	result = pyfiglet.figlet_format("WP SCAN")
	print(result)
	wpscan.scan()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_1()
	else:
		exit(0)	

def page2_1_4():
	os.system('clear')
	result = pyfiglet.figlet_format("CRIPS")
	print(result)
	crips.select()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_1()
	else:
		exit(0)	
def page2_1_5():
	os.system('clear')
	result = pyfiglet.figlet_format("DNSENUM")
	print(result)
	print("Enter the Domain name:\t")
	db = input()
	print("Specify the word list length")
	print("{0}:Default\n{1}:100\n{2}:500\n{3}:1000\n{4}:10000")
	dic={0:"subdomains.txt",1:"subdomains-100.txt",2:"subdomains-500.txt",3:"subdomains-1000.txt",4:"subdomains-10000.txt"}
	ch = int(input())
	inp=" -d "+db+" -w "+dic[ch]
	print("Enter the number of threads{Default=8}")
	t=int(input()) or 8
	inp+= (" -t "+str(t))
	print(inp)
	inp="python dnsenum.py "+inp
	os.system(inp)
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_1()
	else:
		exit(0)	

def page2_2():
	os.system('clear')
	result = pyfiglet.figlet_format("PASSWORD ATTACK")
	print(result)
	print("			HashCat..............1")
	print("			exit.........................0")
	print("			Back........................99")
	ch=int(input())
	if ch==1:
		hashcat.main()
	elif ch==99:
		page2()
	else:
		exit(0)
def page2_2_1():
	result = pyfiglet.figlet_format("JTR")
	print(result)
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_2()
	else:
		exit(0)

def page2_3():
	os.system('clear')	
	result = pyfiglet.figlet_format("WEB EXPLOITATION")
	print(result)
	print("			Admin Buster.................1")
	print("			Denial Of Service............2")
	print("			SQL Injection................3")
	print("			MYWEEMAN.....................4")
	print("			Exit.........................0")
	print("			Back.........................99")
	ch=int(input())
	if ch==1:
		page2_3_1()
	elif ch==2:
		page2_3_2()
	elif ch==3:
		page2_3_3()
	elif ch==4:
		page2_3_4()
	elif ch==0:
		exit(0)
	else:
		page2()
def page2_3_1():
	print("Hello this is AdminBuster")
	#page2_3()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_3()
	else:
		exit(0)
def page2_3_2():
	os.system('clear')
	result = pyfiglet.figlet_format("DENIAL OF SERVICE")
	print(result)
	denos.main()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_3()
	else:
		exit(0)
def page2_3_3():
	os.system('clear')
	result = pyfiglet.figlet_format("SQL INJECTION")
	print(result)
	sql.sql()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_3()
	else:
		exit(0)
def page2_3_4():
	os.system('clear')
	result = pyfiglet.figlet_format("MYWEEMAN")
	print(result)
	myweeman.main()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_3()
	else:
		exit(0)	

def page2_4():
	os.system('clear')
	result = pyfiglet.figlet_format("Social Engineering")
	print(result)
	page2()
	ch = int(input("{1}:Go-Back\n{0}:Exit\n"))
	if ch==1:
		page2_3()
	else:
		exit(0)



def page1():

	ch=0
	print("Enter the choice")
	print(" 1 for continue ")
	print("0 for exit")
	ch=int(input())
	if ch==1:
		page2()
	else:
		exit(0)



																				#sp.call('clear',shell=True)
os.system('clear')
result = pyfiglet.figlet_format("WELCOME") 
print(result) 
result=pyfiglet.figlet_format("PESU-RND PENTESTING FRAMEWORK")
print(result)

page1()

