import tkinter as tk
import time
from fcts import*
pT=tk.Tk()

pT.attributes("-topmost",1)
pT.geometry("+%d+%d"%(0,0))
pT.geometry("350x130")
pT.wm_overrideredirect(1) # hier wird der Windows-Fensterrahmen ausgeschaltet
pT.resizable(0, 0) #Don't allow resizing in the x or y direction
pT.configure(bg="gray")


#Labels
labelWorkTime=tk.Label(pT,text="0h 00min", bg="gray", font=("times",10))
labelWorkTime.grid(row=20, rowspan=20, column=30, sticky="W")

labelTaskTime=tk.Label(pT,text="0h 00min",bg="gray", font=("times",10))
labelTaskTime.grid(row=40,rowspan=20, column=30,sticky="W")

labelNextAlarm=tk.Label(pT,text="30min bis Termin", bg="gray", font=("times",10))
labelNextAlarm.grid(row=50,rowspan=20,column=0, columnspan=30,sticky="W")

labelAlarm=tk.Label(pT,text="Wecker hinzufügen",bg="gray", font=("times",10))
labelAlarm.grid(row=80,rowspan=20,column=10, columnspan=30,sticky="W")


zeit=time.strftime("%H:%M:%S",time.localtime())
labelTime=tk.Label(pT,text=zeit,fg="black",bg="gray",font=("times",25,"bold"),compound=tk.CENTER)
labelTime.grid(row=20,rowspan=30,column=10,columnspan=20, sticky="NW")


#Buttons
closeButton=tk.Button(pT,text="X",command=lambda:close(pT))
closeButton.grid(row=0,column=70,columnspan=5, rowspan=20)

menuActive=0
menuButton=tk.Button(pT,text="Menü",command=lambda:menuClick(pT))
menuButton.grid(row=0, rowspan=20,column=0, columnspan=20, sticky="W")

state="off"
logButton=tk.Button(pT,text="Einloggen",command=lambda:log(logButton,taskMenu,labelTime,labelWorkTime, labelTaskTime,breakButton))
logButton.grid(row=10, rowspan=20,column=50,columnspan=20,sticky="W")

breakButton=tk.Button(pT,text="Kurzpause",state=tk.DISABLED, command=lambda:shortBreak(breakButton,logButton,taskMenu,labelTime))
breakButton.grid(row=70,rowspan=20, column=50,columnspan=20,sticky="W")

taskList=["Aufgabe wählen","Task1","Task2","Task3"]
task=tk.StringVar(pT)
task.set(taskList[0])
taskMenu=tk.OptionMenu(pT,task, *taskList)
passarg=[logButton,labelTime,breakButton,labelTaskTime,task,taskMenu]
task.trace("w",lambda *args, passed=passarg:changeTask(passed,*args)) # Ruft die Funktion changeTask auf, wenn die varieable Task geändert wird (w=wirte)
taskMenu.grid(row=40,column=50 ,rowspan=10,columnspan=20)

alarmButton=tk.Button(pT,text="+")
alarmButton.grid(row=80,column=0, rowspan=2)

timer(labelWorkTime, labelTaskTime,logButton,breakButton,taskMenu,labelTime)
pT.mainloop()
