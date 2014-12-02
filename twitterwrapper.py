import os
import time
import sqlite3
from twython import Twython
import wallpaperkeys as keys

def sqlStart():
	return sqlite3.connect('wallpapers.db')
	
def sqlConnection(sqlconn):
	return sqlconn.cursor()

def sqlClose(conn):
	conn.close()
	
def filterSQLResult(string):
	string = string.split("'")
	return string[1]

if __name__ == "__main__":

	twitter = Twython(
    app_key = keys.CONSUMER_KEY,
    app_secret = keys.CONSUMER_SECRET,
    oauth_token = keys.OAUTH_TOKEN,
    oauth_token_secret = keys.OAUTH_TOKEN_SECRET
    )
	
	conn = sqlStart()
	c = sqlConnection(conn)
	
	board = 'wg'
	
	while True:
		try:
			c.execute("SELECT FILENAME FROM Wallpapers ORDER BY RANDOM() LIMIT 1")
			randFilename = filterSQLResult(str(c.fetchone()))
			randImagePath = os.getcwd()+'/'+board+'/'+randFilename
			photo = open(randImagePath,'rb')
			
			twitter.update_status_with_media(media=photo)
			os.remove(randImagePath)
			
			sleep_int = 600 #downtime interval in seconds
			print "Sleeping...\n"
			time.sleep(sleep_int)
	
		except KeyboardInterrupt:
			sys.exit()