"""
Challenge #1: Connect my webcam and draw bounding boxes 
and text over live video frames
"""

import cv2 as cv
import numpy as np

def startWebcam():
    liveVideo = cv.VideoCapture(0)
    bool = True
    while bool:
        bool, frame = liveVideo.read() # returns a bool statement and frame
        frame_row = frame.shape[0]
        frame_col = frame.shape[1]
        cv.rectangle(frame, (frame_col // 4 , frame_row // 4), ((frame_col * 3) // 4, (frame_row * 3) // 4), (0,0,255), 3)
        cv.putText(frame, "Me", (frame_col // 2, frame_row // 4), cv.FONT_HERSHEY_PLAIN, 10.0, (0,0,0), 1)
        cv.imshow('Live Video', frame)
        keyPressed = cv.waitKey(1)
        
        if keyPressed & 0xFF == ord('q'): # Claude helped me write this line, to be more reliable
            break
    liveVideo.release()
    cv.destroyAllWindows()


""" 
Challenge #2 Convert a video into HSV color space and use 
thresholding to isolate a bright blue object
"""

def isolateBrightObject():
    liveVideo = cv.VideoCapture(0)
    availableFrame = True
    while availableFrame:
        availableFrame, frame = liveVideo.read()
        hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # Converts to HSV Color Space
        # HSV = Hue, Saturation, Value (brightness)
        lowerRange = (85, 60, 60) # Had Claude help me create a range to target blue objects
        upperRange =(130, 255, 255)

        thresholdedImage = cv.inRange(hsvFrame, lowerRange, upperRange)

        cv.imshow('HSV Live Video', thresholdedImage)
        keyPressed = cv.waitKey(1)

        if keyPressed & 0xFF == ord('q'): # Claude helped me write this line, to be more reliable
            break
    liveVideo.release()
    cv.destroyAllWindows()

"""
Challenge #3: Extract contours from a mask and use spacial moments to track 
the center pixel coordinate and print it dunamically to the console.
"""

def centerPixel():
    liveVideo = cv.VideoCapture(0)
    availableFrame = True
    while availableFrame:
        availableFrame, frame = liveVideo.read()
        hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        lowerRange = (85, 60, 60) 
        upperRange =(130, 255, 255)

        thresholdedImage = cv.inRange(hsvFrame, lowerRange, upperRange) # this is used to create a mask over a blue object, from here we can sum white pixel weights to find the center.
        cv.imshow('HSV Live Video', thresholdedImage)
        keyPressed = cv.waitKey(1)

        # To find the average we need to find the average position of white pixels.
        row_grid, column_grid = np.indices((thresholdedImage.shape[0], thresholdedImage.shape[1]))
        totalWeight = np.sum(thresholdedImage)

        # Find Average row
        weightedRows = np.sum(row_grid * thresholdedImage)
        averageRow = weightedRows // totalWeight

        # Average Column
        weightedColumns = np.sum(column_grid * thresholdedImage)
        averageColumn = weightedColumns // totalWeight

        print(f"Center Pixel: (x: {averageColumn}, y: {averageRow})")

        if keyPressed & 0xFF == ord('q'): # Claude helped me write this line, to be more reliable
            break
    liveVideo.release()
    cv.destroyAllWindows()

centerPixel()




