import cv2
import numpy as np
from PIL import Image, ImageEnhance


class photo(object):

    def __init__(self, path):
        self.img = cv2.imread(path)

    def lighten(self, a, b, c):
        img0 = self.img
        if not (a == b == c == d == 0):
            cv2.bilateralFilter(img0, a, b, c, infmg_1)
            dst1 = infmg_1 - img0 + 128
            infmg_2 = cv2.GaussianBlur(dst1, (1, 1), 0, 0)
            infmg_3 = img0 + 2 * infmg_2 - 255
            infmg_4 = cv2.addWeighted(img0, 0.2, infmg_3, 0.8, 0)
            img0 = cv2.add(img, infmg_4)  # img是原图，infmg_4是最终滤波的结果
        return img0

    def whiten(self, a):
        img = self.img
        blur_img = cv2.bilateralFilter(img, 31, 75, 75)
        # 图像融合
        result_img = cv2.addWeighted(img, a, blur_img, 1-a, 0)
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

        img = cv2.imread(fileName)
        blur_img = cv2.bilateralFilter(img, 31, 75, 75)
        # 图像融合
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

    def createWindow(self):
        def noting(x):
            pass
        cv2.namedWindow('image')
        cv2.createTrackbar('d', 'image', 0, 50, noting)
        cv2.createTrackbar('sigmaColor', 'image', 0, 255, noting)
        cv2.createTrackbar('sigmaSpace', 'image', 0, 255, noting)
        cv2.createTrackbar('getWhite', 'image', 0, 255, noting)
        a = cv2.getTrackbarPos('d', 'image')
        b = cv2.getTrackbarPos('sigmaColor', 'image')
        c = cv2.getTrackbarPos('sigmaSpace', 'image')
        d = cv2.getTrackbarPos('getWhite', 'image')