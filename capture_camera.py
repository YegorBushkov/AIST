#!/usr/bin/env python3

from ev3dev.ev3 import *
import pygame
import pygame.camera
import time
from PIL import Image, ImageDraw, ImageFont

lcd = Screen()

pygame.camera.init()
cameras = pygame.camera.list_cameras()
if cameras:
    cam = pygame.camera.Camera(cameras[0])
    cam.start()
    time.sleep(1)

for i in range(10):
    print("Capture Image {}".format(i))
    img = cam.get_image()
    time.sleep(1)
    pil_string_image = pygame.image.tostring(img,"RGBA",False)
    im = Image.frombytes("RGBA",img.get_size(),pil_string_image)
    im.save("img{}.png".format(i),"PNG")
    print("Wait 5...")
    time.sleep(5) 

lcd.clear()

if cameras:
    cam.stop()