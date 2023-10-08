import cv2 

# https://medium.com/@mohd-uzair/making-face-filters-with-opencv-e3c928865239
# https://youtu.be/7IFhsbfby9s
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# img = cv2.imread('test.jpg')

filter=cv2.imread("glasses.png")
filter=cv2.resize(filter,(150,150), interpolation = cv2.INTER_AREA)

r,c,h=filter.shape #taking shape of image
#TODO: Does using png remove the need for mask?
img_g=cv2.cvtColor(filter,cv2.COLOR_BGR2GRAY) #converting to gray scale as threshold functions for grey image
ret,mask= cv2.threshold(img_g,10,255,cv2.THRESH_BINARY) # if the value is less than 10=> 0, otherwise 255
mask_i=cv2.bitwise_not(mask)

cap = cv2.VideoCapture(0)
while True:
    #TODO: img vs frame
    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x,y,w,h) in faces:
        # Rectangle color and thickness
        frame = cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

        #dont resize filter because it loses quality by interpolation
        active_filter = cv2.resize(filter, (w,h), interpolation = cv2.INTER_AREA)
        mask = cv2.resize(mask, (w,h), interpolation = cv2.INTER_AREA)
        mask_i = cv2.resize(mask_i, (w,h), interpolation = cv2.INTER_AREA)
        cv2.imshow('Filter', active_filter)
        """
        if(y-h<0): # if you are using video / web cam this condition will take care of your filter not going out of window 
            continue # i.e  your face with filter perfectly fits on window
        """
                     
        roi=active_filter[y-h:y,x:x+w]
        """
        frame_bg=cv2.bitwise_and(roi,roi,mask=mask_i) # Bitwise operation in only that region where mask is present (non zero) and in reference to that  
        frame_fg=cv2.bitwise_and(filter,filter,mask=mask)
        dst = cv2.add(frame_fg,frame_bg)
        dst = cv2.resize(dst, (200,200))
        # frame[hy1-h:hy1,hx1:hx2]=dst
        # Juxtapositioned feed
        cv2.imshow('Edited feed',dst)
        """
        print("x: " , x , " y: " , y , " w: " , w , " h: " , h )
        


    # Unfiltered feed
    cv2.imshow('Feed', img)




    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

cap.release()