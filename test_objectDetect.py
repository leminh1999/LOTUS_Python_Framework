import tensorflow as tf
import numpy as np
import cv2

# Load the pre-trained model
# model = tf.keras.models.load_model('ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model')
model = tf.keras.models.load_model('model/saved_model')
# Load the image you want to detect objects in
image = cv2.imread('cat.jpg')

# Convert the image to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Resize the image to the size required by the model
image = cv2.resize(image, (640, 640))

# Convert the image to a numpy array and normalize the pixel values
image = np.array(image, dtype=np.float32)
image = image / 127.5 - 1.0

# Add a batch dimension to the image
image = np.expand_dims(image, axis=0)

# Make a prediction with the model
predictions = model.predict(image)

# Extract the bounding boxes and class labels from the predictions
boxes = predictions[0]['detection_boxes'][0].numpy()
classes = predictions[0]['detection_classes'][0].numpy().astype(np.int32)
scores = predictions[0]['detection_scores'][0].numpy()

# Loop through the bounding boxes and draw them on the image
for i in range(boxes.shape[0]):
    if scores[i] > 0.5:
        ymin, xmin, ymax, xmax = tuple(boxes[i])
        xmin = int(xmin * 640)
        xmax = int(xmax * 640)
        ymin = int(ymin * 640)
        ymax = int(ymax * 640)
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(image, str(classes[i]), (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Show the image with the bounding boxes drawn on it
cv2.imshow('Object detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
