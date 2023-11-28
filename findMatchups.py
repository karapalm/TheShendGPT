import sys #Only imported for argument handler so we can print the timestamped URLs
import time #Used to time and improve efficiency
import cv2 #OpenCV library
import numpy as np #Used to find where the match was greater than the threshold

startTimer = time.time()
from os import listdir
from os.path import isfile, join
#Sort thumbnails alphanumerically
import re
_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]   
            
#Import characters that we're checking for from CharacterNames subfolder
characterCheck = [f for f in listdir("./CharacterNames") if isfile(join("./CharacterNames", f))]
testFiles = [f for f in listdir("./TestCases") if isfile(join("./TestCases", f))]
testFiles.sort(key=natural_sort_key)
#print(testFiles)
url=sys.argv[1]
#Left half for P1 side, take only the top ~1/3 to reduce false-matches
def left_half(image):
    height, width, channels = image.shape
    croppedImage = image[0:int(height/3.5), 0:int(width/2)] 
    return croppedImage

#Right half for P2 side, take only the top ~1/3 to reduce false-matches
def right_half(image):
    height, width, channels = image.shape
    croppedImage = image[0:int(height/3.5), int(width/2):width] #this line crops
    return croppedImage

template = []
i = 0
knownP1 = ''
knownP2 = ''
foundP1Threshold = 0
#Threshold where the loop will end. 0-1 (%), lower can result in more false matches.
minimumThreshold = 0.7
printMatchup = False
#Import all the character images, found it to be faster to load it into an array at the beginning rather than re-loading the image
while i < len(characterCheck):
    template.append(cv2.imread("./CharacterNames/"+characterCheck[i],cv2.IMREAD_GRAYSCALE))
    i = i+1
#Main loop for each Screenshot
for pt in testFiles:
    img_rgb = cv2.imread("./TestCases/"+pt)
#    print(pt) #This line can be useful to print out which screenshot was analyzed
#Split image in half, crop out the bottom
    img_rgbl = left_half(img_rgb)
    img_rgbr = right_half(img_rgb)
#Convert both halves to grayscale
    img_grayl = cv2.cvtColor(img_rgbl, cv2.COLOR_BGR2GRAY)
    img_grayr = cv2.cvtColor(img_rgbr, cv2.COLOR_BGR2GRAY)

    characterFound = 0
    threshold = 0.90
    i = 0
    while characterFound == 0:
        #print(threshold)
        while i < len(characterCheck):
            
            #template = cv2.imread("./CharacterNames/"+characterCheck[i],cv2.IMREAD_GRAYSCALE)
            #w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_grayl,template[i],cv2.TM_CCOEFF_NORMED)
            loc = np.where( res >= threshold)
            #print("Loop Start")
            #print(loc)
            #This commented code below used to draw a box around where the match was which was very helpful during troubleshooting/development
            #for point in zip(*loc[::-1]):
            #    cv2.rectangle(img_rgb, point, (point[0] + w, point[1] + h), (0,0,255), 2)
            #    filename=pt+characterCheck[i][0:len(characterCheck[i])-4]+'.PNG'
            #    cv2.imwrite(filename,img_rgbl)
            if len(loc[0]>0):
                #characterCheck[i][0:len(characterCheck[i])-4] is CharacterName minus .PNG
                if characterCheck[i][0:len(characterCheck[i])-4] != knownP1:
                    printMatchup = True
                    knownP1 = characterCheck[i][0:len(characterCheck[i])-4]
                    #Printing more debug information
                    #foundP1Threshold = threshold
                    #print(characterCheck[i][0:len(characterCheck[i])-4]+' P1 '+str(threshold))
                    #print(url+'&t='+str(int(pt[4:len(pt)-4])*30)+'s')
                characterFound = 1
                
                
            i = i+1
        i = 0
        
        threshold = round(threshold-0.01,2)
        if threshold <= minimumThreshold:
            characterFound = -1
            #Removed this print to declutter the output report
            #print(pt+' P1 Character Not Found')
            
    #Reset everything and do it again for P2 side
    i = 0
    characterFound = 0
    threshold = 0.9
    while characterFound == 0:
        #print(threshold)
        while i < len(characterCheck):
            #templateR = cv2.flip(template[i], 1) #If your designator image is the character portrait, you need to flip the portrait for 2P side.
            templateR = template[i]
            res = cv2.matchTemplate(img_grayr,templateR,cv2.TM_CCOEFF_NORMED)
            loc = np.where( res >= threshold)
            
            if len(loc[0]>0):
                #CharacterName minus .PNG
                if characterCheck[i][0:len(characterCheck[i])-4] != knownP2:
                    printMatchup = True
                    knownP2 = characterCheck[i][0:len(characterCheck[i])-4]

                characterFound = 1
                
                
            i = i+1
        i = 0
        

        threshold = round(threshold-0.01,2)
        if threshold <= minimumThreshold:
            characterFound = -1
            
            #print(pt+' P2 Character Not Found\n')
    if printMatchup == True:
        print(pt)
        print(knownP1+' vs '+knownP2)
        print(url+'&t='+str(int(pt[4:len(pt)-4])*30)+'s\n')
        printMatchup = False



#Print timer to help to reduce runtime
endTimer = time.time()
print(str(endTimer - startTimer)+' Seconds')

