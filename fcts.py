


def close(fenster):
    fenster.destroy()
    #menu.attributes("-topmost",0)
    #pT.attributes("-topmost",1)
    try:
            menu.destroy()

    except:
            print("close():Menüfenster ist schon zu")


def timer(labelWorkTime, labelTaskTime,logButton,breakButton,taskMenu,labelTime):
    import time
    zeit=time.strftime("%H:%M",time.localtime())
    if(zeit=="00:00"):
            labelWorkTime.config(text="0h 0min")
    labelTime.config(text=zeit)
    labelTime.after(60000,lambda:timer(labelWorkTime, labelTaskTime, logButton,breakButton,taskMenu,labelTime)) # müsste auf 60000 gesetzt werden
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
    print(cur_path)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:8]=="projekte"):
            zeileArr=zeile.split(";")
            zeileArr.remove(active)
            separator=";"
            zeileNeu=separator.join(zeileArr)
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    listProjekte.delete(0,"end")
    countProjekte=len(zeileArr)
    i=1
    while i<countProjekte:
        listProjekte.insert(i,zeileArr[i])
        i=i+1

def changedProjekt(listProjekte,active,newProjektName,changeName):
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
        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
    listProjekte.delete(0,"end")
    countProjekte=len(zeileArr)
    i=1
    while i<countProjekte:
        listProjekte.insert(i,zeileArr[i])
        i=i+1
    changeName.destroy()


def changeProjekt(listProjekte):
    import tkinter as tk
    active=listProjekte.get(listProjekte.curselection())

    changeName=tk.Tk()
    changeName.title("Neuer Projektname")
    changeName.geometry("+%d+%d"%(75,250))
    changeName.geometry("250x75")
    changeName.attributes("-topmost",1)

    label1=tk.Label(changeName,text="Bitte gebe den neuen Projektnamen an:",font=("times",10))
    label1.grid(row=0,column=0,columnspan=2, sticky="W")

    input=tk.Entry(changeName)
    input.insert(10,"")
    input.grid(row=1,column=0, sticky="W")

    buttonOK2=tk.Button(changeName,text="OK",height=1,width=10, command=lambda:changedProjekt(listProjekte,active,input,changeName))
    buttonOK2.grid(row=1,column=1, sticky="W")

def addProjekt(listProjekte,inputNeu):
    import os
    newName=inputNeu.get()
    cur_path = os.path.dirname(__file__)
    config=open(cur_path+"\config.txt","r")
    configNeu=""
    for zeile in config:
        if (zeile[0:8]=="projekte"):
            zeileArr=zeile.split(";")
            zeileArr.append(newName)
            print(zeileArr)
            separator=";"
            zeileNeu=separator.join(zeileArr)
            zeileNeu=zeileNeu.replace("\n","")

        else:
            zeileNeu=zeile
        configNeu=configNeu+zeileNeu
    config.close()
    config=open(cur_path+"\config.txt","w")
    config.write(configNeu)
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
        log.write("logIn;"+logDate+";"+logTime+";"+task+"\n")

    if(timeLogOut.get()!="hh:mm"):
        logDate=str(dateLogOut.get_date())
        logTime=str(timeLogOut.get())+":00"
        task=taskLogOut["text"]
        log.write("logOut;"+logDate+";"+logTime+";"+task+"\n")
    stempelFenster.destroy()




def auswertung(menu):
    import os

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
    sleep(60)
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
        weckerButton=tk.Button(menu,text="Wecker",state=tk.DISABLED,width=12,height=1,command=lambda:test())
        weckerButton.grid(row=3,column=0)
        einstellungButton=tk.Button(menu,text="Einstellungen",state=tk.DISABLED,width=12,height=1,command=lambda:test())
        einstellungButton.grid(row=4,column=0)
        auswertungButton=tk.Button(menu,text="Auswertung",width=12,height=1,command=lambda:auswertung(menu))
        auswertungButton.grid(row=5,column=0)

def hideWindow(pT,hideButton):
    if (hideButton["text"]=="Hide"):
        pT.attributes("-topmost",0)
        hideButton.config(text="Fix")
    else:
        pT.attributes("-topmost",1)
        hideButton.config(text="Hide")
