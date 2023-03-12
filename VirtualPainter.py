import cv2
import mediapipe as mp
import time
from hand_tracking import HandTracker
import numpy as np

cap = cv2.VideoCapture(0)
header = cv2.imread('D:\Proyectos ML\OpenCV\Hand-tracking\Headers\Header-1.png')
ret, frame = cap.read()
h,w,c = frame.shape
mask = np.ones((h,w,c))
print(mask.shape)

while True:
        ret, frame = cap.read()
        # print(type(frame), frame.shape)
        # print(type(mask),mask.shape)
        # frame = np.multiply(frame, mask)
        h,w,c = frame.shape
        header_h,_,_ = header.shape
        frame = cv2.flip(frame,1)
        
        #set header
        frame[0:header_h,0:w,:]=header
        
        #Get hand landmarks
        hand_lmks=HandTracker().get_landmarks(frame) #hacer una sobrecarga de __call__
        
        #Determine drawing mode
        mode="move"
        if hand_lmks.count(0)==0: #there's a hand in the image
            mode=HandTracker().determine_mode(hand_lmks)
            print(mode)#int(hand_lmks[8].x*10))
        
        if mode=="drawing":
            mask[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),:] = (255,0,0)
            # mask[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),1] = 255
            # mask[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),2] = 255
            print(mask[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),:].shape)
            #  frame[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),0] = 255
            #  frame[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),1] = 255
            #  frame[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),2] = 255
            #  print(frame[int(hand_lmks[8].y*h),int(hand_lmks[8].x*w),:].shape)
            #  print(int(hand_lmks[8].x*w))     

        #show frame
        cv2.imshow('image',mask)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
