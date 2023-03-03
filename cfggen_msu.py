import os
import subprocess
import glob
from jmgen import generate

# ####################
path = "/data/CAOYUE/MSU2021/"    #指定MSU序列源文件（YUV）的目录
raw_yuv = glob.glob(path + "*.yuv")
# 五个list分别记录视频名称、分辨率、帧数量和帧率
fileName    = []
width       = []
height      = []
frameNumber = []
frameRate   = []

for vid in raw_yuv:
    # 读取每个YUV的大小: yuv_size
    cmd = 'du -b ' + vid
    yuv_size = subprocess.getoutput(cmd).split()[0]
    # 对YUV文件名称做分割，读取出序列文件名、帧率、分辨率
    yuv_name = (vid.rsplit('/',1)[1]).split('.')[0]
    yuv_frameRate = yuv_name.split('_')[-1]
    yuv_resolution = yuv_name.split('_')[-2]
    yuv_width = yuv_resolution.split('x')[0]
    yuv_height = yuv_resolution.split('x')[1]
    # 用YUV文件大小除以（像素数×3÷2），计算YUV序列中帧的个数
    yuv_frameNumber = float(yuv_size) / (float(yuv_height)*float(yuv_width)*3/2)

    # 将数据添加到五个List中
    print(vid, yuv_resolution, yuv_frameRate, yuv_frameNumber)  
    fileName.append(yuv_name)    
    width.append(yuv_width) 
    height.append(yuv_height)
    frameRate.append(yuv_frameRate)
    frameNumber.append(str(int(yuv_frameNumber)))


# 生成每个视频的JM编码器配置文件
shName = 'MSU_JM.sh'      
shFile = open(shName, mode='w', encoding='utf-8')
qpList   = ['26', '28', '30', '32', '35', '38', '41']  # 放弃QP=22、24的编码，使用7个QP值
# 循环对每个序列生成配置文件并且写入Shell脚本
for i in range(len(fileName)):
    for qp in qpList:
        generate(path, fileName[i], frameNumber[i], frameRate[i], width[i], height[i], qp)
        shFile.write('./lencod.exe -f ' + fileName[i] + '_' + qp + '.cfg > ' + fileName[i] + '_' + qp + '.log &\n')
    # 此时同时并行对一个序列的7个QP值编码，即同时并行执行7条lencod指令。如果要改变程序并行度，只需要改变'wait'插入的位置即可。
    shFile.write("wait\n")
shFile.close()
os.system('chmod 777 ' + shName)