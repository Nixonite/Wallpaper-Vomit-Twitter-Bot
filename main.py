from HTMLParser import HTMLParser
import urllib2
import sys,os
import re
import sqlite3

def sqlStart():
	return sqlite3.connect('wallpapers.db')
	
def sqlConnection(sqlconn):
	return sqlconn.cursor()

def sqlClose(conn):
	conn.close()

board = "wg"

badImagesList = ["1334280578782.jpg"]#filename for the sticky image at top of /wg/

conn = sqlStart()
c = sqlConnection(conn)
c.execute("create table if not exists Wallpapers (ID INTEGER PRIMARY KEY, FILENAME text)")
conn.commit()

directory = os.getcwd()+'/'+board
os.chdir("/")
if not os.path.exists(directory):
    os.makedirs(directory)

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
		if(tag == "a"):
			if((".jpg" or ".png" or ".gif") in (dict(attrs)["href"])):
				if "class" not in dict(attrs):
					global counter
					fullURL = "http:"+(dict(attrs)["href"])
					response = urllib2.urlopen(fullURL)
					reverseURL = fullURL[::-1]
					filename = reverseURL[:reverseURL.find('/')][::-1]
					if filename not in badImagesList:#sticky image name					
						c.execute("select 1 from Wallpapers where FILENAME=:filen",{"filen":filename})
						conn.commit()
						if c.fetchone() is None:
							output = open(directory+"/"+filename,"wb")
							output.write(response.read())
							output.close()
							if os.path.getsize(directory+"/"+filename)/1024.0/1024.0 < 3.0 and os.path.getsize(directory+"/"+filename)/1024.0/1024.0 > 0: #if image is less than 3MB, and not corrupted (twitter rules)
								c.execute("insert into Wallpapers (FILENAME) values (:filen)",{"filen":filename})
								conn.commit()
								print "Inserted "+filename
							else:
								badImagesList.append(filename)
								os.remove(directory+"/"+filename)



webtry = urllib2.urlopen('http://boards.4chan.org/'+board+"/")
html = webtry.read()
parser = MyHTMLParser()
parser.feed(html)

for i in range(2,11):
	webtry = urllib2.urlopen('http://boards.4chan.org/'+board+"/"+str(i))
	html = webtry.read()
	parser = MyHTMLParser()
	parser.feed(html)