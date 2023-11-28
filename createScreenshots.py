import time #Used to time and improve efficiency
import cv2 #OpenCV used again to write screenshots
import yt_dlp
import sys #Only imported for argument handler so we can print the timestamped URLs
startTimer = time.time()
#from yt_dlp.utils import download_range_func
quality = sys.argv[2]
url=sys.argv[1]
ydl_opts={}
ydl=yt_dlp.YoutubeDL(ydl_opts)
info_dict=ydl.extract_info(url, download=False)

formats = info_dict.get('formats',None)
duration = info_dict.get('duration')
screenshotCount = int(duration/30)
print("Obtaining frames")
print("Total number of screenshots to be taken:"+str(screenshotCount))
for f in formats:
    if f.get('format_note',None) == quality:
        url = f.get('url',None)
        cap = cv2.VideoCapture(url)
        x=0
        count=0
        while x<screenshotCount:
            #print(count)
            #print(x)
            ret, frame = cap.read()
            if not ret:
                break
            filename =r"./VideoSegments/shot"+str(x)+".png"
            x+=1
            cv2.imwrite(filename.format(count), frame)
            count+=900 #Skip 900 frames i.e. 30 seconds for 30 fps
            cap.set(1,count)
            if cv2.waitKey(30)&0xFF == ord('q'):
                break
        if x>=screenshotCount:
            break
        cap.release()
endTimer = time.time()
print(str(endTimer - startTimer)+' Seconds')