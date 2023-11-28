:README.md

#1: TheShendGPT doesn't use any machine learning, it's a joke name to honor TheShend who has been a huge asset to the Street Fighter 3: 3rd Strike Community.

#2: Required libs: cv2, yt_dlp, numpy. Written in Python

#3: Uses subfolders VideoSegments, TestCases, CharacterNames
#:	VideoSegments is where createScreenshots.py will write to. The reason we use a different folder is so that way you could be getting screenshots of a different video while running the program to generate a report on the last batch of screenshots you generated.
#:	TestCases is where you should move the screenshots to that you want to test and generate a report of.
#:	CharacterNames is where you want to save the character profile photo or designator image to. For 3s, I used the character name text.
#:	If you use character portraits, you may have to flip the portraits for 2P side

#4: Usage: 'python3 createScreenshots.py <URL to take 640p screenshots of in 30 second intervals>'
#:	This will take awhile. For a 3 hour video,it took roughly 13.5 minutes. The program will print how many thumbnails it is going to generate and you can look in the VideoSegments folder to see how far along it is.
#:	Once it's done, move your screenshots to TestCases and run 'python3 findMatchups.py <URL> > Results.txt' 
#:	I'm using > Results.txt to pipe it out to a text file which you can easily copy to google sheets or whatever.

#5:	That's it. I'm not a software engineer, if you have recommendations for improvements feel free to reach out.

#6: If you want to run it for a different game, create new test images for the CharacterNames folder and remove the old ones. It is very important that the resolution of your test images match the resolution that you capture from createScreenshots.py
#:	I recommend using createScreenshots first and then getting your match images directly from those screenshots in order to avoid any resolution issues.
#:	My biggest time-waste while working on this project was failing to realize when I was screenshotting from YT that it was stretching the resolution, it was a goofy mistake to make.
