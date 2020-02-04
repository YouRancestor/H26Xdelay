import cv2
import av
import numpy as np

frame_width=960
frame_height=540

pic = np.ones((frame_height, frame_width, 3), dtype=np.uint8) # generate a picture

container = av.open('test1.264', mode='w')

video_stream = container.add_stream('h264_nvenc', rate=25)
video_stream.width=frame_width
video_stream.height=frame_height
video_stream.pix_fmt='yuv420p'
video_stream.codec_context.options={
    # 'preset':'fast', # for h264_nvenc
    'delay':'0', # for h264_nvenc
    # 'zerolatency':'1' # for h264_nvenc
}

container2 = av.open('test.264', mode='r')
video_stream2 = container2.streams.video[0]

for i in range(100):

    img = pic.copy()

    cv2.putText(img, str(i+1), (int(frame_width/2), int(frame_height/2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 2) # draw frame number on the frame

    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    frame = av.VideoFrame.from_ndarray(tmp, format='rgb24')

    for packet in video_stream.encode(frame):
        container.mux(packet)

        # for pkt in container2.demux():
        #     pass

        for frm in video_stream2.decode(packet):
            arr = frm.to_ndarray()
            im = cv2.cvtColor(arr, cv2.COLOR_YUV2BGR_I420)
            cv2.imshow('decoded', im)

    
    cv2.imshow('origin', img)

    cv2.waitKey(40)

for packet in video_stream.encode():
    container.mux(packet)

container.close()

cv2.waitKey(0)