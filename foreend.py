import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk #图像控件

cap = cv2.VideoCapture(0) #创建摄像头对象

def process(src):
  dst = src
  # TODO
  # 美白  use white

  # 磨皮  use skin

  # 修脸  use face
  return dst

# TODO
# 返回默认状态
def back():
  pass

# 撤销
def undo():
  pass

# 重做
def redo():
  pass

# 与原图对比
def compare():
  pass

# 一键美颜
def quick():
  pass

# 重置
def reset():
  pass

# 保存照片
def save():
  pass

# 绑定鼠标事件
def get_values1(event):
  global white
  white = scale1.get()
  return white

def get_values2(event):
  global skin
  skin = scale2.get()
  return skin

def get_values3(event):
  global face
  face = scale3.get()
  return face

# 界面画布更新图像
def tkImage():
    ref, frame=cap.read()

    if ref is False:  # 开启摄像头失败
    	# 打印报错
        print('read video error')
        # 退出程序
        exit(0)
    
    frame = cv2.flip(frame, 1) # 摄像头翻转
    frame = process(frame)
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pilImage=Image.fromarray(np.uint8(cvimage))
    pilImage = pilImage.resize((image_width, image_height),Image.ANTIALIAS)
    tkImage =  ImageTk.PhotoImage(image=pilImage)
    return tkImage

top = tk.Tk()
top.title('美颜')
top.geometry('480x800')
image_width = 600
image_height = 480
canvas = Canvas(top, bg='white', width=image_width, height=image_height)#绘制画布
canvas.place(x=0, y=40)

button1 = Button(top, text='x ', font=14, bg='white', command=lambda x:back()).place(x=100, y=0)
button2 = Button(top, text='←', font=14, bg='white', command=lambda x:undo()).place(x=180, y=0)
button3 = Button(top, text='→', font=14, bg='white', command=lambda x:redo()).place(x=260, y=0)
button4 = Button(top, text='⏳', font=14, bg='white', command=lambda x:compare()).place(x=340, y=0)

button5 = Button(top, text='✨', font=14, bg='white', command=lambda x:quick()).place(x=290, y=750)
button6 = Button(top, text='〇', font=14, bg='white', command=lambda x:reset()).place(x=360, y=750)
button7 = Button(top, text='💾', font=14, bg='white', command=lambda x:save()).place(x=430, y=750)


label1 = Label(top, text='美白', font=("黑体", 14), width=6, height=1).place(x=0, y=545)
white = tk.DoubleVar() #美白
scale1 = Scale(top, variable=white, bg='white', length=400, from_=1.0, to=10.0, orient='horizontal', tickinterval=10.0, resolution=0.1)
scale1.place(x=60, y=525, anchor='nw')
scale1.set(0)
scale1.bind('<ButtonRelease-1>', get_values1)

label2 = Label(top, text='磨皮', font=("黑体", 14), width=6, height=1).place(x=0, y=620)
skin = tk.DoubleVar() #磨皮
scale2 = Scale(top, variable=skin, bg='white', length=400, from_=1.0, to=10.0, orient='horizontal', tickinterval=10.0, resolution=0.1)
scale2.place(x=60, y=600, anchor='nw')
scale2.set(0)
scale2.bind('<ButtonRelease-1>', get_values2)

label3 = Label(top, text='修脸', font=("黑体", 14), width=6, height=1).place(x=0, y=695)
face = tk.DoubleVar() #修脸
scale3 = Scale(top, variable=face, bg='white', length=400, from_=1.0, to=10.0, orient='horizontal', tickinterval=10.0, resolution=0.1)
scale3.place(x=60, y=675, anchor='nw')
scale3.set(0)
scale3.bind('<ButtonRelease-1>', get_values3)


while True:
  pic = tkImage()
  canvas.create_image(0, 0, anchor = 'nw', image = pic)
  top.update()
  top.after(1)

cap.release()
top.mainloop()

