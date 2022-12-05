import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance #图像控件
import pandas as pd
import csv
import math
import dlib
import os

cap = cv2.VideoCapture(0) #创建摄像头对象
global history, idx, now, limit, white, skin, face, count, count2, times, twhite, tskin, tface
limit = 100
history = [ [ 0 for i in range (3)] for i in range (limit)]
idx, now, white, skin, face, count, count2, times, twhite, tskin, tface = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def White(img, a):
    img0 = img
    infmg_1 = np.zeros(img.shape, np.uint8)
    infmg_2 = np.zeros(img.shape, np.uint8)
    infmg_3 = np.zeros(img.shape, np.uint8)
    infmg_4 = np.zeros(img.shape, np.uint8)
    if not (a == 0):
        cv2.bilateralFilter(img0, int(a / 10), a, a, infmg_1)
        dst1 = infmg_1 - img0 + 128
        infmg_2 = cv2.GaussianBlur(dst1, (1, 1), 0, 0)
        infmg_3 = img0 + 2 * infmg_2 - 255
        infmg_4 = cv2.addWeighted(img0, 0.2, infmg_3, 0.8, 0)
        img0 = cv2.add(img0, infmg_4)  # img是原图，infmg_4是最终滤波的结果
    return img0

def Skin(img_, a):
    img = img_
    blur_img = cv2.bilateralFilter(img, 31, a, a)
    # 图像融合
    # result_img = cv2.addWeighted(img, a, blur_img, 1-a, 0)
    # cv2.imwrite("58_1.jpg", result_img)
    img_1 = cv2.addWeighted(img, 0.5, blur_img, 0.5, 0)
    # image = Image.open("58_1.jpg")
    # 锐度调节
    img_mid = Image.fromarray(cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB))
    enh_img = ImageEnhance.Sharpness(img_mid)
    image_sharped = enh_img.enhance(1.5)
    # 对比度调节
    con_img = ImageEnhance.Contrast(image_sharped)
    image_con = con_img.enhance(1.15)
    image_res = np.array(image_con)
    image_res = cv2.cvtColor(image_res, cv2.COLOR_RGB2BGR)
    return image_res

predictor_path='./shape_predictor_68_face_landmarks.dat'

#使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
def landmark_dec_dlib_fun(img_src):
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

    land_marks = []

    rects = detector(img_gray, 0)

    for i in range(len(rects)):
        land_marks_node = np.matrix([[p.x, p.y] for p in predictor(img_gray, rects[i]).parts()])
        # for idx,point in enumerate(land_marks_node):
        #     # 68点坐标
        #     pos = (point[0,0],point[0,1])
        #     print(idx,pos)
        #     # 利用cv2.circle给每个特征点画一个圈，共68个
        #     cv2.circle(img_src, pos, 5, color=(0, 255, 0))
        #     # 利用cv2.putText输出1-68
        #     font = cv2.FONT_HERSHEY_SIMPLEX
        #     cv2.putText(img_src, str(idx + 1), pos, font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        land_marks.append(land_marks_node)

    return land_marks


# Interactive Image Warping 局部平移算法
def localTranslationWarp(srcImg, startX, startY, endX, endY, radius):
    ddradius = float(radius * radius)
    copyImg = np.zeros(srcImg.shape, np.uint8)
    copyImg = srcImg.copy()

    # 计算公式中的|m-c|^2
    ddmc = (endX - startX) * (endX - startX) + (endY - startY) * (endY - startY)
    H, W, C = srcImg.shape
    for i in range(W):
        for j in range(H):
            # 计算该点是否在形变圆的范围之内
            # 优化，第一步，直接判断是会在（startX,startY)的矩阵框中
            if math.fabs(i - startX) > radius and math.fabs(j - startY) > radius:
                continue

            distance = (i - startX) * (i - startX) + (j - startY) * (j - startY)

            if (distance < ddradius):
                # 计算出（i,j）坐标的原坐标
                # 计算公式中右边平方号里的部分
                ratio = (ddradius - distance) / (ddradius - distance + ddmc)
                ratio = ratio * ratio

                # 映射原位置
                UX = i - ratio * (endX - startX)
                UY = j - ratio * (endY - startY)

                # 根据双线性插值法得到UX，UY的值
                value = BilinearInsert(srcImg, UX, UY)
                # 改变当前 i ，j的值
                copyImg[j, i] = value

    return copyImg


# 双线性插值法
def BilinearInsert(src, ux, uy):
    w, h, c = src.shape
    if c == 3:
        x1 = int(ux)
        x2 = x1 + 1
        y1 = int(uy)
        y2 = y1 + 1

        part1 = src[y1, x1].astype(np.float) * (float(x2) - ux) * (float(y2) - uy)
        part2 = src[y1, x2].astype(np.float) * (ux - float(x1)) * (float(y2) - uy)
        part3 = src[y2, x1].astype(np.float) * (float(x2) - ux) * (uy - float(y1))
        part4 = src[y2, x2].astype(np.float) * (ux - float(x1)) * (uy - float(y1))

        insertValue = part1 + part2 + part3 + part4

        return insertValue.astype(np.int8)

# 瘦脸
def Face(_img, face):
    face = face / 150 + 1
    landmarks = landmark_dec_dlib_fun(_img)

    thin_image = _img
    # 如果未检测到人脸关键点，就不进行瘦脸
    if len(landmarks) == 0:
        return _img

    for landmarks_node in landmarks:
        left_landmark = landmarks_node[3]
        left_landmark_down = landmarks_node[5]

        right_landmark = landmarks_node[13]
        right_landmark_down = landmarks_node[15]

        endPt = landmarks_node[30]

        # 计算第4个点到第6个点的距离作为瘦脸距离
        r_left = math.sqrt(
            (left_landmark[0, 0] - left_landmark_down[0, 0]) * (left_landmark[0, 0] - left_landmark_down[0, 0]) +
            (left_landmark[0, 1] - left_landmark_down[0, 1]) * (left_landmark[0, 1] - left_landmark_down[0, 1]))

        # 计算第14个点到第16个点的距离作为瘦脸距离
        r_right = math.sqrt(
            (right_landmark[0, 0] - right_landmark_down[0, 0]) * (right_landmark[0, 0] - right_landmark_down[0, 0]) +
            (right_landmark[0, 1] - right_landmark_down[0, 1]) * (right_landmark[0, 1] - right_landmark_down[0, 1]))

        r_left *= face
        r_right *= face

        # 瘦左边脸
        thin_image = localTranslationWarp(_img, left_landmark[0, 0], left_landmark[0, 1], endPt[0, 0], endPt[0, 1],
                                          r_left)
        # 瘦右边脸
        thin_image = localTranslationWarp(thin_image, right_landmark[0, 0], right_landmark[0, 1], endPt[0, 0],
                                          endPt[0, 1], r_right)
    return thin_image

def process(src):
  global times, history, idx, now, white, skin, face
  if times == 0 and not os.path.exists('./default.csv'):  #首次使用，赋予一定初始值
    white = 25
    skin = 25
    face = 25
    scale1.set(white)
    scale2.set(skin)
    scale3.set(face)
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face
    times = 1
  elif times == 0 and os.path.exists('./default.csv'):
    df = pd.read_csv('./default.csv')
    white = df.iat[0, 0]
    skin = df.iat[1, 0]
    face = df.iat[2, 0]
    scale1.set(white)
    scale2.set(skin)
    scale3.set(face)
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face
    times = 1
  dst = src
  # TODO
  # 美白  use white
  dst = White(dst, white)

  # 磨皮  use skin
  dst = Skin(dst, skin)

  # 修脸  use face
  #dst = Face(dst, face)

  return dst

# 关闭美颜状态
def close():
  global count, twhite, tskin, tface, white, skin, face
  if count == 0:
    twhite = white
    tskin = skin
    tface = face
    white = 0
    skin = 0
    face = 0
    scale1.set(0)
    scale2.set(0)
    scale3.set(0)
    button1.configure(image=imgclose2)
    button2.configure(state='disabled', image=imgleft2)
    button3.configure(state='disabled', image=imgright2)
    label_hint.place(x=490, y=0)
  elif count == 1:
    white = twhite
    skin = tskin
    face = tface
    scale1.set(white)
    scale2.set(skin)
    scale3.set(face)
    button1.configure(image=imgclose)
    button2.configure(state='normal', image=imgleft1)
    button3.configure(state='normal', image=imgright1)
    label_hint.place_forget()
  count = 1 - count

# 撤销
def undo():
  global history, idx, now, white, skin, face
  if now > 0:
    now -= 1
    white = history[now][0]
    skin = history[now][1]
    face = history[now][2]
    scale1.set(white)
    scale2.set(skin)
    scale3.set(face)

# 重做
def redo():
  global history, idx, now, white, skin, face
  if now < idx:
    now += 1
    white = history[now][0]
    skin = history[now][1]
    face = history[now][2]
    scale1.set(white)
    scale2.set(skin)
    scale3.set(face)

# 一键美颜
def quick():
  global history, idx, now, white, skin, face
  df = pd.read_csv('./default.csv')
  white = df.iat[0, 0]
  skin = df.iat[1, 0]
  face = df.iat[2, 0]
  scale1.set(white)
  scale2.set(skin)
  scale3.set(face)
  if now != idx:
    idx = now
  idx += 1
  now += 1
  history[idx][0] = white
  history[idx][1] = skin
  history[idx][2] = face

# 重置
def reset():
  global history, idx, now, white, skin, face
  white = 0
  skin = 0
  face = 0
  scale1.set(white)
  scale2.set(skin)
  scale3.set(face)
  if now != idx:
    idx = now
  idx += 1
  now += 1
  history[idx][0] = white
  history[idx][1] = skin
  history[idx][2] = face

# 保存照片
def save():
  global frame_
  root = tk.Tk()
  root.withdraw()
  fname = filedialog.asksaveasfilename(title=u'保存照片', filetypes=[(".png", "PNG"),])
  cv2.imwrite(str(fname)+'.png', frame_)
  df = pd.DataFrame([white, skin, face])
  df.to_csv('./default.csv', index=False)

# 绑定鼠标事件
def get_values1(event):
  global white, history, idx, now
  temp = white
  white = scale1.get()
  if temp != white:
    if now != idx:
      idx = now
    idx += 1
    now += 1
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face
  return white

def get_values2(event):
  global skin, history, idx, now
  temp = skin
  skin = scale2.get()
  if temp != skin:
    if now != idx:
      idx = now
    idx += 1
    now += 1
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face
  return skin

def get_values3(event):
  global face, history, idx, now
  temp = face
  face = scale3.get()
  if temp != face:
    if now != idx:
      idx = now
    idx += 1
    now += 1
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face
  return face

def wheel1(event):
  if event.delta > 0:
    scale1.set(scale1.get()+10)
  else:
    scale1.set(scale1.get()-10)
  global white, history, idx, now
  temp = white
  white = scale1.get()
  if temp != white:
    if now != idx:
      idx = now
    idx += 1
    now += 1
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face
  

def wheel2(event):
  if event.delta > 0:
    scale2.set(scale2.get()+10)
  else:
    scale2.set(scale2.get()-10)
  global skin, history, idx, now
  temp = skin
  skin = scale2.get()
  if temp != skin:
    if now != idx:
      idx = now
    idx += 1
    now += 1
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face

def wheel3(event):
  if event.delta > 0:
    scale3.set(scale3.get()+10)
  else:
    scale3.set(scale3.get()-10)
  global face, history, idx, now
  temp = face
  face = scale3.get()
  if temp != face:
    if now != idx:
      idx = now
    idx += 1
    now += 1
    history[idx][0] = white
    history[idx][1] = skin
    history[idx][2] = face

#对该控件的定义
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()+30
        y = y + cy + self.widget.winfo_rooty()+30
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text,justify=LEFT,
                      background="white", relief=SOLID, borderwidth=1,
                      font=("黑体", "15"))
        label.pack(side=BOTTOM)
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# 界面画布更新图像
def tkImage():
    ref, frame = cap.read()

    if ref is False:  # 开启摄像头失败
    	# 打印报错
        print('read video error')
      # 退出程序
      # exit(0)
    global frame_
    frame = cv2.flip(frame, 1) # 摄像头翻转
    frame_ = process(frame)
    cvimage = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGBA)
    pilImage = Image.fromarray(np.uint8(cvimage))
    pilImage = pilImage.resize((image_width, image_height), Image.ANTIALIAS)
    tkImage =  ImageTk.PhotoImage(image=pilImage)
    return tkImage

top = tk.Tk()
top.title('美颜')
top.geometry('602x800')
top.configure(bg='lightcyan')
image_width = 600
image_height = 480
canvas = Canvas(top, bg='lightcyan', width=image_width, height=image_height)  # 绘制画布
canvas.place(x=0, y=20)

label_hint = Label(top, text='当前美颜已关闭！', font=("黑体", 10), bg='lightcyan', width=15, height=1)
label_hint.place(x=490, y=0)
label_hint.place_forget()


img1=PhotoImage(file='./img/btn.png')
img2=PhotoImage(file='./img/btn2.png')
img3=PhotoImage(file='./img/btn3.png')
imgsave=PhotoImage(file='./img/saveimage.png')
imgclose=PhotoImage(file='./img/close.png')
imgclose2=PhotoImage(file='./img/close2.png')
imgreset=PhotoImage(file='./img/reset.png')
imgleft1=PhotoImage(file='./img/left1.png')
imgleft2=PhotoImage(file='./img/left2.png')
imgright1=PhotoImage(file='./img/right1.png')
imgright2=PhotoImage(file='./img/right2.png')

button1 = Button(top, font=14, image=imgclose, compound='center', command=lambda:close()) 
button1.place(x=60, y=750)
button1.configure(relief='flat', bd=0, bg='lightcyan', activebackground='lightcyan')
CreateToolTip(button1, '暂时关闭/开启')

button2 = Button(top, font=14, image=imgleft1, compound='center', command=lambda:undo())
button2.place(x=120, y=750)
button2.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button2, '撤销')

button3 = Button(top, font=14, image=imgright1, compound='center', command=lambda:redo())
button3.place(x=180, y=750)
button3.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button3, '重做')

button5 = Button(top, text='✨', font=14, image=img1, compound='center', command=lambda:quick())
button5.place(x=420, y=750)
button5.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button5, '一键美颜')

button6 = Button(top, font=14, image=imgreset, compound='center', command=lambda:reset())
button6.place(x=480, y=750)
button6.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button6, '重置')

button7 = Button(top, font=14, image=imgsave, compound='center', command=lambda:save())
button7.place(x=540, y=750)
button7.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button7, '保存')

label1 = Label(top, text='美白', font=("黑体", 14), bg='lightcyan', width=6, height=1).place(x=0, y=545)
white_ = tk.IntVar()
scale1 = Scale(top, variable=white_, bg='lightcyan', length=520, from_=0, to=100, orient='horizontal', tickinterval=50, resolution=1)
scale1.place(x=60, y=525, anchor='nw')
scale1.set(0)
scale1.bind('<ButtonRelease-1>', get_values1)
scale1.bind('<MouseWheel>', wheel1)

label2 = Label(top, text='磨皮', font=("黑体", 14), bg='lightcyan', width=6, height=1).place(x=0, y=620)
skin_ = tk.IntVar()
scale2 = Scale(top, variable=skin_, bg='lightcyan', length=520, from_=0, to=100, orient='horizontal', tickinterval=50, resolution=1)
scale2.place(x=60, y=600, anchor='nw')
scale2.set(0)
scale2.bind('<ButtonRelease-1>', get_values2)
scale2.bind('<MouseWheel>', wheel2)

label3 = Label(top, text='修脸', font=("黑体", 14), bg='lightcyan', width=6, height=1).place(x=0, y=695)
face_ = tk.IntVar()
scale3 = Scale(top, variable=face_, bg='lightcyan', length=520, from_=0, to=100, orient='horizontal', tickinterval=50, resolution=1)
scale3.place(x=60, y=675, anchor='nw')
scale3.set(0)
scale3.bind('<ButtonRelease-1>', get_values3)
scale3.bind('<MouseWheel>', wheel3)


while True:
  pic = tkImage()
  canvas.create_image(0, 0, anchor='nw', image=pic)
  top.update()
  top.after(1)

cap.release()
top.mainloop()

