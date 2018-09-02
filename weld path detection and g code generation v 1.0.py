from tkinter import *
#import Tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
from collections import deque
import numpy as np
import argparse
import imutils
import os

import time

from scipy import signal
from time import time
import math

cap = cv2.VideoCapture(1)

rho = 2 # distance resolution in pixels of the Hough grid
theta = 1 * np.pi/180 # angular resolution in radians of the Hough grid
threshold = 15	 # minimum number of votes (intersections in Hough grid cell)
min_line_length = 25 #minimum number of pixels making up a line
max_line_gap = 20

kernel_size = 3


i=0
x1=0
x2=0
y1=0
y2=0
pr=.03566
drawing = False
window = Tk()
window.title("Automatic welding G-code Generator V 1.0 By Lislin Luka")
window.geometry('1300x800')
lbl = Label(window, text="Camera view")
lbl.grid(column=2, row=0)
lb2 = Label(window, text="Weld patrh view")
lb2.grid(column=8, row=0)

width, height = 500, 400

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#_, frame = cap.read()

#window.bind('<Escape>', lambda e: window.quit())
lmain = Label(window)
lmain.grid(column=0, row=1,columnspan=6,rowspan=5)
edgew = Label(window)
edgew.grid(column=8, row=1,columnspan=6,rowspan=5)
def show_frame():
    _, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

show_frame()

def textbox():
    
    textframe=Frame(window, width=600, height=110)
    textframe.grid(column=1, row=9)
    textframe.grid_propagate(False)
    textframe.grid_rowconfigure(0, weight=1)
    textframe.grid_columnconfigure(0, weight=1)
    txt=Text(textframe, borderwidth=3, relief="sunken")
    txt.config(font=("consolas", 12), undo=True, wrap='word')
    txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    scrollb = Scrollbar(textframe, command=txt.yview)
    scrollb.grid(row=0, column=1, sticky='nsew')
    txt['yscrollcommand'] = scrollb.set
    
    f=open('gcode.txt','r')
    message=f.read()
    f.close()
    
    #message="G code didnot generated"
    txt.insert(END, message)
    

#textbox()
def setpoint(event,x,y,flags,param):
    global x1
    global x2
    global y1
    global y2
    #print x,y
    global im
    
    global pr
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(im,(x,y),5,(255,0,0),2)
        
        cv2.imshow('img',im)
        if x1==0:
            x1=x
            y1=y
            
            #cv2.circle(im,(x,y),5,(255,0,0),2)
        elif x2==0:
            x2=x
            y2=y
            #cv2.circle(im,(x,y),5,(255,0,0),2)
            print x1,y1,x2,y2
            print 'distance between pt'
            ptd=math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))
            print ptd
            pr=5/ptd
        elif y2>0:
            im=cv2.imread("cali.jpg")
            cv2.imshow('img',im)
            x1=0
            y1=0
            x2=0
            y2=0
            print 'test'

def measure(event,x,y,flags,param):
    global x1
    global x2
    global y1
    global y2
    #print x,y
    global ck
    
    global pr
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(ck,(x,y),5,(255,0,0),2)
        
        cv2.imshow('check',ck)
        if x1==0:
            x1=x
            y1=y
            print 'x1,y1'
            print x1*pr,y1*pr
        elif x2==0:
            x2=x
            y2=y
            print 'x12,y2'
            print x2*pr,y2*pr
            #print x1,y1,x2,y2
            print 'distance between pt'
            ptd=math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))
            print ptd*pr
        elif y2>0:
            ck=cv2.imread("test.jpg")
            cv2.imshow('img',im)
            x1=0
            y1=0
            x2=0
            y2=0




def calibrate():
    
    while(1):
        k = cv2.waitKey(10) & 0xFF
   
        _, frame = cap.read()
        cv2.imshow('frame',frame)
    

        if k == 32:
            cv2.imwrite('cali.jpg',frame)
            global im
            im = cv2.imread("cali.jpg")
        
            cv2.imshow('img',im)
            cv2.namedWindow('img')
            cv2.setMouseCallback('img',setpoint)


    
        if k==116:
            x1=0
            x2=0
            y1=0
            y2=0
            ck = cv2.imread("cali.jpg")
            cv2.imshow('check',ck)
            cv2.namedWindow('check')
            cv2.setMouseCallback('check',measure)
        

        
        if k == 27:
            break


def draw_rect(event,x,y,flags,param):
    global sx
    global sy
    t = time() 
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: '+str(x)+', '+str(y)
        global sx
        sx=x
        global sy
        sy=y
        
    elif event == cv2.EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        ex=x
        ey=y
        
        #cv2.rectangle(img,(sx,sy),(ex,ey),(0,255,0),3)
        
        global matrix
       
        i=0
        x=len(matrix)
        
        while(i<x):
            
            (a,b,c,d)= matrix[i][0]
            if (a or c) in range(min(ex,sx),max(ex,sx)) and (b or d) in range(min(ey,sy),max(ey,sy)):

                matrix= np.delete(matrix,[i],0)
                i=i-1
                x=len(matrix)
            i=i+1
            img1 = cv2.imread('test.jpg')
        
        i=0
        
        while(i<len(matrix)):
            for x1,y1,x2,y2 in matrix[i]:
                cv2.line(img1,(x1,y1),(x2,y2),(0,255,0),2)
            i=i+1
        global img
        img=img1
        print 'ttt'
        #cv2.imshow('delete unwanted',img)

def draw_line(event,x,y,flags,param):
    global matrix
    global i
    global a
    global b
    if event == cv2.EVENT_LBUTTONDBLCLK:
          
        cv2.circle(img,(x,y),1,(255,0,0),-1)

        if(i<1):
            a=x
            b=y
        
        else:
            c=x
            d=y
            matrix= np.append(matrix,[[[a,b,c,d]]],axis=0) 
            cv2.line (img, (int(a), int(b)), (int(c), int(d)), (0,225,0), 2)
            cv2.imshow('Add',img)
            a=c
            b=d
                        
        i=i+1
        
        cv2.imshow('Add',img)


def clicked():
    global img
    global flag
    flag=0
    _, frame = cap.read()
    cv2.imwrite('test.jpg',frame)
    img = cv2.imread('test.jpg')
    gray1=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray1, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blur_gray, 50, 150)
    cv2.imwrite('edge.jpg',edges)
    ed1 = cv2.imread('edge.jpg')
    #cv2.imshow('edge',ed1)
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), minLineLength=min_line_length, maxLineGap=max_line_gap)
    i=0
    global matrix
    matrix=lines
        
        
        
    while(i<len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        i=i+1    
           
    #cv2.imshow('lines',img)
    
    img1 = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img1)
    edgew.imgtk = imgtk
    edgew.configure(image=imgtk)
    
    #lbl.configure(text="Button was clicked !!")
    
def delete():
    while(1):
        k = cv2.waitKey(10) & 0xFF
        global img
        cv2.imshow('delete unwanted',img)
        cv2.namedWindow('delete unwanted')
        cv2.setMouseCallback('delete unwanted',draw_rect)
        cv2.imshow('delete unwanted',img)
        
        if k == 27:
            print 'test11'
            img1 = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img1)
            edgew.imgtk = imgtk
            edgew.configure(image=imgtk)
            break
def Add():
    global i
    i=0
    while(1):
        k = cv2.waitKey(10) & 0xFF
        global img
        cv2.imshow('Add',img)
        cv2.namedWindow('Add')
        cv2.setMouseCallback('Add',draw_line)
        #cv2.imshow('Add',img)
        
        if k==110:
            i=0
            print 'new'
        if k == 27:
            img1 = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img1)
            edgew.imgtk = imgtk
            edgew.configure(image=imgtk)
            break
        

def gcode():
    global matrix
    global pr
    global flag
    gc = open('gcode.txt','w')
    gc.write('N1 T1 M06')
    gc.write('\nN2 G90 G54')
    j=3
    for i in range (0,len (matrix)):
        (a,b,c,d)=matrix[i][0]
        a=a*pr
        b=b*pr
        c=c*pr
        d=d*pr
        gc.write('\nN'+str(j)+' G00 Z3')
        j=j+1
        gc.write('\nN'+ str(j)+' G00 X'+str(a)+' Y'+str(b))
        j=j+1
        gc.write('\nN'+ str(j)+' G00 Z-3')
        j=j+1
        gc.write('\nN'+str(j)+' M23')
        j=j+1
        gc.write('\nN'+str(j)+' G01 X'+str(c)+' Y'+str(d))
        j=j+1
        gc.write('\nN'+str(j)+' M24')
        j=j+1
        
            
    gc.write('\nN'+ str(j)+' M30')
    j=j+1
    print 'G code generated'
    
    gc.close()
    textbox()
    
def draw_curve(event,x,y,flags,param):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img,(x,y),2,(0,0,255),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

def curve():
    print 'fff'
    while(1):
        k = cv2.waitKey(10) & 0xFF
        cv2.imshow('add curve',img)
        cv2.namedWindow('add curve')
        cv2.setMouseCallback('add curve',draw_curve)
        #drawing = False

        if k == 27:
            img1 = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img1)
            edgew.imgtk = imgtk
            edgew.configure(image=imgtk)
            break
def grbl():
    os.startfile("C:\Program Files (x86)\Grbl Controller\GrblController.exe")

btn = Button(window, text="capture", command=clicked)
btn.grid(column=2, row=7,)
btn1 = Button(window, text="calibration", command=calibrate)
btn1.grid(column=1, row=7,)
btn2 = Button(window, text="delete lines", command=delete)
btn2.grid(column=8, row=7)
btn3 = Button(window, text="Add lines", command=Add)
btn3.grid(column=9, row=7)
btn4 = Button(window, text="Generate G CODE ", command=gcode)
btn4.grid(column=9, row=8)
btn5 = Button(window, text="Add curve ", command=curve)
btn5.grid(column=10, row=7)
btn6 = Button(window, text="GRBL G-CODE SENDER ", command=grbl)
btn6.grid(column=11, row=8)
k = cv2.waitKey(10) & 0xFF
print k
if k == 27:
    print 'exit'

window.mainloop()
