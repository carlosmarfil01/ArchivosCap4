import dlib
import numpy as np
import cv2
import sys
sys.path.append('/content/ArchivosCap4/DeepFake')
from deepfake_face_points_detection import face_points_detection


def select_face(im, r=10):
    faces = face_detection(im)

    if len(faces) == 0:
        print('Detected no faces in image.')
        exit(-1)

    if len(faces) == 1:
        bbox = faces[0]
    else:
        bbox = []

        def click_on_face(event, x, y, flags, params):
            if event != cv2.EVENT_LBUTTONDOWN:
                return

            for face in faces:
                if face.left() < x < face.right() and face.top() < y < face.bottom():
                    bbox.append(face)
                    break

        im_copy = im.copy()
        for face in faces:
            # draw the face bounding box
            cv2.rectangle(im_copy, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 1)
        cv2.imshow('Click the Face:', im_copy)
        cv2.setMouseCallback('Click the Face:', click_on_face)
        while len(bbox) == 0:
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        bbox = bbox[0]

    points = np.asarray(face_points_detection(im, bbox))

    im_w, im_h = im.shape[:2]
    left, top = np.min(points, 0)
    right, bottom = np.max(points, 0)

    x, y = max(0, left-r), max(0, top-r)
    w, h = min(right+r, im_h)-x, min(bottom+r, im_w)-y

    return points - np.asarray([[x, y]]), (x, y, w, h), im[y:y+h, x:x+w]

## Face detection
def face_detection(img,upsample_times=1):
    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    detector = dlib.get_frontal_face_detector()
    faces = detector(img, upsample_times)

    return faces
