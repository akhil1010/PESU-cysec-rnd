#!usr/bin/env python3
from dns import reversename,resolver
import requests
import dns.zone
import dns.ipv4
menu = '''\033[0m
    {1}--Whois lookup
    {2}--Traceroute
    {3}--Reverse DNS Lookup
    {4}--NS lookup
     '''
print(menu)    

def select():
    print(menu)
    try:
        choice= int(input("Enter the option"));
        if choice==1:
            d3=input("Enter the IP or Domain:\n")
            url="http://api.hackertarget.com/whois/?q=" + d3
            r=requests.get(url)
            print(r.text)
        elif choice==2:
            d3=input("Enter the IP or Domain")
            url="https://api.hackertarget.com/mtr/?q=" + d3
            r=requests.get(url)
            print(r.text)
        elif choice==3:
            d3=input("Enter the ip")

           # reversed_dns=socket.gethostbyaddr(d3)
            rev_name = reversename.from_address(d3)
            reversed_dns = str(resolver.query(rev_name,"PTR")[0])
            print(reversed_dns)
        else:
            #It return the Mx record type in the directory
            d3=input("Enter the domain for nslookup")
            answers=dns.resolver.query(d3,'MX')
            for rdata in answers:
                print('Host',rdata.exchange,'has preference',rdata.preference)
    except(KeyboardInterrupt):
            print("Keyboard Interrupt")


