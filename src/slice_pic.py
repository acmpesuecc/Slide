import cv2
img = cv2.imread('assets\\imgs\\brandy.png')
height, width, channels = img.shape
grid = 4
k = 0
for r in range(0, img.shape[0], width // grid + 1):
    for c in range(0, img.shape[1], height // grid + 1):
        cv2.imwrite(f"assets/imgs/gen_imgs/brandy{grid}x{grid}_{k+1}.png", img[r:r + width // grid, c:c + height // grid, :])
        k += 1
        print(width // grid)
