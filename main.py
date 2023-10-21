import os
import cv2

def loadFilter(name):
    global filter,filter_gray, ret, mask, mask_inv

    # Load the filter image
    filter = cv2.imread(name)

    # Convert filter to grayscale for creating a mask
    filter_gray = cv2.cvtColor(filter, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(filter_gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

def applyFilter():
    # Resize the filter to match the size of the detected face
    global x,y,w,h
    match filterSelection:
        case 0:
            scaling_factor = max(1.0, 3.0/(w*h))
            custom_w = int(1.2*scaling_factor*w)
            custom_h = int(1*scaling_factor*h)
            print(scaling_factor)

            #hat starts from the forehead (so y+e) and needs to be shifted a bit
            y = int(1.35*y)
            x = int((1-0.1)*x)

        case 1:
            custom_w = int(1*w)
            custom_h = int(0.9*h)

    current_filter = cv2.resize(filter, (custom_w, custom_h), interpolation=cv2.INTER_AREA)
    mask_resized = cv2.resize(mask, (custom_w, custom_h), interpolation=cv2.INTER_AREA)
    mask_inv_resized = cv2.resize(mask_inv, (custom_w, custom_h), interpolation=cv2.INTER_AREA)

    # Region of Interest (ROI) in the frame where the hat will be placed
    # TODO: Crop hat to avoid this check

    # Out of bounds
    if(y-custom_h<0 or x+custom_h<0): # if you are using video / web cam this condition will take care of your filter not going out of window 
        return # i.e  your face with filter perfectly fits on window

    #TODO: Smoothen filter using epsilon comparing to previous array.
    # Do this before cv calculations so its faster
    match filterSelection:
        case 0:
            roi = frame[y - custom_h: y, x:x + custom_w]

        case 1:
            roi = frame[y:y + custom_h, x:x + custom_w]

    # debug
    os.system('cls' if os.name == 'nt' else 'clear')
    print("roi: ", roi.shape, " mask: ", mask_inv_resized.shape)
    print("x, y, w, h: ", x , " ", y , " ", custom_w, " ", custom_h, "\n")

    # Use the mask to create a masked region
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv_resized)
    roi_fg = cv2.bitwise_and(current_filter, current_filter, mask=mask_resized)

    # Add the masked hat and the original ROI
    dst = cv2.add(roi_bg, roi_fg)

    # Replace the ROI in the frame with the combined result
    match filterSelection:
        case 0:
            frame[y - custom_h: y, x:x + custom_w] = dst

        case 1:
            frame[y:y + custom_h, x:x + custom_w] = dst


# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
# Default filter
loadFilter("filters/pirate_hat.png")

# TODO: Buffer faces for 5 frames before applying filter (so artifacts are removed)
# Use epsilon around x,y,w,h values


# TODO: Replace numbers with hashmap, same for k
filterSelection = 0

cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)

    for (x, y, w, h) in faces:
        # Highlight each face
        rect = cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 1)

        applyFilter()

    #time.sleep(0.5)
    # Display the frame with the filter
    cv2.imshow('Filter added', frame)

    # Asynchronous button click to cycle through filters
    k = cv2.waitKey(3) & 0xff
    if k==0xff:
        k = filterSelection + 48

    match k:
        # Check for the 'Esc' key to exit the loop
        case 27:
            break

        case 48:
            filterSelection = k - 48
            loadFilter("filters/pirate_hat.png")


        case 49:
            filterSelection = k - 48
            loadFilter("filters/glasses.png")

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
