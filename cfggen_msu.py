import os
import subprocess
import glob
from jmgen import generate
# ####################
# 使用ffprobe指令，遍历同目录下所有文件，获取其分辨率、帧的数量和帧率
# 同时使用ffmpeg将所有文件转为YUV
# raw_mp4 = [f for f in os.listdir() if os.path.isfile(f)]
path = "/root/"    #指定MSU序列源文件（YUV）的目录
raw_yuv = glob.glob(path + "*.yuv")
# 四个list分别记录视频名称、分辨率、帧数量和帧率
fileName    = []
width       = []
height      = []
frameNumber = []
frameRate   = []
for vid in raw_yuv:
    # 读取每个YUV的大小
    cmd = 'du -b ' + vid
    yuv_size = subprocess.getoutput(cmd).split()[0]
    yuv_name = (vid.rsplit('/',1)[1]).split('.')[0]
    yuv_frameRate = yuv_name.split('_')[-1]
    yuv_resolution = yuv_name.split('_')[-2]
    yuv_width = yuv_resolution.split('x')[0]
    yuv_height = yuv_resolution.split('x')[1]
    yuv_frameNumber = float(yuv_size) / (float(yuv_height)*float(yuv_width)*3/2)

    print(vid, yuv_resolution, yuv_frameRate, yuv_frameNumber)  
    fileName.append(yuv_name)    
    width.append(yuv_width) 
    height.append(yuv_height)
    frameRate.append(yuv_frameRate)
    frameNumber.append(str(int(yuv_frameNumber)))


# 生成每个视频的JM编码器配置文件
shName = 'MSU_JM.sh'      
shFile = open(shName, mode='w', encoding='utf-8')
qpList   = ['26', '28', '30', '32', '35', '38', '41']  # 放弃QP=22、24的编码
for i in range(len(fileName)):
    for qp in qpList:
        generate(path, fileName[i], frameNumber[i], frameRate[i], width[i], height[i], qp)
        shFile.write('./lencod.exe -f ' + fileName[i] + '_' + qp + '.cfg > ' + fileName[i] + '_' + qp + '.log &\n')
    shFile.write("wait\n")
shFile.close()
os.system('chmod 777 ' + shName)