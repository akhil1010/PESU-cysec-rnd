'''
*****************************************************************************************
This program implements the functionality of basic nmap scanner commands like -sS -sU -sV -sC and can grab csv records
The program can also be able to do banner grabbing and can show manual for original nmap scanner
Code written and executed By- Akhil Upadhyay PESU Cybersecurity group Head R&D dept. Head 
For any queries contact me on github- username akhil1010
*****************************************************************************************
'''
import nmap
import socket
scanner=nmap.PortScanner()
f=open("manualnmap.txt","r")

print("            ------------------------------------------               ")
print ("welcome to the nmap Scanner ")
ip_addr=input("enter the ip address ")									#taking ip_addr as input from user
print("you have entered the IP address:-> ",ip_addr)
type(ip_addr)
resp = input("""\nPlease enter the type of scan you want to run
                1)SYN ACK Scan										
                2)UDP Scan
                3)Comprehensive Scan 
		4)List Scan 
		5)Ping Scan and .csv version information
		6)banner grabbing
		press # for manual\n""")								#taking response for different types of info gathering
print("you have selected option:",resp)
if resp=='1':
	print( "NMap Version: ",scanner.nmap_version())
	scanner.scan(ip_addr,'1-1024','-v -sS ')							#SYN STEALTH Scan
	print(scanner.command_line())
	print(scanner.scaninfo())
	print("IP Status: ",scanner[ip_addr].state()) 
	print(scanner[ip_addr].all_protocols()) 
	try:
		print("Open ports",scanner[ip_addr]['tcp'].keys())
	except(Exception):
		print("No Ports open")
elif resp=='2':
	print("Wait for a moment...")									#udp scan
	print("NMap Version: ",scanner.nmap_version())
	scanner.scan(ip_addr,'1-1024','-v -sU ')
	print(scanner.command_line())
	print(scanner.scaninfo())
	print("IP Status: ",scanner[ip_addr].state()) 
	print(scanner[ip_addr].all_protocols()) 
	try:
		print ("Open ports",scanner[ip_addr]['udp'].keys())
		if scanner[ip_addr].has_tcp(22):
			print(scanner[ip_addr].tcp(22))
	except(Exception):
		print("No Ports Open")
elif resp=='3':
	print("NMap Version: ",scanner.nmap_version())							#comprehensive scan
	scanner.scan(ip_addr,'1-1024','-vv -sS -sV -sC -A -O ')
	print(scanner.command_line())
	print(scanner.scaninfo())
	print("IP Status: ",scanner[ip_addr].state()) 
	print(scanner[ip_addr].all_protocols()) 
	try:
		print ("Open ports",scanner[ip_addr]['tcp'].keys())
		if scanner[ip_addr].has_tcp(22):
			print(scanner[ip_addr].tcp(22))
	except(Exception):
		print("No Ports Open")
elif resp=='4':
	print("NMap Version: ",scanner.nmap_version())
	scanner.scan(ip_addr,'1-1024','-v -sT -A -sV ')
	print(scanner.command_line())									#list scan
	print(scanner.scaninfo())
	print("IP Status: ",scanner[ip_addr].state()) 
	print(scanner[ip_addr].all_protocols()) 
	
	try:
		print("Open ports",scanner[ip_addr]['tcp'].keys())
		if scanner[ip_addr].has_tcp(22):
			print(scanner[ip_addr].tcp(22))
	except(Exception):
		print("No Ports Open")
elif resp=='5':
	
	print("NMap Version: ",scanner.nmap_version())
	scanner.scan(ip_addr,'1-1024','-v ')
	print(scanner.command_line())									#Ping Scan and CSV form information about versions and related ports
	print(scanner.scaninfo())
	print("IP Status: ",scanner[ip_addr].state()) 
	print(scanner[ip_addr].all_protocols()) 
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")	
	print(scanner.csv())
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	
elif resp=='6':
	t_port = int(input("Enter Port: "))
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	try:
		sock.connect((ip_addr,t_port))								#banner grabbing of specific port
		sock.send((('GET HTTP/1.1 \r\n').encode('utf-8')))
		ret = sock.recv(1024)
		print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")	
		print( '[+]' + (ret).decode('utf-8'))
		print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")	
	except(Exception):
		print("Connection can't formed on the given port") 
elif resp=='#':												#press #for manual of nmap
	print(f.read())

else:
	exit(0)												#exit for any other response
'''
**************************************************************************************************************
program ends here
**************************************************************************************************************
'''
	
