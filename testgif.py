from PIL import Image, ImageSequence
import pygame
 

pillow_image = Image.open(r'assets\gif\demon\f2MasterTaiKwaiIdle.gif')
index = 1
    # 使用pillow的ImageSequence获取GIF动图所有帧对应的迭代器
for frame in ImageSequence.all_frames(pillow_image):
            # 以png格式保存在./images/bird/文件夹下面，文件名以gif1、gif2......等为后缀名
    frame.save(f"./assets/npc/demon/Idle/{index}.png", quality=100)
    index = index + 1