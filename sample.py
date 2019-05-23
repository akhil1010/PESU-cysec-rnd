import dnsenum
import os
#os.system('python dnsenum.py -h')
#print("Example")
#print("input(standard):\t-d domain_name -w word_list -T 10")
#print("input:\t-d domain_name -w word_list -T 10 -r -D")
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

