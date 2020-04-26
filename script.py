import cv2, time, pandas
from playsound import playsound
from datetime import datetime


def playaudio(audiofile):
    playsound(audiofile)

times = []
status_list = [None, None]
first_frame = None
df = pandas.DataFrame(columns = ["Start", "End"])

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21, 21), 0)
    
    if first_frame is None:
        first_frame = gray
        continue
    
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contors in cnts:
        if cv2.contourArea(contors) < 1000:
            continue
        status = 1
        playaudio('beep3.wav')
        (x, y, h, w) = cv2.boundingRect(contors)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    
    status_list.append(status)
    
    if status_list [-1] == 1 and status_list [-2] == 0:
        times.append(datetime.now())
    if status_list [-1] == 0 and status_list [-2] == 1:
        times.append(datetime.now())
        
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Thresh Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)
    
    key = cv2.waitKey(1)
    #print(gray, '\ngray')
    #print(delta_frame, '\ndelta')
    if key == ord("q"):
        if status_list == 1:
            times.append(datetime.now())
        break
    #print(status)
    

print(status_list) 
print(times)
try:
    for i in range (0, len(times), 2):
        df = df.append({"Start":times[i],"End":times[i+1]}, ignore_index = True)
except:
    pass
    
df.to_csv('C:/Users/haris/Documents/new.csv')
video.release() 

cv2.destroyAllWindows