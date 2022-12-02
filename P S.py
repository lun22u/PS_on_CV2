import cv2
import numpy as np
from PIL import Image, ImageEnhance


class photo(object):

    def __init__(self, path):
        self.img = cv2.imread(path)
        self.img_now = self.img
        self.history = {}

    def lighten(self, a, b, c):
        img0 = self.img_now
        infmg_1 = np.zeros(self.img.shape, np.uint8)
        infmg_2 = np.zeros(self.img.shape, np.uint8)
        infmg_3 = np.zeros(self.img.shape, np.uint8)
        infmg_4 = np.zeros(self.img.shape, np.uint8)
        if not (a == b == c == 0):
            cv2.bilateralFilter(img0, a, b, c, infmg_1)
            dst1 = infmg_1 - img0 + 128
            infmg_2 = cv2.GaussianBlur(dst1, (1, 1), 0, 0)
            infmg_3 = img0 + 2 * infmg_2 - 255
            infmg_4 = cv2.addWeighted(img0, 0.2, infmg_3, 0.8, 0)
            img0 = cv2.add(self.img_now, infmg_4)  # img是原图，infmg_4是最终滤波的结果
        return img0

    def whiten(self, a):
        img = self.img_now
        blur_img = cv2.bilateralFilter(img, 31, 75, 75)
        # 图像融合
        # result_img = cv2.addWeighted(img, a, blur_img, 1-a, 0)
        # cv2.imwrite("58_1.jpg", result_img)
        img_1 = cv2.addWeighted(img, a, blur_img, 1-a, 0)
        # image = Image.open("58_1.jpg")
        # 锐度调节
        enh_img = ImageEnhance.Sharpness(img_1)
        image_sharped = enh_img.enhance(1.5)
        # 对比度调节
        con_img = ImageEnhance.Contrast(image_sharped)
        image_con = con_img.enhance(1.15)
        return image_con


    def createWindow(self):
        his = 1
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
        while 1:
            a2 = cv2.getTrackbarPos('d', 'image')
            b2 = cv2.getTrackbarPos('sigmaColor', 'image')
            c2 = cv2.getTrackbarPos('sigmaSpace', 'image')
            d2 = cv2.getTrackbarPos('getWhite', 'image')
            if a2 != a or b2 != b or c2 != c or d2 != d:
                if a2 != a or b2 != b or c2 != c:
                    self.img_now = self.lighten(a2, b2, c2)
                if d2 != d:
                    self.img_now = self.whiten(d2)
                self.history[his] = [a2, b2, c2, d2]
                a = a2, b = b2, c = c2, d = d2
            cv2.imshow('ori', self.img)
            cv2.imwrite("res.jpg", self.img_now)


test = photo('test.png')
test.createWindow()
