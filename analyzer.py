import os
import subprocess
import glob

# 指定YUV文件目录、x264输出码流目录和JM log目录
path_yuv = '/data/CAOYUE/MSU2021/'
path_264 = '/data/WispChan/x264_benchmark_output/'
path_log = '/data/WispChan/jm_benchmark_output/log/'

# 对MSU序列中每个YUV文件，用ffmpeg计算出x264编码的PSNR和JM编码的PSNR
raw_yuv = glob.glob(path_yuv + "*.yuv")
for vid in raw_yuv:
    # 对YUV文件名称做分割，读取出序列文件名、帧率、分辨率
    yuv_name = (vid.rsplit('/',1)[1]).split('.')[0]
    yuv_frameRate = yuv_name.split('_')[-1]
    yuv_resolution = yuv_name.split('_')[-2]
    yuv_width = yuv_resolution.split('x')[0]
    yuv_height = yuv_resolution.split('x')[1]

    # 使用ffmpeg计算x264的PSNR
    # ffmpeg -pix_fmt yuv420p -r 30 -s 1920x1080 -i /data/CAOYUE/MSU2021/apple_tree_1920x1080_30.yuv -r 30 -i /data/WispChan/x264_benchmark_output/apple_tree_1920x1080_30/apple_tree_1920x1080_30_700.264  -lavfi psnr="stats_file=psnr.log" -f null -
    cmd_x264 = 'ffmpeg -pix_fmt yuv420p -r ' + yuv_frameRate + ' -s ' + yuv_resolution \
               + ' -i ' + path_yuv + yuv_name + '.yuv -r ' + yuv_frameRate + ' -i ' + path_264 \
               + yuv_name + '/' + yuv_name + '_700.264 -lavfi psnr="stats_file=psnr.log" -f null -'
    psnr_x264 = subprocess.getoutput(cmd_x264)

print(psnr_x264)