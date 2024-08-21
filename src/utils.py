# src/utils.py

import cv2
import json
import numpy as np

def load_video(video_path: str):
    """
    Loads the video from the given path.

    :param video_path: Path to the video file.
    :return: Video capture object (cv2.VideoCapture).
    """
    cap = cv2.VideoCapture(filename=video_path)
    if not cap.isOpened():
        raise ValueError(f"Error opening video file: {video_path}")
    return cap

def load_calibration_data(calibration_path: str):
    """
    Loads the camera calibration data from a JSON file.

    :param calibration_path: Path to the calibration JSON file.
    :return: Calibration data as a dictionary.
    """
    with open(calibration_path, 'r') as file:
        calibration_data = json.load(fp=file)
    return calibration_data


def get_D_and_K_from_calibration(calibration_data):
    fx = calibration_data['fx']
    fy = calibration_data['fy']
    cx = calibration_data['px']
    cy = calibration_data['py']
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    D = np.array(calibration_data['dist_coeffs'])
    return K, D, fx, fy, cx, cy

def get_last_frame(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError(f"Error: Could not open video file at {video_path}")

    # Get the total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Set the video position to the last frame
    video.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 3)
    
    # Read the last frame
    ret, last_frame = video.read()
    
    if not ret:
        raise ValueError("Error: Could not read the last frame from the video.")

    # Release the video capture object
    video.release()
    
    return last_frame

def get_X_frames(video_path, number_of_frames):
    frames = []
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError(f"Error: Could not open video file at {video_path}")

    # Get the total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for x in range(number_of_frames):

    
        # Set the video position to the last frame
        video.set(cv2.CAP_PROP_POS_FRAMES, round(total_frames * (x/number_of_frames)))
        
        # Read the last frame
        ret, frame = video.read()
        frames.append(frame)
        
        if not ret:
            raise ValueError("Error: Could not read frame from the video.")

    # Release the video capture object
    video.release()
    
    return frames