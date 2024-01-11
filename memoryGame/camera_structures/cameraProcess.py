import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.nn import softmax


class CameraProcess:
    """
    Class that stores methods used for object classification, camera initialization, image process

    Attributes
    ----------
    :arg camera: camera instance
    :arg: image: table that stores 3 images captured to be classified
    :arg roi: predefined ROI
    :arg model: CNN model for object classification
    :arg classes: all classes to be recognized
    """
    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        self.image = []
        self.roi = 380, 170, 224, 224
        self.model = load_model('CNN/model_mobilenet_v7.h5')
        self.classes = ['bee', 'bird', 'cow', 'duck', 'elephant', 'fox', 'frog', 'groundhog', 'ladybug', 'monkey',
                        'octopus', 'owl', 'pig', 'seal']

        self.focus = 60
        self.width = 960
        self.height = 540
        self.roi_table = []

    def start_camera(self):
        """Starts the camera with specific properties"""
        self.camera.set(28, self.focus)
        self.camera.set(3, self.width)
        self.camera.set(4, self.height)

    def capture_image(self):
        """Captures image, crops it and appends to the images table"""
        _, image = self.camera.read()
        cropped = image[self.roi[1]:self.roi[1] + self.roi[3], self.roi[0]:self.roi[0] + self.roi[2]]
        cv2.imwrite('captured.png', cropped)
        self.image.append(cropped)

    def stop_camera(self):
        """Stops the camera"""
        self.camera.release()

    def set_roi(self):
        """Sets the ROI"""
        _, frame = self.camera.read()
        self.roi = cv2.selectROI('select ROI', frame)
        self.roi_table.append(self.roi)

    def predict(self) -> str:
        """Makes a triple prediction and gets the most common one"""
        image = self.image
        image = np.array(image, dtype='float32')
        image = image
        predictions = self.model.predict(image)
        predictions = softmax(predictions)
        best = np.zeros(len(self.classes))
        self.image.clear()
        for prediction in predictions:
            best[np.argmax(prediction)] += 1
        return self.classes[np.argmax(best)]

    def calibrate_camera(self):
        """Shows window with camera image to place the camera on the proper position"""
        while 1:
            _, image = self.camera.read()
            cropped = image[self.roi[1]:self.roi[1] + self.roi[3], self.roi[0]:self.roi[0] + self.roi[2]]
            cv2.imshow('PRESS Q TO QUIT', cropped)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
