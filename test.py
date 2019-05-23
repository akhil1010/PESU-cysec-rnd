import n_map
import sql
import os
import crips
import dnsenum
import wpscan
os.system('clear')
print("Enter your option")
print("{1}:N-map\n{2}:SQL Injection\n{3}:Crips\n{4}:Dns Enumeration\n{5}:WP Scan\n{99}:Main menu")
ch = int(input("\n"))
if ch==1:
	n_map.scan()
elif ch==2:
	sql.sql()
elif ch==3:
	crips.select()
elif ch==4:
	dnsenum.scan()
elif ch==5:
	wpscan.scan()
else:
	exit(0)
