from moviepy.editor import VideoFileClip
from skimage.metrics import structural_similarity
import cv2,os,base64
#检测中文
def is_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
#裁切视频
def cut_video(videopath,start,end,path):
    clip = VideoFileClip(videopath).subclip(start,end)
    clip.write_videofile(path)
#匹配图片
def matchImage(imageA,imageB,size):
    #匹配分辨率
    imageA = cv2.resize(imageA,size)
    imageB = cv2.resize(imageB,size)
    #转为灰度照片
    grayA = cv2.cvtColor(imageA,cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB,cv2.COLOR_BGR2GRAY)
    #图片比较
    score = structural_similarity(grayA,grayB)
    if score >= 0.75:
        return 0
    else:
        return 1
#秒转时分秒
def secondsToHours(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return ("%02d:%02d:%02d" % (h, m, s))
#使用列表裁切视频
def useListCutVideo(videoPath,keys,foldername):
    #检测输出文件夹
    if not os.path.exists('output'):
        os.mkdir('output')
    for i in range(len(keys)):
        print('正在裁切第'+str(i+1)+'个视频...')
        #如果文件存在就跳过
        if os.path.exists('output/'+foldername+'/'+str(i+1)+'.mp4'):
            print('文件已存在')
            continue
        #第一个特殊处理
        if i == 0:
            cut_video(videoPath,0,keys[i],'output/'+foldername+'/'+str(i+1)+'.mp4')
        #常规情况
        else:
            cut_video(videoPath,keys[i-1],keys[i],'output/'+foldername+'/'+str(i+1)+'.mp4')
#保存临时文件
def saveTempFile(name,keys):
    #检测文件夹
    if not os.path.exists('temp'):
        os.mkdir('temp')
    #加密名称及关键帧
    namen = base64.b64encode(name.encode()).decode()
    keysn = base64.b64encode(str(keys).encode()).decode()
    #保存文件
    file = open('temp/'+namen+'.txt','w+',encoding='utf-8')
    file.write(keysn)
    file.close()
    return 0
#读取临时文件
def readTempFile(name):
    #检测文件夹
    if not os.path.exists('temp'):
        os.mkdir('temp')
    #加密文件名
    namen = base64.b64encode(name.encode()).decode()
    #检测文件
    if not os.path.exists('temp/'+namen+'.txt'):
        return 1
    #读取文件
    file = open('temp/'+namen+'.txt','r',encoding='utf-8')
    keysn = file.read()
    file.close()
    keys = eval(base64.b64decode(keysn.encode()).decode())
    return keys
#删除临时文件
def removeTempFile(name):
    #检测文件夹
    if not os.path.exists('temp'):
        os.mkdir('temp')
    #加密文件名
    namen = base64.b64encode(name.encode()).decode()
    #检测文件
    if os.path.exists('temp/'+namen+'.txt'):
        os.remove('temp/'+namen+'.txt')
    return 0
#获取视频时长
def getVideoDuration(videoPath):
    cap = cv2.VideoCapture(videoPath)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frames / fps
    cap.release()
    return duration