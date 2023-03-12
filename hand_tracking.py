import cv2
import mediapipe as mp
import time

class HandTracker():
    def __init__(self) -> None:
        mpHands = mp.solutions.hands
        self.hands = mpHands.Hands() #Initialize object with default parameters
        mpDraw = mp.solutions.drawing_utils
        self.num_lmks=21
    
    def get_landmarks(self,img):
        '''
        Receives an BGR image and returns its landmarks list (if there's a hand) or None (if there aren't any hands)
        '''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        
        lmks=[0 for i in range(0,self.num_lmks)]
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id,lm in enumerate(handLms.landmark):
                    # print(id,type(lm))
                    lmks[id]=lm
        return lmks
        # try:
        #     for handLms in results.multi_hand_landmarks:
        #         for id,lmk in enumerate(handLms.landmark):
        #             lmks[id]=lmk
        #             print(id,lmk)
        #             # lmks['id']=id
        #             # lmks['lmk']=lmk
        #     return lmks
        # except:
        #     print("hay un error")
        #     return lmks
    def determine_mode(self,lmks):
        '''
        Recevies a list of landmarks and image shape and returns drawing mode:
            - Only index finger up: drawing mode
            - Index and middle up: selection/movement mode
        '''
        # index_pos = 8
        # middle_pos = 12

        # index_lmks=lmks[index_pos]
        # middle_lmks=lmks[middle_pos]

        if lmks[12].y>lmks[9].y and lmks[8].y<lmks[5].y: #middle finger down, index finger up
            mode = "drawing"
        elif lmks[12].y<lmks[9].y and lmks[8].y<lmks[5].y: #middle finger up, index finger up
            mode = "selection"
        else:
            mode = "move"
        return mode
        


# cap = cv2.VideoCapture(0)

def main():

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id,lm in enumerate(handLms.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w),int(lm.y*h)
                    if id == 4:
                        cv2.circle(img, (cx,cy),25,(255,0,255),cv2.FILLED)

                # mpDraw.draw_landmarks(img,handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        
        cv2.imshow('image',img)  
        cv2.waitKey(1)
        
if __name__ == "__main__":
    main()