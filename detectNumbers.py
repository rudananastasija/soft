# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:47:01 2019

@author: Anastasija
"""
import cv2
from Number import Broj

import numpy as np
import math

brojeviBlue=[]
brojeviGreen=[]
regioni = []
   

#ako je plava true,ako je zelena false
def checkNumber(broj,color,region,udaljenost):
    check = False
    
    if color is True:
        if len(brojeviBlue)>0:
            for num in brojeviBlue: 
                razlika=math.sqrt((num.x - broj.x)**2 + (num.y - broj.y)**2)
                 #to je isti broj ako je   
                if razlika <= 20: 
                    num.x = broj.x
                    num.y = broj.y
                    check = True     
                    if udaljenost >= 30:
                        if num.dodao is False:
                            num.slika = region
                            num.dodao = True

                    return num,check
        return broj,check
    else:
        if len(brojeviGreen)>0:
            for num in brojeviGreen: 
                razlika=math.sqrt((num.x - broj.x)**2 + (num.y - broj.y)**2)
                if razlika <= 20: 
                    num.x = broj.x
                    num.y = broj.y
                    check = True
                    if udaljenost >= 30:
                        if num.dodao is False:
                            num.slika = region
                            num.dodao = True

                    return num,check
        return broj,check
        
def prepareImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(image, 170,255, cv2.THRESH_BINARY)
    return im_bw


def resize_region(region):
    img = cv2.resize(region,(28,28), interpolation = cv2.INTER_NEAREST)
    return img


def foundNum(image,lineBlue,lineGreen):
    bin_image =  prepareImage(image) 
    img, contours, hierarchy = cv2.findContours(bin_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    xLijevo = lineBlue[0][0][0] 
    yVece = lineBlue[0][0][1]
    xDesno = lineBlue[0][0][2]
    yManje = lineBlue[0][0][3]
    
    xLijevoZelena = lineGreen[0][0][0] 
    yVeceZelena = lineGreen[0][0][1]
    xDesnoZelena = lineGreen[0][0][2]
    yManjeZelena = lineGreen[0][0][3]
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)  
        region = bin_image[y-2:y+h+2, x-2:x+w+2]
        if h >=13  and w >=1:  
            udaljenost = y+h
            brojBlue = Broj(x,y,False,region,False)
            brojGreen = Broj(x,y,False,region,False)
              
            brojProvjerenBlue,check = checkNumber(brojBlue,True,region,udaljenost)
                          
             #ako je taj broj ponovljen onda imamo flag true,ako je broj prvi put tu onda je flag false i treba da ga dodamo u listu
            if not check:
                brojeviBlue.append(brojProvjerenBlue)
         
            brojProvjerenGreen,check = checkNumber(brojGreen,False,region,udaljenost)
             #ako je taj broj ponovljen onda imamo flag true,ako je broj prvi put tu onda je flag false i treba da ga dodamo u listu
            if not check:
                brojeviGreen.append(brojProvjerenGreen)
                    
            if (x+w) >= xLijevo and x <= xDesno:  #ako je x u dozvoljenim granicama
                        
                if y <= yVece: #ako je y u dozvoljenim granicama
                    if y >= yVece + (x - xLijevo)*((yManje - yVece) / (xDesno - xLijevo)):
                           
                        if not brojProvjerenBlue.flag:
                            brojProvjerenBlue.flag = True
                            #print('***********novi******************')
                            
                            
                            resizovanRegion = resize_region(brojProvjerenBlue.slika)
                            kernel = np.ones((3, 3))
                           
                            img_dil = cv2.dilate(resizovanRegion, kernel, iterations=1)
                            img_close = cv2.erode(img_dil, kernel, iterations=1)
                          
                            regioni.append([img_close,1])
                           
                            cv2.imshow('broj plava',img_close)
                          
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
            if (x+w) >= xLijevoZelena and x <= xDesnoZelena:  #ako je x u dozvoljenim granicama
                        
                if y <= yVeceZelena:
                    if y >= yVeceZelena + (x - xLijevoZelena)*((yManjeZelena - yVeceZelena) / (xDesnoZelena - xLijevoZelena)):
                           
                        if not brojProvjerenGreen.flag:
                            brojProvjerenGreen.flag = True
                            #print('***********novi******************')
                            resizovanRegion = resize_region(brojProvjerenGreen.slika)
                            kernel = np.ones((3, 3))
                            img_dil = cv2.dilate(resizovanRegion, kernel, iterations=1)
                            img_close = cv2.erode(img_dil, kernel, iterations=1)
                            
                            regioni.append([img_close,0])
                            
                            cv2.imshow('broj zelena',img_close)
                                                      
                        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)
                                   
    return image,regioni


