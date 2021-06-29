# This Python file uses the following encoding: utf-8
import tkinter as tk
import time
from fcts import*
import os


pT=tk.Tk()

pT.attributes("-topmost",1)
pT.geometry("+%d+%d"%(0,0))
#pT.geometry("340x120")
pT.wm_overrideredirect(1) # hier wird der Windows-Fensterrahmen ausgeschaltet
pT.resizable(0, 0) #Don't allow resizing in the x or y direction
pT.configure(bg="gray")


#Labels
labelWorkTime=tk.Label(pT,text="0h 00min", bg="gray", font=("times",10))
labelWorkTime.grid(row=2, rowspan=3, column=24, columnspan=9,sticky="NW")

labelTaskTime=tk.Label(pT,text="0h 00min",bg="gray", font=("times",10))
labelTaskTime.grid(row=6,rowspan=3, column=24, columnspan=9,sticky="NW")

inputTimeNextAlarm=tk.Entry(pT,width=3)
labelNextAlarm=tk.Label(pT,text="min bis ", bg="gray", font=("times",10))
inputNextAlarm=tk.Entry(pT)

addErinnerungen()
nextAlarmArr=getNextAlarm()

nextAlarm=nextAlarmArr[0]

nextAlarmName=nextAlarmArr[1]
curSeconds=time.mktime(time.localtime())
nextAlarmSeconds=time.mktime(nextAlarm)

timerNextAlarm=int((nextAlarmSeconds-curSeconds)/60)+1 #+1 weil direkt im Anschluss Timer ausgeführt wird, wo die variabele um 1 reduziert wird


labelActiveAlarm=tk.Label(pT,text="Noch "+str(timerNextAlarm)+"min bis "+nextAlarmName, bg="gray", font=("times",10))
labelActiveAlarm.grid(row=10,rowspan=3, column=0, columnspan=32,sticky="NW")

zeit=time.strftime("%H:%M",time.localtime())
labelTime=tk.Label(pT,text=zeit,width=5,fg="black",bg="gray",font=("times",25,"bold"),compound=tk.CENTER)
labelTime.grid(row=2,rowspan=7,column=8,columnspan=14, sticky="NW")
addAlarmButton=tk.Button(pT,text="+",command=lambda:addAlarm(addAlarmButton,labelNextAlarm,alarmButton,inputTimeNextAlarm,inputNextAlarm,labelActiveAlarm))

#Buttons
hideButton=tk.Button(pT,text="Hide",command=lambda:hideWindow(pT,hideButton))
hideButton.grid(row=0, rowspan=4,column=50,columnspan=6, sticky="NW")

closeButton=tk.Button(pT,text="X",command=lambda:close(pT))
closeButton.grid(row=0, rowspan=4,column=56,columnspan=3, sticky="NW")



menuActive=0
menuButton=tk.Button(pT,text="Menü",command=lambda:menuClick(pT))
menuButton.grid(row=0, rowspan=4,column=0, columnspan=7, sticky="NW")

state="off"
logButton=tk.Button(pT,text="Einloggen",height=1, width=10, command=lambda:log(logButton,taskMenu,labelTime,labelWorkTime, labelTaskTime,breakButton))
logButton.grid(row=2, rowspan=5,column=34,columnspan=14,sticky="NW")

breakButton=tk.Button(pT,text="Kurzpause",state=tk.DISABLED, command=lambda:shortBreak(breakButton,logButton,taskMenu,labelTime))
breakButton.grid(row=13,rowspan=4, column=34,columnspan=14,sticky="NW")

cur_path = os.path.dirname(__file__)
config=open(cur_path+"\config.txt","r")
taskList=[""]
for zeile in config:
    if (zeile[0:8]=="projekte"):
        zeile=zeile.replace("\n","")
        tasks=zeile.split(";")
        if (len(tasks)>1):
            taskList=tasks[1:len(tasks)]

task=tk.StringVar(pT)
task.set(taskList[0])
taskMenu=tk.OptionMenu(pT,task, *taskList)
passarg=[logButton,labelTime,breakButton,labelTaskTime,task,taskMenu]
task.trace("w",lambda *args, passed=passarg:changeTask(passed,*args)) # Ruft die Funktion changeTask auf, wenn die varieable Task geändert wird (w=wirte)
taskMenu.configure(height=1);
taskMenu.configure(width=14);
taskMenu.configure(anchor="w")
taskMenu.grid(row=8,rowspan=4,column=34 ,columnspan=23, sticky="NW")

alarmButton=tk.Button(pT, text="Neuen Alarm hinzufügen", command=lambda:newAlarm(labelActiveAlarm,addAlarmButton,inputTimeNextAlarm,labelNextAlarm,inputNextAlarm,alarmButton))
alarmButton.grid(row=13,rowspan=4,column=0,  columnspan=23,sticky="NW")

timer(nextAlarmName,labelActiveAlarm,inputTimeNextAlarm,labelWorkTime, labelTaskTime,logButton,breakButton,taskMenu,labelTime)
pT.mainloop()
