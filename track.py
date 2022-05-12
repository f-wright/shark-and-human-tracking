# import useful libraries
import cv2
import json
import numpy as np
import sys
from random import randint

# set allowable tracker types
tracker_types = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def runTracker(video_name, tracker_name):
    """ Runs an OpenCV tracker on a video.

    Arguments:
        video_name      -- string, filename of the video to track objects in without file suffix
        tracker_name    -- string, must be one of the options in trackerTypes

    Return:
        nothing, but creates two files - one video with bounding boxes drawn on it, and one json
        file with timestamps and bounding boxes
    """
    # Set video to load
    video_path = video_name + '.mp4'

    # Create a video capture object to read videos
    cap = cv2.VideoCapture(video_path)

    # Read first frame
    success, frame = cap.read()
    # quit if unable to read the video file
    if not success:
        print('Failed to read video')
        sys.exit(1)
        
    height, width = frame.shape[:2]
    file_size = (width, height)

    # set up video file to write output bounding boxes to
    output_video = video_name + "_" + tracker_name + ".mp4"
    output_fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    result = cv2.VideoWriter(output_video,  
                            fourcc, 
                            output_fps, 
                            file_size)

    # get user initialized boxes
    print("To select boxes, drag a box around your desired object with your cursor, starting in" \
        " the upper left corner. If you want to discard a box you drew, don't press any keys and" \
        " simply redraw the correct box. To confirm a box selection, press enter, then enter" \
        " again if you want to select more boxes, or q if that was your last box.")
    bboxes, colors = selectBoxes(frame)

    # create and initialize MultiTracker object
    multiTracker = cv2.MultiTracker_create()
    for bbox in bboxes:
        multiTracker.add(createTrackerByName(tracker_name), frame, bbox)

    # empty dictionary to add bounding boxes to
    bboxes_dict = {}

    # process video and track objects
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # get updated location of objects in subsequent frames through tracking
        success, boxes = multiTracker.update(frame)

        # add bounding boxes to dictionary
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        bboxes_dict[timestamp] = np.array2string(boxes, max_line_width=None)

        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        # write frame to out video and show it
        result.write(frame)
        cv2.imshow('MultiTracker', frame)

        # quit on esc
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyWindow('MultiTracker')
            break

    # stop when the video is finished
    cap.release()
    result.release()
    cv2.destroyWindow('MultiTracker')

    # convert dictionary holding bounding boxes to JSON file
    with open(video_name + '_' + tracker_name + '.json', 'w') as f:
        json.dump(bboxes_dict, f)


def createTrackerByName(tracker_name):
    """ Creates an OpenCV tracker given an input type.

    Arguments:
        trackerType     -- string, must be one of the options in trackerTypes

    Return:
        an OpenCV tracker object
    """
    # Create a tracker based on tracker name
    if tracker_name == tracker_types[0]:
        tracker = cv2.TrackerBoosting_create()
    elif tracker_name == tracker_types[1]:
        tracker = cv2.TrackerMIL_create()
    elif tracker_name == tracker_types[2]:
        tracker = cv2.TrackerKCF_create()
    elif tracker_name == tracker_types[3]:
        tracker = cv2.TrackerTLD_create()
    elif tracker_name == tracker_types[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_name == tracker_types[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif tracker_name == tracker_types[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_name == tracker_types[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in tracker_types:
            print(t)
    return tracker


def selectBoxes(frame):
    """ Given an initial frame, runs an interface which allows the user to draw bounding boxes
    around objects to track. Outputs those bounding boxes

    Arguments:
        frame       -- image, first frame read from a video

    Return:
        bboxes      -- a list of bounding boxes representing initial coordinates for objects
        colors      -- assigned colors for those bounding boxes in video output
    """

    bboxes = []
    colors = [] 

    # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
    # So we will call this function in a loop till we are done selecting all objects
    while True:
        # draw bounding boxes over objects
        print("Selecting object! Press enter to confirm your box once drawn.")
        bbox = cv2.selectROI('MultiTracker', frame)
        bboxes.append(bbox)
        colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))

        # box selected, check if the user wants another
        print("Press q to quit selecting boxes and start tracking, or press enter again to" \
            " select next object")
        k = cv2.waitKey(0) & 0xFF
        print(k)
        if (k == 113):  # q is pressed
            cv2.destroyWindow('MultiTracker')
            break
            
    print('Selected bounding boxes {}'.format(bboxes))
    return bboxes, colors


def main():
    # expected input format: python track.py [video name] [tracker name]
    # if the video name or tracker name are wrong in any way, errors will pop up later on and the
    # program will quit without crashing
    if len(sys.argv) == 3:
        video_name = sys.argv[1]
        tracker_name = sys.argv[2]
        runTracker(video_name, tracker_name)
    else:
        raise Exception("Incorrect number of arguments: %s" % sys.argv)

if __name__ == '__main__':
    sys.exit(main())  