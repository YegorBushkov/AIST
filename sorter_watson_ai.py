#!/usr/bin/env python3
# so that script can be run from Brickman

print('>>> AIST ver. 0.5.2 ibm watson <<<')
print('>>> Starting...')
import requests
import json
import pygame
import pygame.camera
from ev3dev.ev3 import *
from time import sleep
import time
from PIL import Image, ImageDraw, ImageFont
from imgcompare import image_diff_percent
from colorama import Fore, Back, Style
from colorama import init

url = "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify"
params = (
    ('api_key', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'),
    ('version', '2016-05-20'),
)

init(autoreset=True)

diff_empty = 2.5

m = MediumMotor('outA')
m1 = LargeMotor('outB')
m2 = LargeMotor('outC')

pygame.mixer.init()
sound = pygame.mixer.Sound('devCon.wav')
time.sleep(1) 


pygame.camera.init()
cameras = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cameras[0]) #176x144

for i in range(10):
    time.sleep(1) # to stabilize
    cam.start()
    img = cam.get_image()
    cam.stop()
    #time.sleep(1)
    pil_string_image = pygame.image.tostring(img,"RGBA",False)
    im_empty = Image.frombytes("RGBA",img.get_size(),pil_string_image)
    im = im_empty
    sound.play()
    print(Fore.CYAN + '>>> Load, please')

    j=0
    while j <= 2:
        cam.start()
        img = cam.get_image()
        #time.sleep(1)
        pil_string_image = pygame.image.tostring(img,"RGBA",False)
        im = Image.frombytes("RGBA",img.get_size(),pil_string_image)
        cam.stop()
        diff = image_diff_percent(im_empty, im)
        if diff >= diff_empty: 
            j=j+1
        elif j > 1:
            j=j-1
           
        print(diff)

    print(Fore.CYAN + '>>> Begin recognition')
    time.sleep(2)
    cam.start()
    img = cam.get_image()
    cam.stop()

    pil_string_image = pygame.image.tostring(img,"RGBA",False)
    im = Image.frombytes("RGBA",img.get_size(),pil_string_image)
    im.save("img{}.png".format(i),"PNG")
    im.close()

    # watson-visual-recognition
    files = {
        'images_file': ('img%s.png' % i, open('img%s.png' % i, 'rb'), 'image/png'),
        'parameters': ('myparams.json', open('myparams.json', 'rb')),
    }

    for j in range(3):
        result = requests.post(url, params=params, files=files).json()
        if result['images_processed'] > 0:
            break
        print('>>> Try again.. ') 

    if result['images'][0]['classifiers']: 
        classes = result['images'][0]['classifiers'][0]['classes']
        print(classes)
        max_score = 0
        max_cl = 'empty'
        for cl in classes:
            print(cl)
            if cl['score'] > max_score:
                max_score = cl['score']
                max_cl = cl['class']
        print(max_cl)

    print('>>> This is ',Fore.GREEN + max_cl,  i)

    if max_cl == 'empty':
       time.sleep(1)

    if max_cl == 'gear':
       m.run_timed(time_sp=2800, speed_sp=300)
       time.sleep(3)

    if max_cl == 'line':
       m.run_timed(time_sp=2100, speed_sp=300)
       time.sleep(2)
       m2.run_to_rel_pos(position_sp=-360, speed_sp=900, stop_action="hold")

    if max_cl == 'angle':
       m.run_timed(time_sp=900, speed_sp=300)
       time.sleep(1)
       m1.run_to_rel_pos(position_sp=-360, speed_sp=900, stop_action="hold")


