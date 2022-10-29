import cv2
import os
from random import randint

IMAGE_PATH = "assets\\imgs\\puzzle\\"
image_list = []
for x in os.listdir(IMAGE_PATH):
    if x.endswith(".png"):
        image_list.append(x)

for x in range(len(image_list)):
    img = cv2.imread(f'assets\\imgs\\puzzle\\{image_list[x]}')

    img_parsed = image_list[x] 
    img_parsed = img_parsed[:-4]
    height, width, channels = img.shape
    grid = 4
    k = 0
    for r in range(0, img.shape[0], width // grid + 1):
        for c in range(0, img.shape[1], height // grid + 1):
            cv2.imwrite(f"assets/imgs/gen_imgs/{img_parsed}{grid}x{grid}_{k+1}.png", img[r:r + width // grid, c:c + height // grid, :])
            k += 1
            print(width // grid) 
