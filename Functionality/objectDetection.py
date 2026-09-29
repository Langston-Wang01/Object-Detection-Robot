import cv2
from ultralytics import YOLO # type: ignore
import threading
from gpiozero import AngularServo

# Find MAX of USB Cam
video = cv2.VideoCapture(1)
retval, image_frame = video.read()
height, width = image_frame.shape[:2]
print(f"Width: {width}, Height: {height}")
# Width: 1920 Height: 1080


def pixelToServoAngle(pixel, inputMin, inputMax, outputMin = 10, outputMax = 170):
    a = pixel - inputMin
    b = outputMax - outputMin
    c = inputMax - inputMin
    angle = outputMin + (a * b) / c
    return angle

def XYtoPanTiltAngles(x_coord, y_coord):
    pan = pixelToServoAngle(x_coord, 0, 1920)
    tilt = pixelToServoAngle(y_coord, 0, 1080)
    return pan, tilt 


def moveServoWithoutGPIO(panAngle = None, tiltAngle = None):
    panServo = AngularServo(17, min_angle = 10, max_angle = 170)
    tiltServo = AngularServo(27, min_angle = 10, max_angle = 170)

    if panAngle is not None and tiltAngle is None:
         panServo.angle = panAngle

    elif panAngle is None and tiltAngle is not None:
         tiltServo.angle = tiltAngle

    else:
        panServo.angle, tiltServo.angle = panAngle, tiltAngle


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

currentTarget = ""
def dynamicTargetChange():
    global currentTarget
    while True:
        newTarget = input("What Target Would You Like?: ")
        if "tv" in newTarget.lower():
             newTarget = newTarget.strip().title().replace("Tv", "TV")
        else:
            newTarget = newTarget.strip().title()
        currentTarget = newTarget

def liveVideoWithObjectDetection():
    model = YOLO("best.pt")
    liveVideo = cv2.VideoCapture(1)

    thread = threading.Thread(target = dynamicTargetChange, daemon = True)
    thread.start()
    previousPanAngle, previousTiltAngle = 0, 0
    while True:
        retval, frame = liveVideo.read()
        if not retval:
            break 
        result = (model(frame, stream = False))[0]
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
            panAngle, tiltAngle = XYtoPanTiltAngles(currentXCenter, currentYCenter)
            newPanAngle = previousPanAngle + 0.3 * (panAngle - previousPanAngle)
            newTiltAngle = previousTiltAngle + 0.3 * (tiltAngle - previousTiltAngle)

            if (abs(newPanAngle - previousPanAngle) >= 2):
                previousPanAngle = newPanAngle
                moveServoWithoutGPIO(newPanAngle)

            if(abs(newTiltAngle - previousTiltAngle) >= 2):
                previousTiltAngle = newTiltAngle
                moveServoWithoutGPIO(None, newTiltAngle)
            

        annotated_frame = result.plot()
        cv2.imshow('Live Video', annotated_frame)
        keyPressed = cv2.waitKey(1)

        if keyPressed & 0xFF == ord('q'):
            break

    liveVideo.release()
    cv2.destroyAllWindows()
liveVideoWithObjectDetection()
















    
