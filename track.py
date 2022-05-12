# import useful libraries
import cv2
from __future__ import print_function
import sys
from random import randint

# set allowable tracker types
trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def runTracker():
    # Set video to load
    video_folder = "shark_human_data/"
    video_prefix = "20200805_OneSharkSUPSurfers"
    video_path = video_folder + video_prefix + '.mp4'

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

    # We want to save the output to a video file
    output_filename = video_prefix + '_KCF.mp4'
    output_frames_per_second = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    result = cv2.VideoWriter(output_filename,  
                            fourcc, 
                            output_frames_per_second, 
                            file_size)

    print("input fps: ", output_frames_per_second)

    ## Select boxes
    bboxes = []
    colors = [] 

    # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
    # So we will call this function in a loop till we are done selecting all objects
    while True:
        # draw bounding boxes over objects
        # selectROI's default behaviour is to draw box starting from the center
        # when fromCenter is set to false, you can draw box starting from top left corner
        bbox = cv2.selectROI('MultiTracker', frame)
        bboxes.append(bbox)
        colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        k = cv2.waitKey(0) & 0xFF
        print(k)
        if (k == 113):  # q is pressed
            cv2.destroyWindow('MultiTracker')
            break
            
    print('Selected bounding boxes {}'.format(bboxes))

    # Specify the tracker type
    trackerType = "KCF"

    # Create MultiTracker object
    multiTracker = cv2.MultiTracker_create()

    # Initialize MultiTracker
    for bbox in bboxes:
        multiTracker.add(createTrackerByName(trackerType), frame, bbox)


    # Process video and track objects
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)

        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        # write frame to out video
        result.write(frame)
        
        # show frame
        cv2.imshow('MultiTracker', frame)
        

        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            cv2.destroyWindow('MultiTracker')
            break

        
    # Stop when the video is finished and release recording
    cap.release()
    result.release()
    cv2.destroyWindow('MultiTracker')


    cap = cv2.VideoCapture("20200805_OneSharkSUPSurfers_KCF.mp4")
    output_frames_per_second = result.get(cv2.CAP_PROP_FPS)
    print("output fps: ", output_frames_per_second)
    cap.release()


def createTrackerByName(trackerType):
    """ Creates an OpenCV tracker given an input type.

    Arguments:
        trackerType     -- string, must be one of the options in trackerTypes

    Return:
        an OpenCV tracker object
    """
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)
    return tracker