import cv2
import av
import numpy as np

frame_width=960
frame_height=540

pic = np.ones((frame_height, frame_width, 3), dtype=np.uint8) # generate a picture

container = av.open('test.mp4', mode='w')

video_stream = container.add_stream('libx264', rate=25)
video_stream.width=frame_width
video_stream.height=frame_height
video_stream.pix_fmt='yuv420p'

for i in range(100):

    img = pic.copy()

    cv2.putText(img, str(i+1), (int(frame_width/2), int(frame_height/2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 2) # draw frame number on the frame

    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    frame = av.VideoFrame.from_ndarray(tmp, format='rgb24')

    for packet in video_stream.encode(frame):
        container.mux(packet)
    
    cv2.imshow('origin', img)

    cv2.waitKey(40)

for packet in video_stream.encode():
    container.mux(packet)

container.close()

cv2.waitKey(0)