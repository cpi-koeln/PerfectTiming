# This Python file uses the following encoding: utf-8
import tkinter as tk
import time
from fcts import*
import os
from tkinter.ttk import *


root=tk.Tk()

root.attributes("-topmost",1)
root.geometry("+%d+%d"%(0,0))
#pT.geometry("340x120")
##root.wm_overrideredirect(1) # hier wird der Windows-Fensterrahmen ausgeschaltet
root.resizable(0, 0) #Don't allow resizing in the x or y direction
root.configure(bg="gray")

erinnerungen=addErinnerungentoWecker()
nextAlarmArr=getNextAlarm()



nextAlarmName=nextAlarmArr[1]
curSeconds=time.mktime(time.localtime())
nextAlarmSeconds=nextAlarmArr[0]

timerNextAlarm=int((nextAlarmSeconds-curSeconds)/60)+1 #+1 weil direkt im Anschluss Timer ausgeführt wird, wo die variabele um 1 reduziert wird
zeit=time.strftime("%H:%M",time.localtime())

class mainFrame:
    def __init__(self,parent):
        myFrame=tk.Frame(parent)
        myFrame.grid(row=0,column=0)
        self.parent=parent

        #Labels
        self.labelWorkTime=tk.Label(parent,text="0h 00min", bg="gray", font=("times",10))
        self.labelWorkTime.grid(row=2, rowspan=3, column=24, columnspan=9,sticky="NW")

        self.labelTaskTime=tk.Label(parent,text="0h 00min",bg="gray", font=("times",10))
        self.labelTaskTime.grid(row=6,rowspan=3, column=24, columnspan=9,sticky="NW")

        self.inputTimeNextAlarm=tk.Entry(parent,width=3)
        self.labelNextAlarm=tk.Label(parent,text="min bis ", bg="gray", font=("times",10))
        self.inputNextAlarm=tk.Entry(parent)

        if (timerNextAlarm>100000):
            self.labelActiveAlarm=tk.Label(parent,text="Kein Wecker", bg="gray", font=("times",10))
        else:
            self.labelActiveAlarm=tk.Label(parent,text="Noch "+str(timerNextAlarm)+"min bis "+nextAlarmName, bg="gray", font=("times",10))
        self.labelActiveAlarm.grid(row=10,rowspan=3, column=0, columnspan=32,sticky="NW")

        self.labelTime=tk.Label(parent,text=zeit,width=5,fg="black",bg="gray",font=("times",25,"bold"),compound=tk.CENTER)
        self.labelTime.grid(row=2,rowspan=7,column=8,columnspan=14, sticky="NW")
        self.addAlarmButton=tk.Button(parent,text="+",command=lambda:addAlarm(self))

        #Buttons
        path = os.path.dirname(__file__)
        self.pin=tk.PhotoImage(file=path+'/pin.gif')
        self.pinned=tk.PhotoImage(file=path+'/pinned.gif')
        self.hideButton=tk.Button(parent,image=self.pinned,text="Hide",command=lambda:hideWindow(self), width="20", height="20")
        #self.hideButton.config(, width="15", height="15")
        self.hideButton.grid(row=0, rowspan=4,column=50,columnspan=6, sticky="NW")

        self.arrow=tk.PhotoImage(file=path+'/arrow.gif')
        self.closeButton=tk.Button(parent,image=self.arrow,text="X",command=lambda:slideWindow(root),width="20", height="20")
        self.closeButton.grid(row=0, rowspan=4,column=56,columnspan=3, sticky="NW")

        menuActive=0
        self.menuButton=tk.Button(parent,text="Menü",command=lambda:menuClick(self))
        self.menuButton.grid(row=0, rowspan=4,column=0, columnspan=7, sticky="NW")

        state="off"
        self.logButton=tk.Button(parent,text="Einloggen",height=1, width=10, command=lambda:log(self))
        self.logButton.grid(row=2, rowspan=5,column=34,columnspan=14,sticky="NW")

        self.breakButton=tk.Button(parent,text="Kurzpause",state=tk.DISABLED, command=lambda:shortBreak(self))
        self.breakButton.grid(row=13,rowspan=4, column=34,columnspan=14,sticky="NW")

        cur_path = os.path.dirname(__file__)
        config=open(cur_path+"\config.txt","r")
        taskList=[""]
        for zeile in config:
            if (zeile[0:8]=="projekte"):
                zeile=zeile.replace("\n","")
                tasks=zeile.split(";")
                if (len(tasks)>1):
                    taskList=tasks[1:len(tasks)]

        task=tk.StringVar(parent)
        task.set(taskList[0])
        self.taskMenu=tk.OptionMenu(parent,task, *taskList)
        passarg=[self,task]
        task.trace("w",lambda *args, passed=passarg:changeTask(passed,*args)) # Ruft die Funktion changeTask auf, wenn die varieable Task geändert wird (w=wirte)
        self.taskMenu.configure(height=1);
        self.taskMenu.configure(width=14);
        self.taskMenu.configure(anchor="w")
        self.taskMenu.grid(row=8,rowspan=4,column=34 ,columnspan=23, sticky="NW")
        self.task=task

        self.alarmButton=tk.Button(parent, text="Neuen Alarm hinzufügen", command=lambda:newAlarm(self))
        self.alarmButton.grid(row=13,rowspan=4,column=0,  columnspan=23,sticky="NW")

pT=mainFrame(root)
nextAlarmArr=getNextAlarm()
timer(pT,nextAlarmArr)
root.mainloop()
