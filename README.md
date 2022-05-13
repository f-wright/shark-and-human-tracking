# shark-and-human-tracking
Final project for CSCI153 Computer Vision at Harvey Mudd College. 

This project aims to automatically label drone video data to track the motion of sharks and humans in the ocean. It will allow researchers to take advantage of drone footage, which is a useful way of gathering animal related data without disturbing them. It takes an input drone video and initial bounding boxes around objects to track, and output bounding boxes which track each of the sharks and humans in the video over time and space.

## Installation
1. Clone the github repository
2. Setup a conda environment (or something similar) with OpenCV 4.4.0. It is important that the version of OpenCV is not newer, since multiple object tracking was deprecated in later versions.

## Running the tracker
From a folder with the tracker and the video, run:

```
python tracker.py [video name] [tracker name]
```

Video name must be a valid name of an mp4 file in the same folder as `track.py`. If the video name contains spaces, it must be put in quotation marks. Do not include the file type extension, it is assumed to be `.mp4`. Tracker name must be one of the names of the 7 supported OpenCV multiple object tracking models. The name options are BOOSTING, MIL, KCF, TLD, MEDIANFLOW, GOTURN, MOSSE, and CSRT. BOOSTING, MIL, and CSRT were tested as part of this project. 

This will output two files: a video with the bounding boxes drawn on it for easy evaluation, and a json file with ordered timestamps and bounding boxes. In the JSON file, the keys are timestamps in seconds and the values are the bounding boxes (ordered according to their initial labeling). Each bounding box will be in the format `[top left x pixel. top left y pixel.   bounding box width.   bounding box height.]`. 