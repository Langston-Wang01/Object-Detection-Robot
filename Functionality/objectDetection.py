import cv2
from ultralytics import YOLO # type: ignore
import threading
from gpiozero import AngularServo
import math 

# Specifications of Webcam
""" 
Webcam Res = 1280 x 720
FOV - H = 102 deg
FOV - D = 120 deg
"""
aspectRatio = 1280 / 720
horizontalFOV = 102
verticalFOV = math.degrees(2 * math.atan( math.tan ( math.radians(102) / 2 ) / aspectRatio)) 
center = (1280 / 2, 720 / 2)
frameWidth = 1280
frameHeight = 720

# Defining Servos
panServo = AngularServo(17, min_angle = 10, max_angle = 170)
tiltServo = AngularServo(27, min_angle = 10, max_angle = 170)
initialAngle = 90
panServo.angle, tiltServo.angle = 90, 90

def pixelToServoAngle(pixel, inputMin, inputMax, outputMin = 10, outputMax = 170):
    a = pixel - inputMin
    b = outputMax - outputMin
    c = inputMax - inputMin
    angle = outputMin + (a * b) / c
    return angle

def setAngleLimit(angle):
    return max(10, min(angle, 170))

def moveServoWithoutGPIO(panAngle = None, tiltAngle = None):
    if panAngle is not None:
        movePanAngle = setAngleLimit(panServo.angle + (panAngle * 0.3)) # smoothing
        
    if tiltAngle is not None:
        moveTiltAngle = setAngleLimit(tiltServo.angle + (tiltAngle * 0.3)) # smoothing



    if panAngle is not None and tiltAngle is None:
         panServo.angle = movePanAngle

    elif panAngle is None and tiltAngle is not None:
         tiltServo.angle = moveTiltAngle 

    elif panAngle is not None and tiltAngle is not None:
        panServo.angle, tiltServo.angle = movePanAngle, moveTiltAngle

    else:
        return


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

currentTarget = "Hair Brush"
def dynamicTargetChange():
    global currentTarget
    print("Current Target Set to 'Hair Brush'")
    while True:
        newTarget = input("Would You Like A New Target?: ")
        if "tv" in newTarget.lower():
             newTarget = newTarget.strip().title().replace("Tv", "TV")
        else:
            newTarget = newTarget.strip().title()
        currentTarget = newTarget

def objectCentroidToServo(Xcenter, Ycenter):
    # Calculate degrees needed to have object at the center of the camera
    xError = center[0] - Xcenter
    yError = center[1] - Ycenter

    degreesPerPixelX = horizontalFOV / frameWidth
    degreesPerPixelY = verticalFOV / frameHeight

    adjustedDegreeX = degreesPerPixelX * xError
    adjustedDegreeY = degreesPerPixelY * yError

    return adjustedDegreeX, adjustedDegreeY



def liveVideoWithObjectDetection():
    model = YOLO("best.pt")
    liveVideo = cv2.VideoCapture(0)

    thread = threading.Thread(target = dynamicTargetChange, daemon = True)
    thread.start()
    while True:
        retval, frame = liveVideo.read()
        if not retval:
            break 
        result = (model(frame, stream = False, verbose = False))[0]
        BoundingBox = result.boxes

        # Filtering out names
        namesList = BoundingBox.cls
        validList = []
        for position, idx in enumerate(namesList): # filters out labels that don't match users request
            index = int(idx)
            currentName = result.names[index]
            if currentName == currentTarget:
                validList.append(position)

        # Calculated Object's Centroid
        BoundingBox = result.boxes
        if len(validList) > 0: # makes sure we actually have detections in the frame

            confidenceOfdetectedObjects = []
            for index in validList: # adds the confidence scores of only valid objects
                confidenceOfdetectedObjects.append(BoundingBox.conf[index])
            indexForValidList = 0
            bestRow = 0
            bestConfidence = 0
            currentConfidence = 0

            for confidence in confidenceOfdetectedObjects: # goes through all confidence scores
                currentConfidence = confidence
                if currentConfidence > bestConfidence: # compares current with previous
                    bestRow = validList[indexForValidList]
                    bestConfidence = currentConfidence
                indexForValidList += 1
            detectedObjects = BoundingBox.xywh
            currentXCenter, currentYCenter = detectedObjects[bestRow][0], detectedObjects[bestRow][1]

        # Calculating Servo Angle, but also creating smoothing and deadbanding
            correctedPanAngle, correctedTiltAngle = objectCentroidToServo(currentXCenter, currentYCenter)
      
            if (abs(correctedPanAngle) >= 2):
                moveServoWithoutGPIO(correctedPanAngle)

            if (abs(correctedTiltAngle) >= 2):
                moveServoWithoutGPIO(None, correctedTiltAngle)
            
        annotated_frame = result[validList].plot()
        cv2.imshow('Live Video', annotated_frame)
        keyPressed = cv2.waitKey(1)

        if keyPressed & 0xFF == ord('q'):
            break

    liveVideo.release()
    cv2.destroyAllWindows()
liveVideoWithObjectDetection()
















        newPanAngle = previousPanAngle + 0.3 * (panAngle - previousPanAngle)
    newTiltAngle = previousTiltAngle + 0.3 * (tiltAngle - previousTiltAngle)
