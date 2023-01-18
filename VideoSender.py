"""
VideoSender

"""
import socket
import time
import cv2
from PIL import Image
import numpy as np
import sys



HOST = "IP address reported by VideoReceiver.py"  # server IP address
PORT = 8000             # server port

MATRIX_X,MATRIX_Y=64,32	# the size of the Waveshare matrix

DEBUG=False
DEFAULT_FPS=27

SOURCE="Your MP4 video"


serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# check the source file exists
try:
    # just try to open the video
    with open(SOURCE) as fp:
       print(f"Source {SOURCE} exists")

except Exception as e:
    print(f"Unable to open {SOURCE}. Error was {e}.Quitting")
    sys.exit(0)

vid=cv2.VideoCapture(SOURCE)


# LED colour correction factors
gain_r=1.0
gain_g=0.8
gain_b=0.5

# work out aspect ratio using first frame

(grabbed, frame) = vid.read()
frame_h,frame_w=frame.shape[:2]

ASPECT_RATIO=frame_h/frame_w

X_SIZE = int(MATRIX_X * ASPECT_RATIO)
Y_SIZE = int(MATRIX_Y * ASPECT_RATIO)
DSIZE = (X_SIZE, Y_SIZE) # scaling sizes to reduce the frame to fit the matrix
X_OFF = int((MATRIX_X - X_SIZE) / 2) # offsets for placing the frame in the matrix
Y_OFF = int((MATRIX_Y - Y_SIZE) / 2)

image_data = np.zeros((MATRIX_Y, MATRIX_X), dtype=np.uint16)  # the output frame

print(f"frame_h {frame_h} frame_w {frame_w} aspect {ASPECT_RATIO}")

# work out the video frame rate
# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
FPS=DEFAULT_FPS
if int(major_ver)  < 3 :
    FPS = vid.get(cv2.cv.CV_CAP_PROP_FPS)
    print(f"Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {FPS}")
else :
    FPS = vid.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second using video.get(cv2.CAP_PROP_FPS) : {FPS}")

FRAMETIME=1.0/FPS

frame_count=0

#########################################################
while True:
    frame_start = time.monotonic()
    (grabbed, frame) = vid.read()

    if not grabbed:
        logit("Frame not grabbed from source! End of video?")
        serverSocket.close()
        break

    if DEBUG:
        cv2.imshow("frame",frame)
        cv2.waitKey(0)

    # reduce image keeping aspect ratio
    res = cv2.resize(frame, dsize=DSIZE, interpolation=cv2.INTER_CUBIC)

    # colour correction required for LED matrix
    res[:,:,0]=np.minimum(res[:,:,0]*gain_r,255)
    res[:,:,1]=np.minimum(res[:,:,1]*gain_g,255)
    res[:,:,2]=np.minimum(res[:,:,2]*gain_b,255)

    # convert to RGB565
    R5 = (res[..., 0] >> 3).astype(np.uint16) << 11
    G6 = (res[..., 1] >> 2).astype(np.uint16) << 5
    B5 = (res[..., 2] >> 3).astype(np.uint16)

    # Assemble components into RGB565 uint16 image
    RGB565 = R5 | G6 | B5

    # paste the image into the matrix shape
    image_data[Y_OFF:Y_OFF+Y_SIZE,X_OFF:X_OFF+X_SIZE]=RGB565 # default aspect ratio 1:1

    # flatten the image into a 1D array of bytes
    flat=image_data.flatten()
    frame_bytes=flat.tobytes()
    bytes_sent = serverSocket.sendto(frame_bytes, (HOST, PORT))

    #print(f"Sent {bytes_sent}")
    cv2.imshow("frame", image_data)
    cv2.waitKey(1)
    # don't send too fast otherwise we get a Laurel and Hardy film
    while (time.monotonic() - frame_start) < FRAMETIME:
        pass

