# 删掉了与原图对比，与暂时关闭美颜功能重复，且长按功能在电脑操作不是很方便
# 关闭美颜状态后，不可使用撤销和重做

import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk #图像控件
import pandas as pd
import csv
import os

cap = cv2.VideoCapture(0) #创建摄像头对象
global history, idx, now, limit, white, skin, face, count, count2, times
limit = 100
history = [ [ 0 for i in range (3)] for i in range (limit)]
idx, now, white, skin, face, count, count2, times = 0, 0, 0, 0, 0, 0, 0, 0

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

  # 磨皮  use skin

  # 修脸  use face
  return dst

# 关闭美颜状态
def close():
  global count
  if count == 0:
    scale1.set(0)
    scale2.set(0)
    scale3.set(0)
    button1.configure(image=img2)
    button2.configure(state='disabled', image=img3)
    button3.configure(state='disabled', image=img3)
    label_hint.place(x=490, y=0)
  elif count == 1:
    scale1.set(white)
    scale2.set(skin)
    scale3.set(face)
    button1.configure(image=img1)
    button2.configure(state='normal', image=img1)
    button3.configure(state='normal', image=img1)
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
    scale1.set(scale1.get()+1)
  else:
    scale1.set(scale1.get()-1)

def wheel2(event):
  if event.delta > 0:
    scale2.set(scale2.get()+1)
  else:
    scale2.set(scale2.get()-1)

def wheel3(event):
  if event.delta > 0:
    scale3.set(scale3.get()+1)
  else:
    scale3.set(scale3.get()-1)

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
button1 = Button(top, text='×', font=14, image=img1, compound='center', command=lambda:close()) 
button1.place(x=60, y=750)
button1.configure(relief='flat', bd=0, bg='lightcyan', activebackground='lightcyan')
CreateToolTip(button1, '暂时关闭/开启')

button2 = Button(top, text='←', font=14, image=img1, compound='center', command=lambda:undo())
button2.place(x=120, y=750)
button2.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button2, '撤销')

button3 = Button(top, text='→', font=14, image=img1, compound='center', command=lambda:redo())
button3.place(x=180, y=750)
button3.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button3, '重做')

button5 = Button(top, text='✨', font=14, image=img1, compound='center', command=lambda:quick())
button5.place(x=420, y=750)
button5.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button5, '一键美颜')

button6 = Button(top, text='🗑', font=14, image=img1, compound='center', command=lambda:reset())
button6.place(x=480, y=750)
button6.configure(relief='flat', bd=0, bg=top['bg'], activebackground=top['bg'])
CreateToolTip(button6, '重置')

button7 = Button(top, text='💾', font=14, image=img1, compound='center', command=lambda:save())
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

