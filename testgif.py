from PIL import Image, ImageSequence
import pygame
 

pillow_image = Image.open(r'assets\gif\烟花礼花卡通装饰贴纸 (37)_爱给网_aigei_com.gif')
index = 1
    # 使用pillow的ImageSequence获取GIF动图所有帧对应的迭代器
for frame in ImageSequence.all_frames(pillow_image):
            # 以png格式保存在./images/bird/文件夹下面，文件名以gif1、gif2......等为后缀名
    frame.save(f"assets/background/fireworks/{index}.png", quality=100)
    index = index + 1