'''
正常模式 视频逐帧分析
测试视频路径：tests/test.mp4
测试图片：cv2.imread('tests/test4.png')
用法：findMatchNormal(视频路径,目标图片)
'''
from utils.videoutils import matchImage,secondsToHours,getVideoDuration
import cv2
import time
def findMatchNormal(videoPath,targetImage):
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
    #获取原始fps和帧数
    orifps = int(cap.get(cv2.CAP_PROP_FPS))
    allframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = 0
    fps = 0
    lastMatch = 0
    starttime = time.time()
    #获取原始时长
    origintime = getVideoDuration(videoPath)
    origintime = secondsToHours(origintime)
    #匹配的帧数列表
    matches = []
    while True: 
        #读取每一帧
        ret,frame = cap.read()
        if ret:
            #获取fps
            frames = frames + 1
            nowtime = time.time()
            fps = int(frames / (nowtime-starttime))
            #获取视频播放时间
            seconds = frames / orifps
            times = secondsToHours(seconds)
            #匹配图片
            if matchImage(frame,targetImage,(50,40)):
                status = "None"
            else:
                status = "Match"
                if (frames - lastMatch) / orifps >= 5 and (allframes - frames) / orifps >= 5:
                    lastMatch = frames
                    #把当前时间点加入要裁切的列表
                    print("在{}(第{}帧,第{}秒)处发现匹配的画面".format(times,frames,seconds))
                    matches.append(seconds)
            #展示画面
            frameshow = cv2.resize(frame,(widthn,heightn))
            frameshow = cv2.putText(frameshow,"Frames:{} CurrentFPS:{} OriginFPS:{} Time:{}/{} Status:{}".format(frames,fps,orifps,times,origintime,status),(0,25),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            #print("Frames:{} CurrentFPS:{} OriginFPS:{} Time:{} Status:{}".format(frames,fps,orifps,times,status))
            cv2.imshow('Preview',frameshow)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyWindow('Preview')
    duration = allframes / orifps
    matches.append(duration)
    print("总分段数：",len(matches))
    return matches