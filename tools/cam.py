import cv2
import time
from pathlib import Path

from pycv2.tools.utils import *
from pycv2.img.utils import resize_img

#cap.set(cv2.CAP_PROP_POS_FRAMES,int(frame_count/2))
#milliseconds = 1000*60
#cap.set(cv2.CAP_PROP_POS_MSEC, milliseconds)
def get_cam_properties(cap):
    """
    return dictionary of fps and frame count
    """
    fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return {"fps":fps,"frame_count":frame_count}
def show_cam_prop(cap:cv2.VideoCapture):
    fps,frame_count=list(get_cam_properties(cap).values())
    duration = frame_count/fps
    print('fps = ' + str(fps))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(duration))
    minutes = int(duration/60)
    seconds = duration%60
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
def video_saver(file_name,video_capture,fourcc=cv2.VideoWriter_fourcc("m","p","4","v")
    ,start_time=0,end_time=float("inf"),fps_v=None,funct=None):
    h,w=video_capture.read()[1].shape[:2]
    
    fps,frame_count=list(get_cam_properties(video_capture).values())
    duration = frame_count/fps
    end_time=min(end_time,duration)
    start_time=min(start_time,end_time)
    start_frame=int(fps*start_time)
    end_frame=int(fps*end_time)
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    if fps_v is None:
        fps_v=fps
    out=cv2.VideoWriter(file_name,fourcc,fps_v,(w,h))
    for _ in progressBar(range(start_frame,end_frame), prefix = 'Progress:', suffix = 'Complete', length = 50):
        success,frame=video_capture.read()
        if not success:break
        if not funct is None:
            frameNumber=video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            frame=funct(frame,frameNumber,fps)
        out.write(frame)
    out.release()
def conver_frames2video(file_name,
        frames,fourcc=cv2.VideoWriter_fourcc("m","p","4","v"),
    fps_v=20,funct=None):
    h,w=frames[0].shape[:2]
    out=cv2.VideoWriter(file_name,fourcc,fps_v,(w,h))
    for id,frame in enumerate(progressBar(frames, prefix = 'Progress:', suffix = 'Complete', length = 50)):
        if not funct is None:
            frame=funct(frame,frameNumber=id,fps=fps_v)
        out.write(frame)
    out.release()
#fps the number of frames per seconds
class FPS():
    def __init__(self):
        self.start_t=0
    @staticmethod
    def calculate_fps(time_passed,frames):
        return frames/time_passed
    def start(self):
        self.start_t=time.time()
    def end(self,frame=None):
        starttime=self.start_t
        self.start_t=time.time()
        fps=int(1/(time.time()-starttime))
        if not frame is None:
            cv2.putText(frame,str(fps),(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0))
        return fps

class VIDEO_SAVER(cv2.VideoCapture):
    def __init__(self,url):
        super().__init__(url)
    def start(self):
        from win32api import GetSystemMetrics
        WIDTH= GetSystemMetrics(0)
        HEIGHT= GetSystemMetrics(1)
        from pykeyboard import keyboards
        from pykeyboard.keys import ENTER,ESC
        control=keyboards()

        print("setting camera")
        print("click ENTER to confirm")
        fps=int(get_cam_properties(self)["fps"])
        token=int((6/fps)*100)
        frames=[]
    
        while not control.pressedkey(ESC):
            ret, frame = self.read()
            if not ret:
                print("fialed")
                break  
            if frame.shape[0]>=HEIGHT-400:
                frame=resize_img(frame,height=HEIGHT)
            if frame.shape[1]>=WIDTH-20:
                frame=resize_img(frame,width=WIDTH)
            if control.pressedkey(ENTER):
                frames.append(frame)
                print(len(frames))
            cv2.imshow("WIDNDOW",frame)
            cv2.waitKey(token)
        conver_frames2video("saved_video.mp4",frames,fps_v=30)

        cv2.destroyAllWindows()
        control.stop_checking_all()

class Fast_set_cam(cv2.VideoCapture):

    def __init__(self,url):
        super().__init__(url)
    def start(self):
        from win32api import GetSystemMetrics
        WIDTH= GetSystemMetrics(0)
        HEIGHT= GetSystemMetrics(1)
        from pykeyboard import keyboards
        from pykeyboard.keys import ENTER
        control=keyboards()

        print("setting camera")
        print("click ENTER to confirm")
        fps=int(get_cam_properties(self)["fps"])
        token=int((6/fps)*100)
        while not control.pressedkey(ENTER):
            ret, frame = self.read()
           
            if not ret:
                print("failed")
                break  
            if frame.shape[0]>=HEIGHT-400:
                frame=resize_img(frame,height=HEIGHT)
            if frame.shape[1]>=WIDTH-20:
                frame=resize_img(frame,width=WIDTH)
            cv2.imshow("WIDNDOW",frame)
            cv2.waitKey(token)
        cv2.destroyAllWindows()
        control.stop_checking_all()
if __name__=="__main__":
    #print(WIDTH,HEIGHT)
    VIDEO_SAVER("http://192.168.0.104:8080/video").start()