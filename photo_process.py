import cv2
import numpy as np
from PIL import Image, ImageEnhance


def noting(x):
    pass
cv2.namedWindow('image')
cv2.createTrackbar('d','image',0,50,noting)
cv2.createTrackbar('sigmaColor', 'image', 0, 255,noting)
cv2.createTrackbar('sigmaSpace', 'image', 0, 255,noting)
cv2.createTrackbar('getWhite', 'image', 0, 255,noting)
a = cv2.getTrackbarPos('d', 'image')
b = cv2.getTrackbarPos('sigmaColor', 'image')
c = cv2.getTrackbarPos('sigmaSpace', 'image')
d = cv2.getTrackbarPos('getWhite', 'image')
img = cv2.imread('test.png')
# img0 = np.zeros(img.shape, np.uint8)
img0 = img
infmg_1 = np.zeros(img.shape, np.uint8)
infmg_2 = np.zeros(img.shape, np.uint8)
infmg_3 = np.zeros(img.shape, np.uint8)
infmg_4 = np.zeros(img.shape, np.uint8)
while (1):
    key = cv2.waitKey(1)
    if key > 0:
        break
    a2 = cv2.getTrackbarPos('d', 'image')
    b2 = cv2.getTrackbarPos('sigmaColor', 'image')
    c2 = cv2.getTrackbarPos('sigmaSpace', 'image')
    d2 = cv2.getTrackbarPos('getWhite', 'image')
    if a2 != a or b2 != b or c2 != c or d2 != d:
        # print('change!')
        img0 = img
        if not (a2 == b2 == c2 == d2 == 0):
            cv2.bilateralFilter(img0, a, b, c, infmg_1)
            a, b, c = a2, b2, c2
            dst1 = infmg_1 - img0 + 128
            # cv2.imshow("double", dst1)
            infmg_2 = cv2.GaussianBlur(dst1, (1, 1), 0, 0)
            infmg_3 = img0 + 2 * infmg_2 - 255
            # cv2.imshow("gauss", infmg_3)
            infmg_4 = cv2.addWeighted(img0, 0.2, infmg_3, 0.8, 0)
            img0 = cv2.add(img, infmg_4)  # img是原图，infmg_4是最终滤波的结果
        cv2.imshow("res", img0)
    cv2.imshow('ori', img)
cv2.imwrite("res.jpg", img0)
while 1:
    key = cv2.waitKey(1)
    if key > 0:
        break
cv2.destroyAllWindows()


def facial_dermabrasion_effect(fileName):
    img = cv2.imread(fileName)
    blur_img = cv2.bilateralFilter(img, 31, 75, 75)
    #图像融合
    result_img = cv2.addWeighted(img, 0.3, blur_img, 0.7, 0)
    cv2.imwrite("58_1.jpg", result_img)

    image = Image.open("58_1.jpg")
    # 锐度调节
    enh_img = ImageEnhance.Sharpness(image)
    image_sharped = enh_img.enhance(1.5)
    # 对比度调节
    con_img = ImageEnhance.Contrast(image_sharped)
    image_con = con_img.enhance(1.15)
    image_con.save("58_2.jpg")

    img1 = cv2.imread("58.jpg")
    img2 = cv2.imread("58_2.jpg")
    cv2.imshow("1", img1)
    cv2.imshow("2", img2)
    cv2.waitKey()
    cv2.destroyAllWindows()

