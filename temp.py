import cv2
import numpy as np
import data_train
from detectNumbers import foundNum

cap = cv2.VideoCapture("video-9.avi")
ret, frame = cap.read()
regioni = []

def DetectLine(image,color):
    gg = cv2.GaussianBlur(color, (7, 7), 0)
    kernel = np.ones((5, 5), np.uint8)  
    erozija = cv2.erode(gg, kernel, iterations=1)
    dilacija= cv2.dilate(erozija, kernel, iterations=1)
    edges = cv2.Canny(dilacija, 75, 150)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,maxLineGap=6)        
    return lines

nums = []               
b, g, r = cv2.split(frame)  
zelenaLinija = DetectLine(frame,g)
plavaLinija = DetectLine(frame,b)
model = data_train.ucitajModel() 

suma = 0  
while True:
        ret, frame = cap.read()
        
        if not ret:
             break 
        
       
        key = cv2.waitKey(25)
        slika,regioni  = foundNum(frame,plavaLinija,zelenaLinija)
                    
        cv2.imshow('slika',slika)
        if key == 27:
            break



for region in regioni:
            #broj= np.reshape(region,[1,28,28,1])
            #broj= np.reshape(region,[-1,28,28,1])
            #broj=np.reshape(region,(-1,28,28,1))
                
            broj = region[0].reshape(1,28,28,1)
        
            predikcija = model.predict(broj)
           
            number = predikcija.argmax()
            print(number)
            if region[1]==1: 
                print('plava')
                suma += number
                
            else:
                print('zelena')
                suma -= number
                
        
print('suma je')            
print(suma)                   
      
cap.release()
cv2.destroyAllWindows()