#!/usr/bin/python3

##################################################
#          Code written by - be1iev3r            #
##################################################

# Import Required Modules
import argparse
import requests
import threading
from colorama import init, Fore, Back, Style
init(autoreset=True)

# Argument Parser
example_text = "example: python3 admin-bust3r.py -u http://example.com -f -e php -o <outfile>"

parser = argparse.ArgumentParser(description=" A powerful,fast and advanced admin panel buster tool in python. ", epilog = example_text)
parser.add_argument("-u", "--url", help=" Target URL to check for admin panel. ", dest="target")
parser.add_argument("-e", "--ext", help=" To check against specific extension only. EX:- (php , asp, html, aspx) ", dest="ext")
parser.add_argument("-s", "--small", help=" To check against small wordlist (default = medium). ", action="store_true", default=False, dest="small")
parser.add_argument("-l", "--large", help=" To check against large wordlist (default = medium). ", action="store_true", default=False, dest="large")
parser.add_argument("-vl", "--verylarge", help=" To check against very large wordlist (default = medium). ", action="store_true", default=False, dest="verylarge")
parser.add_argument("-f", "--fast", help=" For Faster Scaning. ", action="store_true", default=False, dest="fast")
parser.add_argument("-o", "--output", help=" To save output in a file. ", dest="outfile")

args = parser.parse_args()

# Print the Banner
banner = '''
     ___       _______  .___  ___.  __  .__   __.        .______    __    __       _______.___________.____   .______      
    /   \     |       \ |   \/   | |  | |  \ |  |        |   _  \  |  |  |  |     /       |           |___ \  |   _  \     
   /  ^  \    |  .--.  ||  \  /  | |  | |   \|  |  ______|  |_)  | |  |  |  |    |   (----`---|  |----` __) | |  |_)  |    
  /  /_\  \   |  |  |  ||  |\/|  | |  | |  . `  | |______|   _  <  |  |  |  |     \   \       |  |     |__ <  |      /     
 /  _____  \  |  '--'  ||  |  |  | |  | |  |\   |        |  |_)  | |  `--'  | .----)   |      |  |     ___) | |  |\  \----.
/__/     \__\ |_______/ |__|  |__| |__| |__| \__|        |______/   \______/  |_______/       |__|    |____/  | _| `._____| 
'''
print(Fore.YELLOW + Style.BRIGHT + banner)
print(Fore.BLUE + Style.BRIGHT + "\t\t\t\t\t\t\t v-1.0 Made by:-" + Fore.GREEN + Style.BRIGHT + " @be1iev3r \n")

# Disclosure
print(Fore.GREEN + "\t\t\t\t A powerful,fast and advanced admin panel buster tool in python.\n ")
print(Fore.YELLOW + "[!] Author is not responsible or involved in any kind of your activity. Use of this tool in illegal activity is full on user's responsibilty. Happy Hacking!! \n") 

# Check if the target host is reachable
target = args.target

if target[-1] == "/":
    target = target[:-1]
try:
    req = requests.get(target)
except:
    print(Back.RED + "[-] Target host not reachable.")
    print(Fore.YELLOW + "[!] EXITING NOW...")
    quit()

# Check for robots.txt
try:
    print(Fore.BLUE + "[*] Searching for 'robots.txt'...")
    req = requests.get(target + '/robots.txt', timeout=10)
    if req.status_code == 200:
        print(Fore.GREEN + "[+] 'robots.txt' found. Contents of 'robots.txt' are :")
        print("-"*50)
        print(req.text)
        print("-"*50)
    else:
        print(Fore.RED + "[-] 'robots.txt' not found.")
except requests.exceptions.HTTPError:
    print(Back.RED + "[-] HTTP error occurred: ")
except requests.exceptions.Timeout:
    print(Back.RED + "[-] The request for 'robots.txt' timeout.")

# FileName declaration
filename = "ab_medium.txt"
small = args.small
large = args.large
verylarge = args.verylarge

if small:
    filename = "ab_small.txt"
elif large:
    filename = "ab_large.txt"
elif verylarge:
    filename = "ab_verylarge.txt"
else:
    filename = "ab_medium.txt"

# Check for extension supplied
urls_list = []
ext = args.ext
if ext:
    ext_list =['php','asp','html','aspx']
    if ext not in ext_list:
        print(Back.RED + "[-] Invalid extension.")
        print(Fore.YELLOW + "[!] EXITING NOW...")
        quit()
    else:
        new_ext_list = [item for item in ext_list if item!=ext]
    try:
        with open(filename) as paths:
            for path in paths:
                for e in new_ext_list:
                    if e in path:
                        break
                else:
                    urls_list.append(path)
    except IOError:
        print(Back.RED + "[-] Error opening wordlist file. Please check if it is downloaded while git cloning.")
        print(Fore.YELLOW + "[!] EXITING NOW...")
        quit()
else:
    try:
        with open(filename) as paths:
            for path in paths:    
                urls_list.append(path)
    except IOError:
        print(Back.RED + "[-] Error opening wordlist file. Please check if it is downloaded while git cloning.")
        print(Fore.YELLOW + "[!] EXITING NOW...")
        quit()

# Scanning for Target
output = []
def scanner(urls_list):
    for item in urls_list:
        item = item.strip()
        url = target + item
        try:
            req = requests.get(url,timeout=(5,5)).status_code
            if req == 200:
                print(Fore.GREEN + "[+] Admin Panel found: ", url)
                output.append(url)
            elif req == 302:
                print(Back.GREEN + Style.BRIGHT + "[+] Redirection on url: ", url)
                output.append(url)
            else:
                print(Fore.RED + "[-] ",url)
        except:
            print(Fore.RED + "[-] Timeout, skipping: ", url)

# Fast Scanning
fast = args.fast
if fast:
    print(Fore.BLUE + "[*] Fast Mode ON...")
    p = len(urls_list)//5
    division1 = urls_list[:p]
    division2 = urls_list[p:2*p]
    division3 = urls_list[2*p:3*p]
    division4 = urls_list[3*p:4*p]
    division5 = urls_list[4*p:]

    def part1():
        scanner(division1)

    def part2():
        scanner(division2)

    def part3():
        scanner(division3)

    def part4():
        scanner(division4)

    def part5():
        scanner(division5)

    thread1 = threading.Thread(target = part1)
    thread2 = threading.Thread(target = part2)
    thread3 = threading.Thread(target = part3)
    thread4 = threading.Thread(target = part4)
    thread5 = threading.Thread(target = part5)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

else:
    print(Fore.BLUE + "[*] Normal Mode ON...")
    p = len(urls_list)//2
    division1 = urls_list[:p]
    division2 = urls_list[p:]

    def part1():
        scanner(division1)

    def part2():
        scanner(division2)

    thread1 = threading.Thread(target = part1)
    thread2 = threading.Thread(target = part2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

# Output File
outfile = args.outfile
if outfile:
    try:
        f = open(outfile, "w")
        for item in output:
            f.write(item + "\n")
    except IOError:
        print(Back.RED + "[-] Error while writing in output file. ")
