*To even integrate YOLO into Python run this command:*
            from ultra import YOLO

***Below is a list of commands you can use to load, train or evalute a models performance on a validation set***

# Create a new YOLO model from scratch
model = YOLO("yolo26n.yaml")

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo26n.pt")

# Train the model using the 'coco8.yaml' dataset for 3 epochs (cycles)
results = model.train(data="coco8.yaml", epochs=3)

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model("https://ultralytics.com/images/bus.jpg")

# Export the model to ONNX format
success = model.export(format="onnx")



***Train***
- Train Mode is used for training a YOLO model on a custom dataset.
*example*
        from ultralytics import YOLO

        model = YOLO("yolo26n.yaml")
        results = model.train(data="coco8.yaml", epochs=5)

***Val***
- Used to validate a YOLO model after training, uses a validation set to measure accuracy and generalize performance.
*example*
        from ultralytics import YOLO

        # Load a YOLO model
        model = YOLO("yolo26n.yaml")

        # Train the model
        model.train(data="coco8.yaml", epochs=5)

        # Validate on training data
        model.val() 

***Export***
- Used for exported a YOLO model to a format that can be used for deployment.
*example (exports a YOLO model to ONYX)*
        from ultralytics import YOLO

        model = YOLO("yolo26n.pt")
        model.export(format="onnx", dynamic=True)


***Track***
- Used to track objects in real-time using a YOLO model. The model is loaded from a checkpoint file, and the user can provide a live video stream for object tracking. 
*example*
        from ultralytics import YOLO

        # Load a model
        model = YOLO("yolo26n.pt")  # load an official detection model
        model = YOLO("yolo26n-seg.pt")  # load an official segmentation model
        model = YOLO("path/to/best.pt")  # load a custom model

        # Track with the model
        results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True)
        results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True, tracker="bytetrack.yaml")