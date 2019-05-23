import os
import re

def main():
	print("This system makes use of hashcat as it's password attack tool!!")
	print("\nMake sure that all your targeted password hashes are in hash.txt......")

	os.system("hashcat -a 0 -m 1700 hash.txt rockyou.splitaa rockyou.splitab rockyou.splitac rockyou.splitad rockyou.splitae rockyou.splitaf rockyou.splitag -r rule64.txt -o cracked.txt")


	print("\nThe Cracked Passwords are:\n\n")
	with open("hashcat/hash.txt") as file1:
		with open("hashcat/cracked.txt") as file2:	
			for line1 in file1:
				for line2 in file2:
					op = re.search(line1.rstrip(),line2.rstrip(),re.IGNORECASE)     
					if(op!=None):
						print(line2)

