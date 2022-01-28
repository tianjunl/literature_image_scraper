"""
This file contains the object detection model and two functions, which 
A) takes in an image file and output the detected object list,
B) counts each detected object.

Please install the following libraries in exact version.
!pip install numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 keras-resnet==0.2.0
!pip install tensorflow==2.4.0 keras==2.4.3 opencv-python imageai
"""

import os
from imageai.Detection.Custom import CustomObjectDetection


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("models/earwig_detect_model-ex-057--loss-0016.027.h5")
detector.setJsonPath("models/earwig_detect_config.json")
detector.loadModel()


def DetectObjects(image_name, image_ext, source_path, cache_path):
    detections = detector.detectObjectsFromImage(
        input_image=source_path + image_name + "." + image_ext,
        output_image_path=cache_path + image_name + "-detected.jpg",
    )
    os.remove(cache_path + image_name + "-detected.jpg")

    return detections


def CountObjects(detections):
    cercus = 0
    cerci = 0
    earwig = 0
    for detection in detections:
        if detection["name"] == "cercus":
            cercus += 1
        elif detection["name"] == "cerci":
            cerci += 1
        else:
            earwig += 1

    return cercus, cerci, earwig


if __name__ == "__main__":
    base_path = os.getcwd()
    cache_path = base_path + "data/output_test/cache/"
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    image = "./literature_image_scraper/data/img/file_41_p_26_1.jpg"

    detections = DetectObjects(image, cache_path)
    for detection in detections:
        print(
            detection["name"],
            " : ",
            detection["percentage_probability"],
            " : ",
            detection["box_points"],
        )
