#!/usr/bin/env python
# -*- coding: utf-8 -*-
def close(fenster):
    fenster.destroy()
    #menu.attributes("-topmost",0)
    #pT.attributes("-topmost",1)
    try:
            menu.destroy()

    except:
            print("close():Menüfenster ist schon zu")

def closeAlarm(alarmWindow,labelActiveAlarm):
    import time
    alarmWindow.destroy()

    #pT.attributes("-topmost",1)



def timer(nextAlarmName,labelActiveAlarm,inputTimeNextAlarm,labelWorkTime, labelTaskTime,logButton,breakButton,taskMenu,labelTime):
    import time
    import os
    import tkinter as tk
    import beepy as beep

    zeit=time.strftime("%H:%M",time.localtime())
    if(zeit=="00:00"):
            labelWorkTime.config(text="0h 0min")
    labelTime.config(text=zeit)
    #aktivenAlarm runterzählen
    textActiveAlarm=labelActiveAlarm["text"]
    textActiveAlarmArr=textActiveAlarm.split(" ")
    timerNextAlarm=textActiveAlarmArr[1]
    timerNextAlarm=int(timerNextAlarm.replace("min",""))


    if timerNextAlarm>1:
        text=labelActiveAlarm["text"]
        text=text.replace(str(timerNextAlarm),str(timerNextAlarm-1))
        labelActiveAlarm["text"]=text
        timerNextAlarm=timerNextAlarm-1
    else:
        alarmWindow=tk.Tk()
        alarmWindow.attributes("-topmost",1)
        alarmWindow.geometry("+%d+%d"%(500,500))
        alarmWindow.configure(bg="gray")
        alarmLabel=tk.Label(alarmWindow,text=nextAlarmName,font=("times",16))
        alarmLabel.grid(row=0, column=0)
        OkButton=tk.Button(alarmWindow,text="Ok",command=lambda:closeAlarm(alarmWindow,labelActiveAlarm))
        OkButton.grid(row=2, column=0)
        beep.beep(4)
        nextAlarmArr=getNextAlarm()
        nextAlarm=nextAlarmArr[0]
        nextAlarmName=nextAlarmArr[1]
        curSeconds=time.mktime(time.localtime())
        nextAlarmSeconds=time.mktime(nextAlarm)
        timerNextAlarm=int((nextAlarmSeconds-curSeconds)/60)+1 #+1 weil direkt im Anschluss Timer ausgeführt wird, wo die variabele um 1 reduziert wird
        labelActiveAlarm["text"]="Noch "+str(timerNextAlarm)+"min bis "+nextAlarmName


    labelTime.after(60000,lambda:timer(nextAlarmName,labelActiveAlarm,inputTimeNextAlarm,labelWorkTime, labelTaskTime, logButton,breakButton,taskMenu,labelTime)) # müsste auf 60000 gesetzt werden
    state=logButton["text"]
    if(state=="Ausloggen"):
        workTimerString=labelWorkTime["text"]
        positionHour=workTimerString.find("h ")
        workHours=workTimerString[0:positionHour]
        workMinutes=workTimerString[positionHour+2:len(workTimerString)-3]
        resultWorkTime=int(workHours)*60+int(workMinutes)+1 #hier ändern wieviele Minute pro Minute dazugezählt werden
        newHours=resultWorkTime//60
        newMinutes=resultWorkTime%60
        newWorkTimerString=str(newHours)+"h "+str(newMinutes)+"min"
        labelWorkTime.config(text=newWorkTimerString)

        taskTimerString=labelTaskTime["text"]
        positionHour=taskTimerString.find("h ")
        taskHours=taskTimerString[0:positionHour]
        taskMinutes=taskTimerString[positionHour+2:len(taskTimerString)-3]
        resultTaskTime=int(taskHours)*60+int(taskMinutes)+1 #hier ändern wieviele Minute pro Minute dazugezählt werden
        newHours=resultTaskTime//60
        newMinutes=resultTaskTime%60
        newTaskTimerString=str(newHours)+"h "+str(newMinutes)+"min"
        labelTaskTime.config(text=newTaskTimerString)
    if(breakButton["text"]!="Kurzpause"):
        leftTime=breakButton["text"][5:6]
        if(int(leftTime)>1):
            newLeftTime=int(leftTime)-1
            breakButton["text"]="noch "+str(newLeftTime)+"min"
        else:
            breakButton["text"]="Kurzpause"
            log(logButton,taskMenu,labelTime,labelWorkTime, labelTaskTime,breakButton)

    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:8]=="alarmTime"):
            zeileArr=zeile.split(";")
            separator=";"
            zeileNeu=separator.join(zeileArr)
        elif (zeile[0:8]=="alarmName"):
            zeileArr=zeile.split(";")
            separator=";"
            zeileNeu=separator.join(zeileArr)
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()




def log(logButton,taskMenu,labelTime,labelWorkTime, labelTaskTime,breakButton):
    import os
    import time
    import tkinter as tk
    cur_path = os.path.dirname(__file__)
    state=logButton["text"]
    log=open(cur_path+"\log.txt","a")
    logArchiv=open(cur_path+"\logArchiv.txt","a")
    task=taskMenu["text"]
    logDate=time.strftime("%d.%m.%Y",time.localtime())
    logTime=time.strftime("%H:%M:%S",time.localtime())
    if(task=="Aufgabe wählen"):
        task="default"
    if(state=="Einloggen"):
        logButton["text"]="Ausloggen"
        log.write("logIn;"+logDate+";"+logTime+";"+task+"\n")
        logArchiv.write("logIn;"+logDate+";"+logTime+";"+task+"\n")
        labelTime.config(fg="green")
        breakButton["state"]=tk.NORMAL
        if (breakButton["text"]!="Kurzpause"):
            breakButton["text"]="Kurzpause"
    elif(state=="Ausloggen"):
        logButton["text"]="Einloggen"
        log.write("logOut;"+logDate+";"+logTime+";"+task+"\n")
        logArchiv.write("logOut;"+logDate+";"+logTime+";"+task+"\n")
        labelTime.config(fg="black")
        breakButton["state"]=tk.DISABLED
        #labelWorkTime.config(text="0h 0min")
        #labelTaskTime.config(text="0h 0min")
    log.close()
    logArchiv.close()

def shortBreak(breakButton, logButton,taskMenu,labelTime):
    import tkinter as tk
    import os
    import time
    if(breakButton["text"]=="Kurzpause" and logButton["text"]=="Ausloggen"):
        breakButton["state"]=tk.DISABLED
        cur_path = os.path.dirname(__file__)
        log=open(cur_path+"\log.txt","a")
        logDate=time.strftime("%d.%m.%Y",time.localtime())
        logTime=time.strftime("%H:%M:%S",time.localtime())
        task=taskMenu["text"]
        if(task=="Aufgabe wählen"):
            task="default"
        breakButton.config(text="noch 5min")
        logButton["text"]="Einloggen"
        log.write("logOut;"+logDate+";"+logTime+";"+task+"\n")
        labelTime.config(fg="black")
        log.close()

def changeTask(passarg, *args):
    import tkinter as tk
    import os
    import time
    logButton=passarg[0]
    labelTime=passarg[1]
    breakButton=passarg[2]
    labelTaskTime=passarg[3]
    task=passarg[4]
    taskMenu=passarg[5]

    #taskName=task.get()
    if (breakButton["state"]==tk.NORMAL and logButton["text"]=="Ausloggen"):


        cur_path = os.path.dirname(__file__)
        state=logButton["text"]
        log=open(cur_path+"\log.txt","a")
        task=taskMenu["text"]
        logDate=time.strftime("%d.%m.%Y",time.localtime())
        logTime=time.strftime("%H:%M:%S",time.localtime())
        if(task=="Aufgabe wählen"):
            task="default"

        log.write("logOut;"+logDate+";"+logTime+";"+"oldTask"+"\n")
        log.write("logIn;"+logDate+";"+logTime+";"+task+"\n")
        labelTaskTime["text"]="0h 00min"
        log.close()


def test():
    print("test")

def chooseProjekt(passarg,*args):
    import tkinter as tk
    buttonBearbeiten=passarg[0]
    buttonLoeschen=passarg[1]
    buttonBearbeiten["state"]=tk.NORMAL
    buttonLoeschen["state"]=tk.NORMAL

def deleteProjekt(listProjekte):
    import os
    active=listProjekte.get(listProjekte.curselection())
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:8]=="projekte"):
            zeileArr=zeile.split(";")
            zeileArr.remove(active)
            separator=";"
            zeileNeu=separator.join(zeileArr)
            zeileNeu=zeileNeu.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu

    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    listProjekte.delete(0,"end")
    countProjekte=len(zeileArr)
    i=1
    while i<countProjekte:
        listProjekte.insert(i,zeileArr[i])
        i=i+1

def changedProjekt(listProjekte,active,newProjektName,changeWecker):
    import os
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:8]=="projekte"):
            zeileArr=zeile.split(";")
            index=zeileArr.index(active)
            zeileArr[index]=newProjektName.get()
            separator=";"
            zeileNeu=separator.join(zeileArr)
            zeileNeu=zeileNeu.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    listProjekte.delete(0,"end")
    countProjekte=len(zeileArr)
    i=1
    while i<countProjekte:
        listProjekte.insert(i,zeileArr[i])
        i=i+1
    changeWecker.destroy()


def changeProjekt(listProjekte):
    import tkinter as tk
    active=listProjekte.get(listProjekte.curselection())

    changeWecker=tk.Tk()
    changeWecker.title("Neuer Projektname")
    changeWecker.geometry("+%d+%d"%(75,250))
    changeWecker.geometry("250x75")
    changeWecker.attributes("-topmost",1)

    label1=tk.Label(changeWecker,text="Bitte gebe den neuen Projektnamen an:",font=("times",10))
    label1.grid(row=0,column=0,columnspan=2, sticky="W")

    input=tk.Entry(changeWecker)
    input.insert(10,"")
    input.grid(row=1,column=0, sticky="W")

    buttonOK2=tk.Button(changeWecker,text="OK",height=1,width=10, command=lambda:changedProjekt(listProjekte,active,input,changeWecker))
    buttonOK2.grid(row=1,column=1, sticky="W")

def addProjekt(listProjekte,inputNeu):
    import os
    newName=inputNeu.get()
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    zeileArr=[]
    for zeile in config:
        if (zeile[0:8]=="projekte"):
            zeileArr=zeile.split(";")
            zeileArr.append(newName)
            separator=";"
            zeileNeu=separator.join(zeileArr)
            zeileNeu=zeileNeu.replace("\n","")
            zeileNeu=zeileNeu+"\n"

        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    listProjekte.delete(0,"end")
    countProjekte=len(zeileArr)
    i=1
    while i<countProjekte:
        listProjekte.insert(i,zeileArr[i])
        i=i+1

def projekte():
    import tkinter as tk
    from tkinter import ttk
    import os
    menu.destroy()

    projektFenster=tk.Tk()
    projektFenster.title("Projektmenü")
    projektFenster.geometry("+%d+%d"%(100,100))
    projektFenster.geometry("300x200")
    projektFenster.attributes("-topmost",1)

    label1=tk.Label(projektFenster,text="vorhandene Projekte:",font=("times",10))
    label1.grid(row=0,column=0, sticky="W")

    buttonBearbeiten=tk.Button(projektFenster,text="Ändern",width=10,height=1,state=tk.DISABLED, command=lambda:changeProjekt(listProjekte))
    buttonBearbeiten.grid(row=2,column=2, sticky="W")

    buttonLoeschen=tk.Button(projektFenster,text="Löschen",width=10,height=1,state=tk.DISABLED,command=lambda:deleteProjekt(listProjekte))
    buttonLoeschen.grid(row=3,column=2, sticky="W")

    separator=ttk.Separator(projektFenster, orient="horizontal")
    separator.grid(row=4,column=2, sticky="W")

    inputNeu=tk.Entry(projektFenster)
    inputNeu.insert(10,"Neues Projekt")
    inputNeu.grid(row=5,column=2,columnspan=2, sticky="W")

    buttonHinzufuegen=tk.Button(projektFenster,text="Hinzufügen",width=10,height=1,command=lambda:addProjekt(listProjekte,inputNeu))
    buttonHinzufuegen.grid(row=6,column=2, sticky="W")

    buttonOK=tk.Button(projektFenster,text="OK",width=10,height=1,command=lambda:close(projektFenster))
    buttonOK.grid(row=7,column=3, sticky="W")

    listProjekte=tk.Listbox(projektFenster)
    passarg=[buttonBearbeiten,buttonLoeschen]
    listProjekte.bind("<<ListboxSelect>>",lambda *args, passed=passarg:chooseProjekt(passed,*args))
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    for zeile in config:
        if (zeile[0:8]=="projekte"):
            zeileArr=zeile.split(";")
            countProjekte=len(zeileArr)
            i=1
            while i<countProjekte:
                listProjekte.insert(i,zeileArr[i])
                i=i+1
    listProjekte.grid(row=2, rowspan=6, column=0, sticky="W")
    config.close()

def stempeln():
    import tkinter as tk
    import os
    from tkinter import ttk
    import tkcalendar
    from tkcalendar import Calendar, DateEntry
    menu.destroy()


    stempelFenster=tk.Tk()
    stempelFenster.title("Stempeln")
    stempelFenster.geometry("+%d+%d"%(100,100))
    stempelFenster.geometry("350x120")
    stempelFenster.attributes("-topmost",1)

    label1=tk.Label(stempelFenster,text="LogIn",font=("times",10))
    label1.grid(row=5,column=0, sticky="W")

    label2=tk.Label(stempelFenster,text="LogOut",font=("times",10))
    label2.grid(row=10,column=0, sticky="W")

    dateLogIn = DateEntry(stempelFenster,date_pattern="dd.MM.yyyy", width=10,bg="darkblue",fg="white",year=2021)
    dateLogIn.grid(row=5,column=1)

    dateLogOut = DateEntry(stempelFenster,date_pattern="dd.MM.yyyy", width=10,bg="darkblue",fg="white",year=2021)
    dateLogOut.grid(row=10,column=1)

    timeLogIn=tk.Entry(stempelFenster)
    timeLogIn.insert(10,"hh:mm")
    timeLogIn.grid(row=5,column=2,columnspan=2, sticky="W")

    timeLogOut=tk.Entry(stempelFenster)
    timeLogOut.insert(10,"hh:mm")
    timeLogOut.grid(row=10,column=2,columnspan=2, sticky="W")

    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    for zeile in config:
        if (zeile[0:8]=="projekte"):
            tasks=zeile.split(";")
            taskList=tasks[1:len(tasks)]
    config.close()


    #taskList=["Aufgabe wählen","Task1","Task2","Task3"]
    task1=tk.StringVar(stempelFenster)
    task1.set(taskList[0])
    task2=tk.StringVar(stempelFenster)
    task2.set(taskList[0])

    taskLogIn=tk.OptionMenu(stempelFenster,task1, *taskList)
    taskLogIn.configure(height=1);
    taskLogIn.configure(width=14);
    taskLogIn.configure(anchor="w")
    taskLogIn.grid(row=5,column=3 , sticky="W")

    taskLogOut=tk.OptionMenu(stempelFenster,task2, *taskList)
    taskLogOut.configure(height=1);
    taskLogOut.configure(width=14);
    taskLogOut.configure(anchor="w")
    taskLogOut.grid(row=10,column=3 , sticky="W")

    #task.trace("w") # Ruft die Funktion changeTask auf, wenn die varieable Task geändert wird (w=wirte)



    buttonHinzufuegen=tk.Button(stempelFenster,text="Hinzufügen",width=10,height=1,command=lambda:addStempel(stempelFenster,dateLogIn,dateLogOut,timeLogIn,timeLogOut,taskLogIn,taskLogOut))
    buttonHinzufuegen.grid(row=15,column=2, sticky="W")

def addStempel(stempelFenster,dateLogIn,dateLogOut,timeLogIn,timeLogOut,taskLogIn,taskLogOut):
    import os
    cur_path = os.path.dirname(__file__)
    log=open(cur_path+"\log.txt","a")

    if(timeLogIn.get()!="hh:mm"):
        logDate=str(dateLogIn.get_date())
        logTime=str(timeLogIn.get())+":00"
        task=taskLogIn["text"]
        log.write("logIn;"+logDate+";"+logTime+";"+task)

    if(timeLogOut.get()!="hh:mm"):
        logDate=str(dateLogOut.get_date())
        logTime=str(timeLogOut.get())+":00"
        task=taskLogOut["text"]
        log.write("logOut;"+logDate+";"+logTime+";"+task)
    stempelFenster.destroy()
    log.close()




def auswertung(menu):
    import os
    import time
    import openpyxl

    path = os.path.dirname(__file__)+"\Auswertung.xlsm"
    pathLocal = os.path.dirname(__file__)

    excel = openpyxl.load_workbook(path,read_only=False, keep_vba= True)#to open the excel sheet and if it has macros
    config = excel.get_sheet_by_name('config')#get sheetname from the file
    config['AZ1']= str(pathLocal) #write something in B2 cell of the supplied sheet
    excel.save(path)#save it as a new file, the original file is untouched and here I am saving it as xlsm(m here denotes macros).

    menu.destroy()
    os.startfile(path)
    log=os.path.dirname(__file__)+"\log.txt"
    time.sleep(60)
    open(log, 'w').close()


def menuClick(pT):
    import tkinter as tk
    global menuActive, menu
    try:
            menu.destroy()
            #pT.attributes("-topmost",1)
    except:
        menuActive=1
        menu=tk.Tk()
        menu.geometry("+%d+%d"%(0,20))
        menu.geometry("94x130")
        menu.wm_overrideredirect(1) # hier wird der Windows-Fensterrahmen ausgeschaltet
        menu.resizable(0, 0) #Don't allow resizing in the x or y direction
        #pT.attributes("-topmost",0)
        menu.attributes("-topmost",1)

        projektButton=tk.Button(menu,text="Projekte",width=12,height=1, command=lambda:projekte())
        projektButton.grid(row=1,column=0)
        stempelButton=tk.Button(menu,text="Stempeln",width=12,height=1,command=lambda:stempeln())
        stempelButton.grid(row=2,column=0)
        weckerButton=tk.Button(menu,text="Wecker",width=12,height=1,command=lambda:weckerMenu())
        weckerButton.grid(row=3,column=0)
        einstellungButton=tk.Button(menu,text="Einstellungen",state=tk.DISABLED,width=12,height=1,command=lambda:test())
        einstellungButton.grid(row=4,column=0)
        auswertungButton=tk.Button(menu,text="Auswertung",width=12,height=1,command=lambda:auswertung(menu))
        auswertungButton.grid(row=5,column=0)






def addErinnerungen(): # Startet zu Beginndes Programms und schiebt aktive Erinnerungen mit Countdownfunktion in Weckerliste
    print("addErinnerungen")
    import os
    import time as tm

    curDateTime=tm.strftime("%d.%m.%Y %H:%M",tm.localtime())
    curDateTime=tm.strptime(curDateTime,"%d.%m.%Y %H:%M")

    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    newWecker=[]
    newErinnerungen=[]
    for zeile in config:
        if (zeile[0:10]=="erinnerung"):
            erinnerungen=zeile.split(";")
            countErinnerungen=len(erinnerungen)
            i=1
            while i<countErinnerungen:
                erinnerung=erinnerungen[i].split(",")
                if (erinnerung[3]=="ja"):
                    if (erinnerung[4]=="ja"):
                        newDateTimeSec=tm.mkTime(curDateTime)
                        newDateTimeSec=newDateTime+120*60
                        newDateTime=tm.localtime(newDateTimeSec)
                        newDate=tm.strptime(newDateTime,"%d.%m.%Y")
                        newTime=tm.strptime(newDateTime,"%H:%M")
                        wecker=[str(newDate),str(newTime),erinnerung[0],""]
                        separator=","
                        newWecker.append(separator.join(wecker))

                    newErinnerungen.append(erinnerung)
                i=i+1
        elif(zeile[0:5]=="alarm"):
            alarms=zeile
        else:

        print("config wecker aktualisieren")
        config=open(cur_path+"\config.txt","r")
        configNeu=""
        newWecker=[]
        newErinnerungen=[]
        for zeile in config:
            if (zeile[0:10]=="erinnerung"):
                erinnerungen=zeile.split(";")


    config.close()



########--------Funktionen zuer Weckerbearbeitung------------------


def changedWecker(tableWecker,changeWecker,inputName,serie,datum,inputZeitraum,timeMenu,inputZeit):
    import os
    import time as tm
    alarmName=inputName.get()
    alarmDatum=datum.get_date()

    alarmDatum=tm.strptime(str(alarmDatum),"%Y-%m-%d")
    alarmDatum=tm.strftime("%d.%m.%Y",alarmDatum)

    alarmZeitraum=inputZeitraum.get()
    einheitZeitraum=timeMenu["text"]
    alarmZeit=inputZeit.get()
    if (alarmZeitraum!="xxx"):
        if (einheitZeitraum=="Minute(n)"):
            faktor=1
        elif (einheitZeitraum=="Stunde(n)"):
            faktor=60
        elif (einheitZeitraum=="Tag(e)"):
            faktor=60*24
        elif (einheitZeitraum=="Woche(n)"):
            faktor=60*24*7
        else:
            faktor=0
        serie=faktor*int(alarmZeitraum)
    else:
        serie=0

    newAlarm=[str(alarmDatum),str(alarmZeit),str(alarmName),str(serie)]
    separator=","
    newAlarmString=separator.join(newAlarm)


    active=tableWecker.get(tableWecker.curselection())
    separator=","
    active=separator.join(active)
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:5]=="alarm"):
            wecker=zeile.split(";")
            index=wecker.index(active)
            wecker[index]=newAlarmString
            separator=";"
            zeileNeu=separator.join(wecker)
            zeileNeu=zeileNeu.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        else:
            zeileNeu=zeile.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    tableWecker.delete(0,"end")
    countWecker=len(wecker)
    i=1
    while i<countWecker:
        tableWecker.insert(i,wecker[i].split(","))
        i=i+1
    changeWecker.destroy()



def changeWecker(tableWecker):
    import tkinter as tk
    import os
    from tkinter import ttk
    import tkcalendar
    from tkcalendar import Calendar, DateEntry

    try:
        active=tableWecker.get(tableWecker.curselection())

    except:
        print("nichts ausgewählt!")
        active=""

    if (active!=""):
        ## Hier muss noch von Projekt auf Wecker geändert werden
        changeWecker=tk.Tk()
        changeWecker.title("Wecker bearbeiten")
        changeWecker.geometry("+%d+%d"%(75,250))
        changeWecker.geometry("250x150")
        changeWecker.attributes("-topmost",1)

        labelName=tk.Label(changeWecker,text="Name:",font=("times",10))
        labelName.grid(row=2,column=1,rowspan=3,columnspan=10, sticky="W")

        labelSerie=tk.Label(changeWecker,text="Serientermin?:",font=("times",10))
        labelSerie.grid(row=6,column=0,rowspan=3,columnspan=15, sticky="W")

        labelDatum=tk.Label(changeWecker,text="Datum",font=("times",10))
        labelDatum.grid(row=10,column=0,rowspan=3,columnspan=9, sticky="W")

        labelWiederholung=tk.Label(changeWecker,text="Wiederholung: alle",font=("times",10))

        labelUhrzeit=tk.Label(changeWecker,text="Uhrzeit",font=("times",10))
        labelUhrzeit.grid(row=18,column=0,rowspan=3,columnspan=14, sticky="W")

        inputName=tk.Entry(changeWecker)
        inputName.insert(0,active[2])
        inputName.grid(row=2,column=16,rowspan=3,columnspan=19, sticky="W")


        serie=tk.IntVar()

        radioJa=tk.Radiobutton(changeWecker,text="ja",variable=serie, value=1,command=lambda:changeToSerie(changeWecker, labelDatum,labelWiederholung,inputZeitraum,timeMenu))
        radioJa.grid(row=6,column=18,rowspan=3,columnspan=8, sticky="W")
        radioNein=tk.Radiobutton(changeWecker,text="nein",variable=serie, value=2,command=lambda:changeFromSerie(changeWecker, labelDatum,labelWiederholung,inputZeitraum,timeMenu))
        radioNein.grid(row=6,column=27,rowspan=3,columnspan=10, sticky="W")

        datum = DateEntry(changeWecker,date_pattern="dd.MM.yyyy", width=10,bg="darkblue",fg="white",year=2021)
        datum.set_date(active[0])
        datum.grid(row=10,column=16,rowspan=3,columnspan=18,)

        inputZeitraum=tk.Entry(changeWecker)
        inputZeitraum.configure(width=3)


        timeList=["Minute(n)","Stunde(n)","Tag(e)","Woche(n)"]
        times=tk.StringVar(changeWecker)
        times.set(timeList[0])
        timeMenu=tk.OptionMenu(changeWecker,times, *timeList)
        #passarg=[logButton,labelTime,breakButton,labelTaskTime,task,taskMenu]
        #passed=""
        #times.trace("w",lambda *args, passed=passarg:changeTask(passed,*args)) # Ruft die Funktion changeTask auf, wenn die varieable Task geändert wird (w=wirte)
        timeMenu.configure(height=1);
        timeMenu.configure(width=10);
        timeMenu.configure(anchor="w")

        inputZeit=tk.Entry(changeWecker)
        inputZeit.insert(0,active[1])
        inputZeit.grid(row=18,column=16,rowspan=3,columnspan=18,sticky="W")

        if(int(active[3])>0):
            inputZeitraum.insert(0,active[3])
            radioJa.select()
            labelWiederholung.grid(row=14,column=0,rowspan=3,columnspan=19, sticky="W")
            inputZeitraum.grid(row=14,column=21,rowspan=3,columnspan=4,sticky="W")
            timeMenu.grid(row=14,column=26 ,rowspan=3,columnspan=14,sticky="NW")
        else:
            inputZeitraum.insert(10,"xxx")
            radioNein.select()


        buttonSpeichern=tk.Button(changeWecker,text="Wecker speichern",width=15,height=1, command=lambda:changedWecker(tableWecker,changeWecker,inputName,serie,datum,inputZeitraum,timeMenu,inputZeit))
        buttonSpeichern.grid(row=22,column=16,rowspan=3,columnspan=18,sticky="W")
        #changeWecker.mainloop()





def saveWecker(tableWecker,newWecker,inputName,serie,datum,inputZeitraum,timeMenu,inputZeit):
    import tkinter as tk
    import os
    import time as tm

    alarmName=inputName.get()
    alarmDatum=datum.get_date()

    alarmDatum=tm.strptime(str(alarmDatum),"%Y-%m-%d")
    alarmDatum=tm.strftime("%d.%m.%Y",alarmDatum)

    alarmZeitraum=inputZeitraum.get()
    einheitZeitraum=timeMenu["text"]
    alarmZeit=inputZeit.get()
    if (alarmZeitraum!="xxx"):
        if (einheitZeitraum=="Minute(n)"):
            faktor=1
        elif (einheitZeitraum=="Stunde(n)"):
            faktor=60
        elif (einheitZeitraum=="Tag(e)"):
            faktor=60*24
        elif (einheitZeitraum=="Woche(n)"):
            faktor=60*24*7
        else:
            faktor=0
        serie=faktor*int(alarmZeitraum)
    else:
        serie=0

    newAlarm=[str(alarmDatum),str(alarmZeit),str(alarmName),str(serie)]
    separator=","
    newAlarmString=separator.join(newAlarm)
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:5]=="alarm"):
            zeile=zeile.replace("\n","")
            wecker=zeile.split(";")
            wecker.append(newAlarmString)
            separator=";"
            zeileNeu=separator.join(wecker)+"\n"
        else:
            zeileNeu=zeile.replace("\n","")
            zeileNeu=zeileNeu+"\n"

        configNeu=configNeu+zeileNeu
    config.close()

    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    tableWecker.delete(0,"end")
    countWecker=len(wecker)
    i=1
    while i<countWecker:
        tableWecker.insert(i,wecker[i].split(","))
        i=i+1
    newWecker.destroy()

def changeToSerie(newWecker, labelDatum,labelWiederholung,inputZeitraum,timeMenu):
    import tkinter as tk
    labelDatum.configure(text="Startdatum")
    labelWiederholung.grid(row=14,column=0,rowspan=3,columnspan=19, sticky="W")
    inputZeitraum.grid(row=14,column=21,rowspan=3,columnspan=4,sticky="W")
    timeMenu.grid(row=14,column=26 ,rowspan=3,columnspan=14,sticky="NW")
    inputZeitraum.delete(0,tk.END)

def changeFromSerie(newWecker, labelDatum,labelWiederholung,inputZeitraum,timeMenu):
    import tkinter as tk
    labelDatum.configure(text="Datum")
    labelWiederholung.grid_forget()
    inputZeitraum.grid_forget()
    timeMenu.grid_forget()
    inputZeitraum.delete(0,tk.END)
    inputZeitraum.insert(10,"xxx")


def addWecker(tableWecker):
    import tkinter as tk
    import os
    from tkinter import ttk
    import tkcalendar
    from tkcalendar import Calendar, DateEntry

    newWecker=tk.Tk()
    newWecker.title("Neuen Wecker hinzufügen")
    newWecker.geometry("+%d+%d"%(75,250))
    newWecker.geometry("250x150")
    newWecker.attributes("-topmost",1)

    labelName=tk.Label(newWecker,text="Name:",font=("times",10))
    labelName.grid(row=2,column=1,rowspan=3,columnspan=10, sticky="W")

    labelSerie=tk.Label(newWecker,text="Serientermin?:",font=("times",10))
    labelSerie.grid(row=6,column=0,rowspan=3,columnspan=15, sticky="W")

    labelDatum=tk.Label(newWecker,text="Datum",font=("times",10))
    labelDatum.grid(row=10,column=0,rowspan=3,columnspan=9, sticky="W")

    labelWiederholung=tk.Label(newWecker,text="Wiederholung: alle",font=("times",10))

    labelUhrzeit=tk.Label(newWecker,text="Uhrzeit",font=("times",10))
    labelUhrzeit.grid(row=18,column=0,rowspan=3,columnspan=14, sticky="W")

    inputName=tk.Entry(newWecker)
    inputName.grid(row=2,column=16,rowspan=3,columnspan=19, sticky="W")


    serie=tk.IntVar()

    radioJa=tk.Radiobutton(newWecker,text="ja",variable=serie, value=1,command=lambda:changeToSerie(newWecker, labelDatum,labelWiederholung,inputZeitraum,timeMenu))
    radioJa.grid(row=6,column=18,rowspan=3,columnspan=8, sticky="W")
    radioNein=tk.Radiobutton(newWecker,text="nein",variable=serie, value=2,command=lambda:changeFromSerie(newWecker, labelDatum,labelWiederholung,inputZeitraum,timeMenu))
    radioNein.grid(row=6,column=27,rowspan=3,columnspan=10, sticky="W")
    radioNein.select()


    datum = DateEntry(newWecker,date_pattern="dd.MM.yyyy", width=10,bg="darkblue",fg="white",year=2021)
    datum.grid(row=10,column=16,rowspan=3,columnspan=18,)

    inputZeitraum=tk.Entry(newWecker)
    inputZeitraum.configure(width=3)
    inputZeitraum.insert(10,"xxx")

    timeList=["Minute(n)","Stunde(n)","Tag(e)","Woche(n)"]
    times=tk.StringVar(newWecker)
    times.set(timeList[0])
    timeMenu=tk.OptionMenu(newWecker,times, *timeList)
    #passarg=[logButton,labelTime,breakButton,labelTaskTime,task,taskMenu]
    #passed=""
    #times.trace("w",lambda *args, passed=passarg:changeTask(passed,*args)) # Ruft die Funktion changeTask auf, wenn die varieable Task geändert wird (w=wirte)
    timeMenu.configure(height=1);
    timeMenu.configure(width=10);
    timeMenu.configure(anchor="w")

    inputZeit=tk.Entry(newWecker)
    inputZeit.insert(10,"hh:mm")
    inputZeit.grid(row=18,column=16,rowspan=3,columnspan=18,sticky="W")


    buttonSpeichern=tk.Button(newWecker,text="Wecker speichern",width=15,height=1, command=lambda:saveWecker(tableWecker,newWecker,inputName,serie,datum,inputZeitraum,timeMenu,inputZeit))
    buttonSpeichern.grid(row=22,column=16,rowspan=3,columnspan=18,sticky="W")
    #newWecker.mainloop()

def deleteWecker(tableWecker):
    import os
    active=tableWecker.get(tableWecker.curselection())
    separator=","
    active=separator.join(active)
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:5]=="alarm"):
            zeileArr=zeile.split(";")
            zeileArr.remove(active)
            separator=";"
            zeileNeu=separator.join(zeileArr)
            zeileNeu=zeileNeu.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu

    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    tableWecker.delete(0,"end")
    countWecker=len(zeileArr)
    i=1
    while i<countWecker:
        tableWecker.insert(i,zeileArr[i].split(","))
        i=i+1



#########---------- Funktionen zuer Erinnerungsbearbeitung--------##############
def changedErinnerung(active,tableErinnerung,changeErinnerung,inputName, inputSymbol,inputErinnerung,checkAktivVar,checkCountdownVar):
    import os
    import time as tm
    erinnerungName=inputName.get()
    erinnerungSymbol=inputSymbol.get()
    erinnerungErinnerung=inputErinnerung.get()

    if (checkAktivVar.get()==1):
        checkAktiv="ja"
    else:
        checkAktiv="nein"

    if(checkCountdownVar.get()==1):
        checkCountdown="ja"
    else:
        checkCountdown="nein"

    newErinnerungArr=[str(erinnerungName),str(erinnerungSymbol),str(erinnerungErinnerung),str(checkAktiv),str(checkCountdown)]
    separator=","
    newErinnerungString=separator.join(newErinnerungArr)
    separator=","
    active=separator.join(active)

    #active=tableErinnerung.curselection()
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:10]=="erinnerung"):
            erinnerung=zeile.split(";")
            index=erinnerung.index(active)
            erinnerung[index]=newErinnerungString
            separator=";"
            zeileNeu=separator.join(erinnerung)
            zeileNeu=zeileNeu.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        else:
            zeileNeu=zeile.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    tableErinnerung.delete(0,"end")
    countErinnerung=len(erinnerung)
    i=1
    while i<countErinnerung:
        tableErinnerung.insert(i,erinnerung[i].split(","))
        i=i+1
    changeErinnerung.destroy()



def changeErinnerung(tableErinnerung):
    import tkinter as tk
    import os
    from tkinter import ttk
    import tkcalendar
    from tkcalendar import Calendar, DateEntry

    try:
        active=tableErinnerung.get(tableErinnerung.curselection())

    except:
        print("nichts ausgewählt!")
        active=""

    if (active!=""):
        ## Hier muss noch von Projekt auf Wecker geändert werden
        changeErinnerung=tk.Tk()
        changeErinnerung.title("Neuen Erinnerung hinzufügen")
        changeErinnerung.geometry("+%d+%d"%(75,250))
        changeErinnerung.geometry("250x150")
        changeErinnerung.attributes("-topmost",1)



        labelName=tk.Label(changeErinnerung,text="Name:",font=("times",10))
        labelName.grid(row=0,column=1,rowspan=1,columnspan=10, sticky="W")

        labelSymbol=tk.Label(changeErinnerung,text="Symbol:",font=("times",10))
        labelSymbol.grid(row=1,column=1,rowspan=1,columnspan=10, sticky="W")

        labelWiederholung1=tk.Label(changeErinnerung,text="Wiederholung nach:",font=("times",10))
        labelWiederholung1.grid(row=2,column=1,rowspan=1,columnspan=10, sticky="W")
        labelWiederholung2=tk.Label(changeErinnerung,text="Minuten",font=("times",10))
        labelWiederholung2.grid(row=2,column=19,rowspan=1,columnspan=10, sticky="W")

        labelaktiv=tk.Label(changeErinnerung,text="aktiv?",font=("times",10))
        labelaktiv.grid(row=3,column=1,rowspan=1,columnspan=10, sticky="W")

        labelCountdown=tk.Label(changeErinnerung,text="Countdown?",font=("times",10))
        labelCountdown.grid(row=4,column=1,rowspan=1,columnspan=10, sticky="W")

        inputName=tk.Entry(changeErinnerung)
        inputName.grid(row=0,column=10,rowspan=1,columnspan=20, sticky="W")
        inputName.insert(0,active[0])

        inputSymbol=tk.Entry(changeErinnerung)
        inputSymbol.grid(row=1,column=10,rowspan=1,columnspan=2, sticky="W")
        inputSymbol.configure(width=3)
        inputSymbol.insert(0,active[1])

        inputErinnerung=tk.Entry(changeErinnerung)
        inputErinnerung.grid(row=2,column=15,rowspan=1,columnspan=5, sticky="W")
        inputErinnerung.configure(width=3)
        inputErinnerung.insert(0,active[2])

        checkAktivVar=tk.IntVar(changeErinnerung)

        checkAktiv=tk.Checkbutton(changeErinnerung,variable = checkAktivVar, onvalue = 1, offvalue = 0)
        checkAktiv.grid(row=3,column=10,rowspan=1,columnspan=1, sticky="W")
        if(active[3]=="ja"):
            checkAktivVar.set(1)
            #checkAktiv.select()
        else:
            checkAktivVar.set(0)

        checkCountdownVar=tk.IntVar(changeErinnerung)
        checkCountdown=tk.Checkbutton(changeErinnerung,variable = checkCountdownVar, onvalue = 1, offvalue = 0)
        checkCountdown.grid(row=4,column=10,rowspan=1,columnspan=1, sticky="W")
        if(active[4]=="ja"):
            checkCountdownVar.set(1)
            #checkAktiv.select()
        else:
            checkCountdownVar.set(0)


        buttonSpeichern=tk.Button(changeErinnerung,text="Erinnerung speichern",width=15,height=1, command=lambda:changedErinnerung(active,tableErinnerung,changeErinnerung,inputName, inputSymbol,inputErinnerung,checkAktivVar,checkCountdownVar))
        buttonSpeichern.grid(row=5,column=16,rowspan=3,columnspan=18,sticky="W")
        #changeErinnerung.mainloop()






def saveErinnerung(tableErinnerung,newErinnerung,inputName, inputSymbol,inputErinnerung,checkAktivVar,checkCountdownVar):
    import tkinter as tk
    import os
    import time as tm

    erinnerungName=inputName.get()
    erinnerungSymbol=inputSymbol.get()
    erinnerungErinnerung=inputErinnerung.get()
    if (checkAktivVar.get()==1):
        checkAktiv="ja"
    else:
        checkAktiv="nein"

    if(checkCountdownVar.get()==1):
        checkCountdown="ja"
    else:
        checkCountdown="nein"

    newErinnerungArr=[str(erinnerungName),str(erinnerungSymbol),str(erinnerungErinnerung),str(checkAktiv),str(checkCountdown)]
    separator=","
    newErinnerungString=separator.join(newErinnerungArr)
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:10]=="erinnerung"):
            zeile=zeile.replace("\n","")
            erinnerung=zeile.split(";")
            erinnerung.append(newErinnerungString)
            separator=";"
            zeileNeu=separator.join(erinnerung)+"\n"
        else:
            zeileNeu=zeile.replace("\n","")
            zeileNeu=zeileNeu+"\n"

        configNeu=configNeu+zeileNeu
    config.close()

    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    tableErinnerung.delete(0,"end")
    countErinnerung=len(erinnerung)
    i=1
    while i<countErinnerung:
        tableErinnerung.insert(i,erinnerung[i].split(","))
        i=i+1
    newErinnerung.destroy()


def addErinnerung(tableErinnerung):
    import tkinter as tk
    import os
    from tkinter import ttk
    import tkcalendar
    from tkcalendar import Calendar, DateEntry

    newErinnerung=tk.Tk()
    newErinnerung.title("Neuen Erinnerung hinzufügen")
    newErinnerung.geometry("+%d+%d"%(75,250))
    newErinnerung.geometry("250x150")
    newErinnerung.attributes("-topmost",1)

    labelName=tk.Label(newErinnerung,text="Name:",font=("times",10))
    labelName.grid(row=0,column=1,rowspan=1,columnspan=10, sticky="W")

    labelSymbol=tk.Label(newErinnerung,text="Symbol:",font=("times",10))
    labelSymbol.grid(row=1,column=1,rowspan=1,columnspan=10, sticky="W")

    labelWiederholung1=tk.Label(newErinnerung,text="Wiederholung nach:",font=("times",10))
    labelWiederholung1.grid(row=2,column=1,rowspan=1,columnspan=10, sticky="W")
    labelWiederholung2=tk.Label(newErinnerung,text="Minuten",font=("times",10))
    labelWiederholung2.grid(row=2,column=19,rowspan=1,columnspan=10, sticky="W")

    labelaktiv=tk.Label(newErinnerung,text="aktiv?",font=("times",10))
    labelaktiv.grid(row=3,column=1,rowspan=1,columnspan=10, sticky="W")

    labelCountdown=tk.Label(newErinnerung,text="Countdown?",font=("times",10))
    labelCountdown.grid(row=4,column=1,rowspan=1,columnspan=10, sticky="W")

    inputName=tk.Entry(newErinnerung)
    inputName.grid(row=0,column=10,rowspan=1,columnspan=20, sticky="W")

    inputSymbol=tk.Entry(newErinnerung)
    inputSymbol.grid(row=1,column=10,rowspan=1,columnspan=2, sticky="W")
    inputSymbol.configure(width=3)

    inputErinnerung=tk.Entry(newErinnerung)
    inputErinnerung.grid(row=2,column=15,rowspan=1,columnspan=5, sticky="W")
    inputErinnerung.configure(width=3)

    checkAktivVar=tk.IntVar(newErinnerung)

    checkAktiv=tk.Checkbutton(newErinnerung,variable = checkAktivVar, onvalue = 1, offvalue = 0)
    checkAktiv.grid(row=3,column=10,rowspan=1,columnspan=1, sticky="W")
    checkAktivVar.set(1)
    checkAktiv.select()
    checkCountdownVar=tk.IntVar(newErinnerung)
    checkCountdown=tk.Checkbutton(newErinnerung,variable = checkCountdownVar, onvalue = 1, offvalue = 0)
    checkCountdown.grid(row=4,column=10,rowspan=1,columnspan=1, sticky="W")

    buttonSpeichern=tk.Button(newErinnerung,text="Erinnerung speichern",width=15,height=1, command=lambda:saveErinnerung(tableErinnerung,newErinnerung,inputName, inputSymbol,inputErinnerung,checkAktivVar,checkCountdownVar))
    buttonSpeichern.grid(row=5,column=16,rowspan=3,columnspan=18,sticky="W")
    #newErinnerung.mainloop()

def deleteErinnerung(tableErinnerung):
    import os
    active=tableErinnerung.get(tableErinnerung.curselection())
    separator=","
    active=separator.join(active)
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:10]=="erinnerung"):
            zeileArr=zeile.split(";")
            zeileArr.remove(active)
            separator=";"
            zeileNeu=separator.join(zeileArr)
            zeileNeu=zeileNeu.replace("\n","")
            zeileNeu=zeileNeu+"\n"
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu

    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    tableErinnerung.delete(0,"end")
    countErinnerung=len(zeileArr)
    i=1
    while i<countErinnerung:
        tableErinnerung.insert(i,zeileArr[i].split(","))
        i=i+1


def weckerMenu():
    import tkinter as tk
    from tkinter import ttk
    import os
    from MultiListbox import MultiListbox

    menu.destroy()

    weckerFenster=tk.Tk()
    weckerFenster.title("Weckermenü")
    weckerFenster.geometry("+%d+%d"%(100,100))
    weckerFenster.geometry("550x250")
    weckerFenster.attributes("-topmost",1)

    tabControl = ttk.Notebook(weckerFenster)

    weckerTab = ttk.Frame(tabControl)
    erinnerungsTab = ttk.Frame(tabControl)

    tabControl.add(weckerTab, text ='Termine')
    tabControl.add(erinnerungsTab, text ='Erinnerungen')
    tabControl.pack(expand = 1, fill ="both")




    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    for zeile in config:
        if (zeile[0:5]=="alarm"):
            wecker=zeile.split(";")
        elif(zeile[0:10]=="erinnerung"):
            erinnerung=zeile.split(";")
    config.close()

    #####--------------TAB Wecker----------------------------###########
    label1=ttk.Label(weckerTab,text="vorhandene Wecker:",font=("times",10))
    label1.grid(row=0,column=0, sticky="W")

    buttonBearbeiten=tk.Button(weckerTab,text="Ändern",width=10,height=1, command=lambda:changeWecker(tableWecker))
    buttonBearbeiten.grid(row=2,column=2, sticky="W")

    buttonLoeschen=tk.Button(weckerTab,text="Löschen",width=10,height=1,command=lambda:deleteWecker(tableWecker))
    buttonLoeschen.grid(row=3,column=2, sticky="W")

    buttonHinzufuegen=tk.Button(weckerTab,text="Neuer Wecker",width=12,height=1,command=lambda:addWecker(tableWecker))
    buttonHinzufuegen.grid(row=5,column=2, columnspan=2, sticky="W")

    buttonOK=tk.Button(weckerTab,text="OK",width=10,height=1,command=lambda:close(weckerFenster))
    buttonOK.grid(row=7,column=2, sticky="W")

    tableWecker=MultiListbox(weckerTab,(("Nächstes Datum",10),("Nächste Uhrzeit",10),("Name",15),("Serie",15)))
    tableWecker.grid(row=2, rowspan=6, column=0, sticky="W")

    countAlarm=len(wecker)
    i=1
    while i<countAlarm:
        columns=wecker[i].split(",")
        ergebnis=ZeitraumBerechnen(columns[3])
        serie=str(ergebnis[0])+" "+str(ergebnis[1])
        tableWecker.insert(tk.END, (columns[0] , columns[1],columns[2],serie))
        i=i+1

    #####--------------TAB Erinnerungen----------------------------###########
    label1E=ttk.Label(erinnerungsTab,text="vorhandene Erinnerungen:",font=("times",10))
    label1E.grid(row=0,column=0, sticky="W")

    buttonBearbeitenE=tk.Button(erinnerungsTab,text="Ändern",width=10,height=1, command=lambda:changeErinnerung(tableErinnerung))
    buttonBearbeitenE.grid(row=2,column=2, sticky="W")

    buttonLoeschenE=tk.Button(erinnerungsTab,text="Löschen",width=10,height=1,command=lambda:deleteErinnerung(tableErinnerung))
    buttonLoeschenE.grid(row=3,column=2, sticky="W")

    buttonHinzufuegenE=tk.Button(erinnerungsTab,text="Neue Erinnerung",width=12,height=1,command=lambda:addErinnerung(tableErinnerung))
    buttonHinzufuegenE.grid(row=5,column=2, columnspan=2, sticky="W")

    buttonOKE=tk.Button(erinnerungsTab,text="OK",width=10,height=1,command=lambda:close(weckerFenster))
    buttonOKE.grid(row=7,column=2, sticky="W")

    tableErinnerung=MultiListbox(erinnerungsTab,(("Erinnerung",20),("Symbol",10),("alle X min",10),("aktiv?",10),("Countdown?",10)))
    tableErinnerung.grid(row=2, rowspan=6, column=0, sticky="W")

    countErinnerung=len(erinnerung)
    i=1
    while i<countErinnerung:
        columns=erinnerung[i].split(",")
        tableErinnerung.insert(tk.END, (columns[0] ,columns[1],columns[2],columns[3],columns[4]))
        i=i+1





def hideWindow(pT,hideButton):
    if (hideButton["text"]=="Hide"):
        pT.attributes("-topmost",0)
        hideButton.config(text="Fix")
    else:
        pT.attributes("-topmost",1)
        hideButton.config(text="Hide")

def newAlarm(labelActiveAlarm,addAlarmButton,inputTimeNextAlarm,labelNextAlarm,inputNextAlarm,alarmButton):
    alarmButton.grid_forget()
    #labelActiveAlarm.grid_forget()
    inputTimeNextAlarm.grid(row=13,rowspan=5, column=0,columnspan=2 ,sticky="NW")
    labelNextAlarm.grid(row=13,rowspan=5,column=2, columnspan=3,sticky="NW")
    inputNextAlarm.grid(row=13,rowspan=5, column=6, columnspan=10, sticky="NW")
    addAlarmButton.grid(row=13, rowspan=5,column=26,columnspan=3,sticky="NW")

def ZeitraumBerechnen(Minuten):
    if (int(Minuten)!=0):
        if(int(Minuten)%(7*24*60)==0):
            einheit="Wochen(n)"
            zeit=int(Minuten)/(7*24*60)
        elif(int(Minuten)%(24*60)==0):
            einheit="Tag(e)"
            zeit=int(Minuten)/(24*60)
        elif(int(Minuten)%(60)==0):
            einheit="Stunde(n)"
            zeit=int(Minuten)/60
        else:
            einheit="Minute(n)"
            zeit=int(Minuten)
        ergebnis=[int(zeit),einheit]
    else:
        ergebnis=[0,""]
    return ergebnis

def addAlarm(addAlarmButton,labelNextAlarm,alarmButton,inputTimeNextAlarm,inputNextAlarm,labelActiveAlarm):
    import time
    import os
    curSeconds=time.mktime(time.localtime())
    alarmSeconds=curSeconds+60*int(inputTimeNextAlarm.get())
    nextAlarm=time.localtime(alarmSeconds)
    dateAlarm=time.strftime("%d.%m.%Y",nextAlarm)
    timeAlarm=time.strftime("%H:%M",nextAlarm)
    nameAlarm=inputNextAlarm.get()
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:5]=="alarm"):
            zeile=zeile.replace("\n","")
            zeileNeu=zeile+";"+dateAlarm+","+timeAlarm+","+nameAlarm+","+"0\n"
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    config.close()
    nextAlarmArr=getNextAlarm()
    nextAlarm=nextAlarmArr[0]
    nextAlarmName=nextAlarmArr[1]
    curSeconds=time.mktime(time.localtime())
    nextAlarmSeconds=time.mktime(nextAlarm)
    timerNextAlarm=int((nextAlarmSeconds-curSeconds)/60)+1 #+1 weil direkt im Anschluss Timer ausgeführt wird, wo die variabele um 1 reduziert wird
    labelActiveAlarm["text"]="Noch "+str(timerNextAlarm)+"min bis "+nextAlarmName
    alarmButton.grid(row=13,rowspan=4,column=0,  columnspan=23,sticky="NW")
    inputTimeNextAlarm.grid_forget()
    labelNextAlarm.grid_forget()
    inputNextAlarm.grid_forget()
    addAlarmButton.grid_forget()

def getNextAlarm():
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import os
    import time as tm

    curDateTime=tm.strftime("%d.%m.%Y %H:%M",tm.localtime())
    curDateTime=tm.strptime(curDateTime,"%d.%m.%Y %H:%M")
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    change=0
    nextAlarm=""
    nextAlarmName=""
    for zeile in config:
        if (zeile[0:5]=="alarm"):
            alarms=zeile.split(";")
            i=1
            date=[]
            time=[]
            name=[]
            nextAlarm=tm.strptime("01.01.2200 09:00","%d.%m.%Y %H:%M")
            while i<len(alarms):
                alarm=alarms[i].split(",")
                date.append(alarm[0])
                time.append(alarm[1])
                name.append(alarm[2])
                alarmDateTime=tm.strptime(alarm[0]+" "+alarm[1],"%d.%m.%Y %H:%M")

                if alarmDateTime<curDateTime:
                    alarms.pop(i)
                    change=1
                elif alarmDateTime<nextAlarm:
                    nextAlarm=alarmDateTime
                    nextAlarmName=str(alarm[2])
                i=i+1
            separator=";"
            zeileNeu=separator.join(alarms)+"\n"

        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu

    config.close()
    if change==1:
        config=open(cur_path+"\config.txt","w")
        config.write(configNeu)
        config.close()
    nextAlarmArr=[nextAlarm,nextAlarmName]
    return nextAlarmArr
