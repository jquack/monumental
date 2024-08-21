# src/april_tag.py

import cv2
from pupil_apriltags import Detector
import numpy as np

def detect_april_tag_in_frame(frame, tag_standard: str, K, D, fx, fy, cx, cy, tag_size):
    frame = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY) # we don't need color
    # cv2.imshow("Test Image", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    frame_undistorted = cv2.undistort(
                                        src=frame, 
                                        cameraMatrix=K, 
                                        distCoeffs=D)
    # TODO, maybe detect tags first and then undistord the pixel coordinates afterwards? cheaper?
    # cv2.imshow("Test Image: Undistorted", frame_undistorted)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    detector = Detector(families=tag_standard)
    
    detected_tags = detector.detect(img=frame_undistorted,
                                    estimate_tag_pose=True,
                                    camera_params=[fx, fy, cx, cy],
                                    tag_size=tag_size)
    print(f".... tags found: {len(detected_tags)}")
    return detected_tags
