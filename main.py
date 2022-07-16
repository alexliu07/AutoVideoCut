import sys,cv2,os
from tkinter import filedialog,messagebox
from easygui import choicebox,enterbox
from utils.videoutils import is_chinese,useListCutVideo,saveTempFile,readTempFile,removeTempFile
from utils.findmatch_fast import findMatchFast
from utils.findmatch_normal import findMatchNormal
from utils.testfps import testFPS
#模式选择
mode = choicebox("请选择视频分析模式","模式选择",['标准模式(逐帧分析，精确度更高，但速度最慢)','快速模式(跳帧分析，精确度较高，速度较快)','极速模式(跳帧更多，精确度较低，速度更快)','测试电脑分析视频速度(按q终止程序)'])
#选择视频及图片及文件名
videoPath = filedialog.askopenfilename(title="请选择视频文件",filetypes=[('Video File','.mp4')])
if mode != '测试电脑分析视频速度(按q终止程序)':
    targetPath = filedialog.askopenfilename(title="请选择要匹配裁切的图片",filetypes=[('Picture File','.jpg'),('Picture File','.png')])
    foldername = enterbox("请输入输出文件夹名称：",'输入文件夹名称')
    if is_chinese(targetPath) or is_chinese(foldername):
        messagebox.showwarning("提示","文件路径或名称不能包含中文")
        sys.exit()
    targetPicture = cv2.imread(targetPath)
    #建立输出文件夹
    if not os.path.exists('output/'+foldername):
        os.mkdir('output/'+foldername)
if is_chinese(videoPath):
    messagebox.showwarning("提示","文件路径或名称不能包含中文")
    sys.exit()
if mode == '标准模式(逐帧分析，精确度更高，但速度最慢)':
    print('正在分析视频...')
    #检测临时文件
    if readTempFile(foldername) == 1:
        keys = findMatchNormal(videoPath,targetPicture)
        print('正在储存临时文件...')
        saveTempFile(foldername,keys)
    else:
        keys = readTempFile(foldername)
        print('找到临时文件，总分段数为：',len(keys))
    print('分析完毕！')
    #裁切视频
    useListCutVideo(videoPath,keys,foldername)
    print('视频裁切完毕！')
    #删除临时文件
    print('正在删除临时文件...')
    removeTempFile(foldername)
    print('程序执行完毕！')
elif mode == '快速模式(跳帧分析，精确度较高，速度较快)':
    print('正在分析视频...')
    #检测临时文件
    if readTempFile(foldername) == 1:
        keys = findMatchFast(videoPath,targetPicture,'fast')
        print('正在储存临时文件...')
        saveTempFile(foldername,keys)
    else:
        keys = readTempFile(foldername)
        print('找到临时文件，总分段数为：',len(keys))
    print('分析完毕！')
    #裁切视频
    useListCutVideo(videoPath,keys,foldername)
    print('视频裁切完毕！')
    #删除临时文件
    print('正在删除临时文件...')
    removeTempFile(foldername)
    print('程序执行完毕！')
elif mode == '极速模式(跳帧更多，精确度较低，速度更快)':
    print('正在分析视频...')
    #检测临时文件
    if readTempFile(foldername) == 1:
        keys = findMatchFast(videoPath,targetPicture,'superfast')
        print('正在储存临时文件...')
        saveTempFile(foldername,keys)
    else:
        keys = readTempFile(foldername)
        print('找到临时文件，总分段数为：',len(keys))
    print('分析完毕！')
    #裁切视频
    useListCutVideo(videoPath,keys,foldername)
    print('视频裁切完毕！')
    #删除临时文件
    print('正在删除临时文件...')
    removeTempFile(foldername)
    print('程序执行完毕！')
elif mode == '测试电脑分析视频速度(按q终止程序)':
    testFPS(videoPath)