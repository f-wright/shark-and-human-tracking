# shark-and-human-tracking
Final project for CSCI153 Computer Vision at Harvey Mudd College. 

This project aims to automatically label drone video data to track the motion of sharks and humans in the ocean. It will allow researchers to take advantage of drone footage, which is a useful way of gathering animal related data without disturbing them. It takes an input drone video and initial bounding boxes around objects to track, and output bounding boxes with labels which track each of the sharks and humans in the video over time and space.

## Installation
1. Clone the github repository
2. Setup a conda environment (or something similar) with OpenCV 4.4.0. It is important that the version of OpenCV is not newer, since multiple object tracking was deprecated in later versions.

## Running the tracker
From a folder with the tracker and the video, run:

```
python tracker.py [video name] [tracker name]
```

This will output two files: a video with the bounding boxes drawn on it for easy evaluation, and a text file with ordered bounding boxes.