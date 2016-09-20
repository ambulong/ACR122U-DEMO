#coding:utf-8
from Tkinter import *
import time
import tkFont
import tkMessageBox
import subprocess

#获取余额
def getBalance():
   try:
	   p = subprocess.Popen('python ../getbalance.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	   #print p.stdout.readlines()
	   for line in p.stdout.readlines():
	       print line
	       if(line.find('Balance:') == 0):
		   return line.replace('Balance: ','').replace("\n",'')
	   return 0
   except(ValueError): 
   	return -1

#设置显示余额
def setBalance():
   global balance
   global root
   balance.set(getBalance())
   root.after(1000, setBalance)

#消费
def costBalance():
   global cost
   try:
   	c = float(cost.get())
   except(ValueError): 
	tkMessageBox.showinfo( "提示", "请输入数字")
	cost.set("0")
	return
   try:
	   p = subprocess.Popen('python ../cost.py '+c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	   #print p.stdout.readlines()
	   for line in p.stdout.readlines():
	       print line
	       if(line.find('Balance:') == 0):
		   setBalance()
		   cost.set(c)
		   return
	   tkMessageBox.showinfo( "提示", "扣款失败")
   except(ValueError): 
   	return 0

#消费成功
def success():
   tkMessageBox.showinfo( "提示", "扣款成功")
   global cost
   cost.set("0")

#消费失败
def failed():
   tkMessageBox.showinfo( "提示", "扣款失败")

root = Tk()
root.title("智能卡演示")
root.geometry('250x105')
root.resizable(width=False, height=False)

root.after(1000, setBalance)

label2 = Label( root, text=" 当前余额：", relief=FLAT,  font=tkFont.Font(size=13) )
label2.grid(row=0)

balance = StringVar()
label = Label( root, textvariable=balance, relief=FLAT,  font=tkFont.Font(size=13) )
balance.set("0")
label.grid(row=0, column=1)

label2 = Label( root, text=" 本次消费：", relief=FLAT,  font=tkFont.Font(size=13) )
label2.grid(row=1)

cost = StringVar()
entry = Entry(root, textvariable = cost)
cost.set("0")
entry.grid(row=1, column=1)

label2 = Label( root, text=" ", relief=FLAT, font = tkFont.Font(size=13) )
label2.grid(row=2)

button = Button(root, text ="确认扣款", command = costBalance, font=tkFont.Font(size=10))
button.grid(row=2, column=1)

root.mainloop()
