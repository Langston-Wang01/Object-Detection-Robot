import cv2
from ultralytics import YOLO # type: ignore
import threading
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
showWindow = False

# Specifications of Webcam
horizontalFOV = 102


# Setting up pigpiod daemon and  Servos
pigoioFactory = PiGPIOFactory()
panServo = AngularServo(17, initial_angle = 90, min_angle = 0, max_angle = 180, min_pulse_width =0.0005, max_pulse_width =0.0025, pin_factory = pigoioFactory)
tiltServo = AngularServo(27, initial_angle = 90, min_angle = 0, max_angle = 180, min_pulse_width =0.0005, max_pulse_width =0.0025, pin_factory = pigoioFactory)

# Defining the first object being detected
currentTarget = "Hand"

# Helper FUnctions

def setAngleLimit(angle): # ensures we dont get errors if angles go past limits
    angle = min(180, angle)
    angle = max(0, angle)
    return angle

def moveServo(panAngle = None, tiltAngle = None):
    if panAngle is not None:
        movePanAngle = setAngleLimit(panServo.angle + (panAngle * 0.3)) # smoothing
        
    if tiltAngle is not None:
        moveTiltAngle = setAngleLimit(tiltServo.angle - (tiltAngle * 0.3)) # smoothing

    if panAngle is not None and tiltAngle is None:
         panServo.angle = movePanAngle

    elif panAngle is None and tiltAngle is not None:
         tiltServo.angle = moveTiltAngle 

    elif panAngle is not None and tiltAngle is not None:
        panServo.angle, tiltServo.angle = movePanAngle, moveTiltAngle

def dynamicTargetChange():
    global currentTarget
    print("Current Target is 'Hand'")
    while True:
        newTarget = input("Select a Target: ")
        if "tv" in newTarget.lower():
             newTarget = newTarget.strip().title().replace("Tv", "TV")
        else:
            newTarget = newTarget.strip().title()
        currentTarget = newTarget

def objectCentroidToServo(Xcenter, Ycenter, frameWidth, frameHeight):
    # Calculate degrees needed to have object at the center of the camera
    xError = frameWidth / 2 - Xcenter
    yError = frameHeight / 2 - Ycenter

    verticalFOV = horizontalFOV * frameHeight / frameWidth
    degreesPerPixelX = horizontalFOV / frameWidth
    degreesPerPixelY = verticalFOV / frameHeight

    adjustedDegreeX = degreesPerPixelX * xError
    adjustedDegreeY = degreesPerPixelY * yError

    return adjustedDegreeX, adjustedDegreeY


# Main Function
def liveVideoWithObjectDetection():
    model = YOLO("best_ncnn_model")
    liveVideo = cv2.VideoCapture(0)
    liveVideo.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    thread = threading.Thread(target = dynamicTargetChange, daemon = True)
    thread.start()
    while True:
        retval, frame = liveVideo.read()
        if not retval: 
            break
        frameHeight, frameWidth = frame.shape[:2]

        result = (model(frame, stream = False, verbose = False, imgsz = 320))[0]
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

        # Calculating Servo Angle, but also creating deadbanding
            correctedPanAngle, correctedTiltAngle = objectCentroidToServo(currentXCenter, currentYCenter, frameWidth, frameHeight)
            
            if (abs(correctedPanAngle) >= 1):
                moveServo(correctedPanAngle)
        

            if (abs(correctedTiltAngle) >= 1):
                moveServo(None, correctedTiltAngle)

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