import cv2
import numpy as np
import datetime

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False):
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
recording = False

while(True):
  ret, frame = cap.read()

  if ret == True:
    if recording:
        out.write(frame)
        cv2.circle(frame, (40, 40), 15, (0, 0, 255), -1)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('r'):
    # Write the frame into the file 'output.avi'
        if not recording:
            recording = True
            current = datetime.datetime.now()
            name = str(current) + '.avi'
            name = "C:\\Users\\underground\\Desktop\\abc.avi"
            out = cv2.VideoWriter(name,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
            print(name)

    elif key & 0xFF == ord('s'):
        if recording:
            recording = False
            out.release()

    elif key == 27:
        if recording:
            recording = False
            out.release()
        break
    cv2.imshow('frame',frame)
    # Display the resulting frame
    # Press Q on keyboard to stop recording

  # Break the loop
  else:
    break

# When everything done, release the video capture and video write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
