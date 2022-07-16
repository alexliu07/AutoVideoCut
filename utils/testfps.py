'''
检测当前电脑播放视频fps
用法：testFPS(视频路径)
'''
import cv2
import time
#获取视频路径
def testFPS(videoPath):
    #读取视频
    cap = cv2.VideoCapture(videoPath)
    #获取视频尺寸
    sizeget = cv2.VideoCapture(videoPath)
    sizeget.set(cv2.CAP_PROP_POS_FRAMES,0)
    sizeimg = sizeget.read()[1]
    height,width = sizeimg.shape[:2]
    heightn = int(height/2)
    widthn = int(width/2)
    sizeget.release()
    #获取原始fps
    orifps = int(cap.get(cv2.CAP_PROP_FPS))
    frames = 0
    fps = 0
    starttime = time.time()
    while True: 
        #读取每一帧
        ret,frame = cap.read()
        if ret:
            #获取fps
            frames = frames + 1
            nowtime = time.time()
            fps = int(frames / (nowtime-starttime))
            #展示画面
            frameshow = cv2.resize(frame,(widthn,heightn))
            frameshow = cv2.putText(frameshow,"CurrentFPS:{} OriginFPS:{}".format(fps,orifps),(0,25),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.imshow('Preview',frameshow)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyWindow('Preview')