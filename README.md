# Materials 
1. x2 Micro Servo 9g, dual-arm servo horn (SG90)
2. x1 Raspberry Pi 4 Model B
3. x1 Inno-Maker U20CAM-720P
4. x2 4 Cell AA Battery Holders


# Object Detection Robot Log

### Resources for Learning
*NumPy*
1. https://www.youtube.com/watch?v=QUT1VHiLmmI
2. https://www.classcentral.com/classroom/youtube-image-processing-with-python-54897 (Video 1 and 2)

*OpenCV*
1. https://www.youtube.com/watch?v=oXlwWbU8l2o&list=LL&index=15&t=7344s

*PyTorch*
1. https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html

*i) Learning About Neural Networks*
1. https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi (Videos 1-3)

*Linux / Raspberry Pi*
1. https://www.youtube.com/watch?v=ZtqBQ68cfJc&t=10455s
2. https://pinout.xyz

*Tools*

i) Roboflow https://www.youtube.com/watchv=a3SBRtILjPI&t=221s&pp=ygURcm9ib2Zsb3cgdHV0b3JpYWw%3D

ii) Ultralytics
https://academy.ultralytics.com/courses/train-your-first-yolo
https://docs.ultralytics.com/guides/model-evaluation-insights

# Personal Summary Over The Months

### July Summary(27th - 31st): NumPy & Image Fundamentals
- Learned NumPy array creation, slicing, reshaping, and data types, like uint8.
- Created practice challenges (with Claude's help) to apply the syntax and concepts I learned.
- Learned how images are stored as NumPy arrays
- Did basic image processing with arrays: isolating color channels, cropping, inverting, and rotating.
  
### August Summary(1st - 31st): OpenCV & Pytorch Fundamentals
- Learned core OpenCV techniques, like thresholding, masking, contour and edge detection, color space conversion, and live video processing.
- Used HSV color space to isolate and track a specific color in a live webcam feed.
- Built an HSV mask to find the approximate center pixel of a tracked object with specific colors.
- Started learning PyTorch tensors and how they compare to NumPy arrays
- Recapped and learned more Linux command-line commands to make navigating the Pi easier
- Set up a Raspberry Pi headless setup, utilizing Raspberry Connect.
- Took notes on Linux command line for smooth navigation
- Set up the initial pan-tilt setup using the Pi's GPIO pins, SG90 servo motors, and separate batteries for power.
- Had Claude write a quick test script for testing servos

### September Summary (1st - 30th): Hardware Setup & Model Training
- Utilized Roboflow to upload and label images (initially hairbrush, TV remote, wallet)
- Looked over a guide on Ultralytics and trained a model
- Used Google Colab to train a custom YOLOv8 nano model on a T4 GPU 
- Looked at a quick overview of the GPIO library
- Began writing the Object Detection script
- Whilst writing the script, began modeling the physical pan-tilt on Onshape

***October Summary (1st - 5th)***

  
