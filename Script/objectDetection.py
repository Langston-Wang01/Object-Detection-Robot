import cv2
from ultralytics import YOLO # type: ignore
import threading
from gpiozero import AngularServo
import math
from hwservo import HwServo

showWindow = False

# Specifications of Webcam
""" 
Webcam Res = 1280 x 720
FOV - H = 102 deg
FOV - D = 120 deg
"""
frameWidth = 1280
frameHeight = 720
horizontalFOV = 102
verticalFOV = horizontalFOV * frameHeight / frameWidth
center = (1280 / 2, 720 / 2)

# Defining Servos
panServo = HwServo(17, initial_angle = 90, min_angle = 10, max_angle = 170)
tiltServo = HwServo(27, initial_angle = 90, min_angle = 10, max_angle = 170)

# Defining the first object being detected
currentTarget = "Phone"


# Helper FUnctions
def setAngleLimit(angle):
    return max(10, min(angle, 170))

def moveServo(panAngle = None, tiltAngle = None):
    if panAngle is not None:
        movePanAngle = setAngleLimit(panServo.angle + (panAngle * 0.15)) # smoothing
        
    if tiltAngle is not None:
        moveTiltAngle = setAngleLimit(tiltServo.angle + (tiltAngle * 0.15)) # smoothing

    if panAngle is not None and tiltAngle is None:
         panServo.angle = movePanAngle

    elif panAngle is None and tiltAngle is not None:
         tiltServo.angle = moveTiltAngle 

    elif panAngle is not None and tiltAngle is not None:
        panServo.angle, tiltServo.angle = movePanAngle, moveTiltAngle
    print("moved ->", panServo.angle, tiltServo.angle)

def dynamicTargetChange():
    global currentTarget
    print("Current Target Set to 'Phone'")
    while True:
        newTarget = input("New Target: ")
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


# Main Function
def liveVideoWithObjectDetection():
    model = YOLO("best.onnx")
    liveVideo = cv2.VideoCapture(0)
    liveVideo.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    thread = threading.Thread(target = dynamicTargetChange, daemon = True)
    thread.start()
    print("loop running")
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
            print(f"det={'Y' if validList else 'N'}  panErr={correctedPanAngle:+.1f}  tiltErr={correctedTiltAngle:+.1f}"
                  f"pan={panServo.angle:.0f}  tilt={tiltServo.angle:.0f}")
            
            if (abs(correctedPanAngle) >= 2):
                moveServo(correctedPanAngle)
            else:
                panServo.release()

            if (abs(correctedTiltAngle) >= 2):
                moveServo(None, correctedTiltAngle)
            else:
                tiltServo.release()

            print("loop end")
        if showWindow:
            annotated_frame = result[validList].plot()
            cv2.imshow('Live Video', annotated_frame)
            keyPressed = cv2.waitKey(1)
            if keyPressed & 0xFF == ord('q'):
                break

    liveVideo.release()
    if showWindow:
        cv2.destroyAllWindows()

try:
    liveVideoWithObjectDetection()
except KeyboardInterrupt:
    print("Stopped")