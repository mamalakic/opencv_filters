import cv2

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the (default) filter image
filter = cv2.imread("pirate_hat.png")
filter = cv2.imread("glasses.png", cv2.IMREAD_UNCHANGED)
filter = cv2.resize(filter, (150, 150), interpolation=cv2.INTER_AREA)
#r, c, h = filter.shape

# Convert filter to grayscale for creating a mask
filter_gray = cv2.cvtColor(filter, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(filter_gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)


cap = cv2.VideoCapture(0)

while True:
    cv2.imshow('filter', mask_inv)    
       # print("x: " , x , " y: " , y , " w: " , w , " h: " , h )
    # Check for the 'Esc' key to exit the loop
    k = cv2.waitKey(30) & 0xff

    match k:
        case 27:
            break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()