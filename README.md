Wallpaper-Vomit-Twitter-Bot
===========================

Check the bot out here: https://twitter.com/WallpaperVomit

Regurgitates wallpapers posted on 4chan's /wg/ board.

Requirements:

Twython
Sqlite3
HTMLParser
Twitter Application with keys
Somewhere about 500MB of space for storing the images.


How to use it:

Run main.py first
It will download all the images from the 10 pages of 4chan /wg/
It doesn't dig into each thread so it's not a monstrous amount of media download.

Use your keys in twitterwrapper.py and then run it. It should post once every 10 minutes (or you can adjust it to another time limit).

Enjoy!
