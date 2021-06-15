
""" Fussballspiel
Es gibt 16 Mannschaften mit jeweils 20 Spielern.
Diese treten an 30 Spieltagen gegeneinander an und kämpfen die Meisterschaft aus.
Eine Mannschaft wird durch den Benutzer verwaltet, der Rest über Computer mit mehr oder weniger idealen Einstellungen.
Jeder Spieler hat die folgenden Eigenschaften: Name, Alter, Müdigkeit, Gesundheit, Faehigkeiten
Zu den Fähigkeiten gehört: Torhüter-, Abwehr-, Mittelfeld-, Sturmfähigkeit
Zu Beginn jedes Spieles wird die Aufstellung vom PC bzw. Anwender festgelegt. Dabei treten auf unterschiedlichen Positionen die Fähigkeiten unterschiedlich stark zu Tage.
Es wird immer im 4,4,2 aufgestellt.
Wenn Spieler gespielt haben steigt ihre Müdigkeit und die möglichkeit einer Verletzung und somit Gesundheitsverlusts steigt.
"""
import random
import csv
import pickle
from pathlib import Path
import tkinter as tk
import pygame

pygame.init()

#genutzte Farben:
ORANGE=(255,140,0)
ROT=(255,0,0)
GRUEN=(0,255,0)
SCHWARZ=(0,0,0)
WEISS=(255,255,255)

"""
    def spielerZuweisen(self):
        zahl_spieler=0
        while zahl_spieler<20:
            self.spieler[zahl_spieler]=Spieler(zahl_spieler,vereinsname)
            zahl_spieler+=1

 """
#++++++++++++++++++++++++++
#Definition der Klassen
#++++++++++++++++++++++++++
class Spieler:
    def __init__(self, nummer):
        self.nummer=nummer
        self.name="spieler "+str(nummer)
        self.alter=random.randint(16,30)
        self.muedigkeit=random.randint(0,100)
        self.gesundheit=random.randint(0,100)
        self.torwart=random.randint(0,10)
        self.abwehr=random.randint(0,10)
        self.mittelfeld=random.randint(0,10)
        self.sturm=random.randint(0,10)

class Mannschaft:
    zahl_spieler=0
    spieler=[]

    while zahl_spieler<20:
        spieler.append(0)
        spieler[zahl_spieler]=Spieler(zahl_spieler)
        zahl_spieler+=1


    def __init__(self,nummer,punkte,position,spieler=[]):
        mannschaftsname=["Mannschaft1","Mannschaft2","Mannschaft3","Mannschaft4","Mannschaft5","Mannschaft6","Mannschaft7","Mannschaft8","Mannschaft9","Mannschaft10","Mannschaft11","Mannschaft12","Mannschaft13","Mannschaft14","Mannschaft15","Mannschaft16"]
        self.mannschaftsname=mannschaftsname[nummer]
        self.nummer=nummer
        self.punkte=punkte
        self.position=position
        anzahl_spieler=0
        self.spieler=[]
        while anzahl_spieler<20:
            self.spieler.append(Spieler(anzahl_spieler))
            anzahl_spieler+=1

    def TorwartFinden(self):

        highscore=0
        bester_torwart=0
        i=1


        for spieler in self.spieler:

            score=(spieler.torwart+0.5*spieler.abwehr)*(100-spieler.muedigkeit)/100*spieler.gesundheit/100
            if score>highscore:
                highscore=score
                torwart=i

            i+=1

        return torwart, highscore

    def AbwehrFinden(self,torwart):
        highscore=[0,0,0,0]
        beste_abwehr=[0,0,0,0]
        i=1
        for spieler in self.spieler:
            if i!=torwart[-1]:
                score=(spieler.torwart*0.1+spieler.abwehr+0.4*spieler.mittelfeld)*(100-spieler.muedigkeit)/100*spieler.gesundheit/100
                if score>highscore[0]:
                    highscore[0]=score
                    beste_abwehr[0]=i
                elif score>highscore[1]:
                    highscore[1]=score
                    beste_abwehr[1]=i
                elif score>highscore[2]:
                    highscore[2]=score
                    beste_abwehr[2]=i
                elif score>highscore[3]:
                    highscore[3]=score
                    beste_abwehr[3]=i
            i=i+1
        return beste_abwehr,highscore

    def MittelfeldFinden(self,torwart,abwehr):
        highscore=[0,0,0,0]
        bestes_mittelfeld=[0,0,0,0]
        i=1
        for spieler in self.spieler:
            if i!=torwart[-1] and not i in abwehr[-1]:
                score=(spieler.abwehr*0.2+spieler.mittelfeld+0.3*spieler.sturm)*(100-spieler.muedigkeit)/100*spieler.gesundheit/100
                if score>highscore[0]:
                    highscore[0]=score
                    bestes_mittelfeld[0]=i
                elif score>highscore[1]:
                    highscore[1]=score
                    bestes_mittelfeld[1]=i
                elif score>highscore[2]:
                    highscore[2]=score
                    bestes_mittelfeld[2]=i
                elif score>highscore[3]:
                    highscore[3]=score
                    bestes_mittelfeld[3]=i
            i=i+1
        return bestes_mittelfeld,highscore

    def SturmFinden(self,torwart,abwehr,mittelfeld):
        highscore=[0,0]
        bester_sturm=[0,0]
        i=1
        for spieler in self.spieler:
            if i!=torwart[-1] and not i in abwehr[-1] and not i in mittelfeld[-1]:
                score=(spieler.mittelfeld*0.5+spieler.sturm)*(100-spieler.muedigkeit)/100*spieler.gesundheit/100
                if score>highscore[0]:
                    highscore[0]=score
                    bester_sturm[0]=i
                elif score>highscore[1]:
                    highscore[1]=score
                    bester_sturm[1]=i

            i=i+1
        return bester_sturm,highscore

class Spieltag:
    def __init__(self,n_spieltag=0,ergebnisse=[]):
        self.n_spieltag=0
        self.ergebnisse=[]


class Liga:
    def __init__(self,name,mannschaften=[],reihenfolge=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],punkte=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],torverhaeltnis=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],spieltag=0):
        self.spieltag=Spieltag(spieltag)
        self.reihenfolge=reihenfolge
        self.punkte=punkte
        self.torverhaeltnis=torverhaeltnis
        self.mannschaften=mannschaften
        self.name=name



        zahl_mannschaften=0
        while zahl_mannschaften<16:
            mannschaft=Mannschaft(zahl_mannschaften,0,1)
            self.mannschaften.append(mannschaft)
            zahl_mannschaften+=1

         # Aufstellung ermitteln automatisch
    def AufstellungErmitteln(self):
        """
        1=Torwart Wert=1xTorwart+0,5*Abwehr
        2,3,4,5=Abwehr Wert=0,1*Torwart+1*Abwehr+0,4*Mittelfeld
        6,7,8,9=Mittelfeld Wert=0,2*Abwehr+1*Mittelfeld+0,3*Sturm
        10,11=Sturm Wert=0,5*Mittelfeld+1*Sturm
        """
        i=0
        self.torwart=[]
        self.abwehr=[]
        self.mittelfeld=[]
        self.sturm=[]

        for mannschaft in bundesliga.mannschaften:

            self.mannschaften[mannschaft.nummer].torwart=self.mannschaften[mannschaft.nummer].TorwartFinden()
            self.mannschaften[mannschaft.nummer].abwehr=self.mannschaften[mannschaft.nummer].AbwehrFinden(self.mannschaften[mannschaft.nummer].torwart)
            self.mannschaften[mannschaft.nummer].mittelfeld=self.mannschaften[mannschaft.nummer].MittelfeldFinden(self.mannschaften[mannschaft.nummer].torwart,self.mannschaften[mannschaft.nummer].abwehr)
            self.mannschaften[mannschaft.nummer].sturm=self.mannschaften[mannschaft.nummer].SturmFinden(self.mannschaften[mannschaft.nummer].torwart,self.mannschaften[mannschaft.nummer].abwehr,self.mannschaften[mannschaft.nummer].mittelfeld)


            i=i+1



    def LigaSpeichern(self,file):
        print("speichert")
        f = open(file,"wb")
        pickle.dump(self,f)
        f.close

    def LigaLaden(self,file):
        liga=pickle.load(open(file,"rb"))
        return liga

    def TamsBestimmen(self,nummer): # Tams=Torwart,Abwehr,Mittelfeld,Sturm
        x=self.mannschaften[nummer]
        #Sturmstärke=1xSturm+0,5*Mittelfeld
        sturmstaerke=x.sturm[1][0]+x.sturm[1][1]+0.5*(x.mittelfeld[1][0]+x.mittelfeld[1][1]+x.mittelfeld[1][2]+x.mittelfeld[1][3])
        #Mittelfeldstärke=0,5xAbwehr+1xMittelfeld+0,5xSturm
        mittelfeldstaerke=0.5*(x.abwehr[1][0]+x.abwehr[1][1]+x.abwehr[1][2]+x.abwehr[1][3])+x.mittelfeld[1][0]+x.mittelfeld[1][1]+x.mittelfeld[1][2]+x.mittelfeld[1][3]+0.5*(x.sturm[1][0]+x.sturm[1][1])
        #Abwehrstärke=1xAbwehr+0,5xMittelfeld
        abwehrstaerke=x.abwehr[1][0]+x.abwehr[1][1]+x.abwehr[1][2]+x.abwehr[1][3]+0.5*(x.mittelfeld[1][0]+x.mittelfeld[1][1]+x.mittelfeld[1][2]+x.mittelfeld[1][3])
        #Torwartstärke=1xTorwart+0,5*Abwehr
        torwartstaerke=x.torwart[1]+0.5*(x.abwehr[1][0]+x.abwehr[1][1]+x.abwehr[1][2]+x.abwehr[1][3])
        return torwartstaerke, abwehrstaerke, mittelfeldstaerke, sturmstaerke

    def SpielAusführen(self,paarung):

        staerke1=self.TamsBestimmen(paarung[0])
        staerke2=self.TamsBestimmen(paarung[1])


        t=1
        ball=0
        tor1=[]
        tor2=[]

        while t<=90:
            if ball==0:
                if staerke2[2]*random.randint(0,1)>1.5*staerke1[2]*random.randint(0,1):
                    ball=1
                    t+=1
                elif staerke1[3]*random.randint(0,1)>(staerke2[0]+staerke2[1])*random.randint(0,1):
                    tor1.append(t)
                    ball=1
                    t+=1
                else:
                    ball=1
                    t+=1

            elif ball==1:
                if staerke1[2]*random.randint(0,1)>1.5*staerke2[2]*random.randint(0,1):
                    ball=0
                    t+=1
                elif staerke2[3]*random.randint(0,1)>(staerke1[0]+staerke1[1])*random.randint(0,1):
                    tor2.append(t)
                    ball==0
                    t+=1
                else:
                    ball=0
                    t+=1


        if len(tor1)>len(tor2):
            self.punkte[paarung[0]]+=3
        elif len(tor2)>len(tor1):
            self.punkte[paarung[1]]+=3
        else:
            self.punkte[paarung[0]]+=1
            self.punkte[paarung[1]]+=1

        self.torverhaeltnis[paarung[0]]+=len(tor1)-len(tor2)
        self.torverhaeltnis[paarung[1]]+=len(tor2)-len(tor1)
        return len(tor1),len(tor2)



    def ErgebnisseAnzeigen(self,paarung,ergebnisse,n_spieltag):
        text_to_screen(screen,"Hallo",50,50)


        """ Ab hier altes Fenster
        Erg=tk.Tk()
        Erg.title("Ergebnisse Spieltag "+ str(n_spieltag))

        text1_="Ergebnisse "+ self.name+ ", Spieltag "+ str(n_spieltag)
        text1=tk.Label(Erg,text=text1_)
        text1.grid()

        texte=[]
        i=0

        while i<8:
            mannschaft1_=self.mannschaften[paarung[i][0]].mannschaftsname
            mannschaft2_=self.mannschaften[paarung[i][1]].mannschaftsname
            tore1_=str(ergebnisse[i][0])+ " : "
            tore2_=str(ergebnisse[i][1])


            tk.Label(Erg,text=mannschaft1_).grid(row=i+3,column=160,sticky=tk.W)
            tore1=tk.Label(Erg,text=tore1_).grid(row=i+3,column=165, sticky=tk.E)
            tore2=tk.Label(Erg,text=tore2_).grid(row=i+3,column=170,sticky=tk.W)
            tk.Label(Erg,text=mannschaft2_).grid(row=i+3,column=175)

            i+=1
        #Ab hier Tabelle erstellen

        i=0
        wertung=[]
        while i<16:
            wertung.append(self.punkte[i]*1000+self.torverhaeltnis[i])
            i+=1


        sortpunkte=sorted(wertung,reverse=True)

        i=0
        while i<16:
            j=0
            while j<16:
                if wertung[i]==sortpunkte[j]:
                    self.reihenfolge[i]=j
                    j=16
                j+=1
            i+=1


        nummer=[]
        mannschaft=[]
        spieltagx=[]
        torverhaeltnis=[]
        punkte=[]
        i=0
        j=0

        u_spieltag=tk.Label(Erg,text="Spieltag")
        u_torverhaeltnis=tk.Label(Erg,text="Torverhältnis")
        u_punkte=tk.Label(Erg,text="Punkte")

        u_spieltag.grid(row=20,column=165)
        u_torverhaeltnis.grid(row=20,column=170)
        u_punkte.grid(row=20,column=175)

        belegt=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        while i<16:
            rang=self.reihenfolge[i]
            j=0
            while j<16:

                if belegt[rang]==0:
                    belegt[rang]=1
                    j=16
                else:
                    rang+=1
                    j+=1



            nummer_=str(rang+1)
            nummer.append(tk.Label(Erg,text=nummer_))
            nummer[i].grid(row=rang+25,column=155)


            mannschaft_=self.mannschaften[i].mannschaftsname
            mannschaft.append(tk.Label(Erg,text=mannschaft_))
            mannschaft[i].grid(row=rang+25,column=160)

            spieltag_=self.spieltag.n_spieltag
            spieltagx.append(tk.Label(Erg,text=spieltag_))
            spieltagx[i].grid(row=rang+25,column=165)

            torverhaeltnis_=str(self.torverhaeltnis[i])
            torverhaeltnis.append(tk.Label(Erg,text=torverhaeltnis_))
            torverhaeltnis[i].grid(row=rang+25,column=170)

            punkte_=str(self.punkte[i])
            punkte.append(tk.Label(Erg,text=punkte_))
            punkte[i].grid(row=rang+25,column=175)

            i+=1


        button_Weiter=tk.Button(Erg,text="nächster Spieltag",command=Erg.destroy)
        button_beenden=tk.Button(Erg,text="Beenden",command=lambda:[SpielBeenden(),Erg.destroy()])

        button_Weiter.grid(row=150, column=20)
        button_beenden.grid(row=150, column=30)


        Erg.mainloop()
        """



#++++++++++++++++++++++++++
#Definition der Funktionen
#++++++++++++++++++++++++++
def NeuesSpiel():
    global bundesliga
    bundesliga=Liga("Bundesliga")
    Liga.LigaSpeichern(bundesliga,"Bundesliga.txt")



def SpielLaden():
    global bundesliga
    bundesliga=Liga("Bundesliga")
    bundesliga=bundesliga.LigaLaden("Bundesliga.txt")

def SpielBeenden():
    print("spiel beenden")
    Liga.LigaSpeichern(bundesliga,"Bundesliga.txt")
    bundesliga.spieltag.n_spieltag=30



def AufstellungAendern():
    print("Aufstellung Ändern")

def schreibe(screen, text, x, y, size = 12,color = SCHWARZ, font_type = 'Comic Dans MS'):
    text = str(text)
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
    pygame.display.flip()



# Abfrage,ob Liga bereits besteht
global screen
screen=pygame.display.set_mode((1200,700))
pygame.display.set_caption("Fußballspiel")
clock=pygame.time.Clock()
spielaktiv=True
screen.fill(GRUEN)

#Rahmen Fenster
pygame.draw.rect(screen,SCHWARZ,[0,0,800,500],2)
pygame.draw.rect(screen,SCHWARZ,[0,500,800,200],2)
pygame.draw.rect(screen,SCHWARZ,[800,0,400,50],2)
pygame.draw.rect(screen,SCHWARZ,[800,50,400,250],2)
pygame.draw.rect(screen,SCHWARZ,[800,300,400,400],2)

#Rahmen Spieler
pygame.draw.rect(screen,SCHWARZ,[225,30,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[425,30,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[25,150,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[225,150,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[425,150,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[625,150,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[25,270,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[225,270,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[425,270,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[625,270,150,80],1)
pygame.draw.rect(screen,SCHWARZ,[325,390,150,80],1)


while spielaktiv:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            spielaktiv=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            print("Mausklick")


    pygame.display.flip()

    clock.tick(10)

    File1 = Path("c:\\Users\\chrcu\\Dropbox\\python\\Fussball\\Bundesliga.txt")

    if File1.is_file():
        neu_alt=tk.Tk()
        neu_alt.title("Neues Spiel?")
        text1=tk.Label(neu_alt,text="Soll ein neues spiel gestartet werden oder ein vorhandender Spielstand geladen werden?")
        button_neu=tk.Button(neu_alt,text="Neues Spiel",command=lambda:[neu_alt.destroy(),NeuesSpiel()])
        button_laden=tk.Button(neu_alt,text="Vorhandenes Spiel laden",command=lambda:[neu_alt.destroy(),SpielLaden()])
        text1.pack()
        button_neu.pack()
        button_laden.pack()
        neu_alt.mainloop()
    else:
        NeuesSpiel()



    #++++++++++++++++++++
    #Programmablauf
    #++++++++++++++++++++
    #print(bundesliga.mannschaften[0].spieler[0].alter)

    bundesliga.AufstellungErmitteln()
    #print(bundesliga.mannschaften[1].spieler[1].alter)
    #Fprint(bundesliga.mannschaften[0].spieler[0].alter)


    #++++++++++++++++++++++++++++++++
    #Aufstellung verändern- UserInput
    #++++++++++++++++++++++++++++++++
    aufst=tk.Tk()
    aufst.title("Aufstellung ändern?")
    text1=tk.Label(aufst,text="Möchten Sie die Aufstellung Ihrer Mannschaft verändern?")
    button_ja=tk.Button(aufst,text="Ja",command=lambda:[aufst.destroy(),AufstellungAendern()])
    button_nein=tk.Button(aufst,text="Nein",command=aufst.destroy)
    text1.pack()
    button_ja.pack()
    button_nein.pack()
    aufst.mainloop()



    #+++++++++++++++++++++++++++
    #Spielablauf
    #+++++++++++++++++++++++++++

    paarungen=[]
    paarung1=[[0,8],[1,9],[2,10],[3,11],[4,12],[5,13],[6,14],[7,15]]
    paarung2=[[0,9],[1,10],[2,11],[3,12],[4,13],[5,14],[6,15],[7,8]]
    paarung3=[[0,10],[1,11],[2,12],[3,13],[4,14],[5,15],[6,8],[7,9]]
    paarung4=[[0,11],[1,12],[2,13],[3,14],[4,15],[5,8],[6,9],[7,10]]
    paarung5=[[0,12],[1,13],[2,14],[3,15],[4,8],[5,9],[6,10],[7,11]]
    paarung6=[[0,13],[1,14],[2,15],[3,8],[4,9],[5,10],[6,11],[7,12]]
    paarung7=[[0,14],[1,15],[2,8],[3,9],[4,10],[5,11],[6,12],[7,13]]
    paarung8=[[0,15],[1,8],[2,9],[3,10],[4,11],[5,12],[6,13],[7,14]]
    paarung9=[[0,4],[1,5],[2,6],[3,7],[8,12],[9,13],[10,14],[11,15]]
    paarung10=[[0,5],[1,6],[2,7],[3,4],[8,13],[9,14],[10,15],[11,12]]
    paarung11=[[0,6],[1,7],[2,4],[3,5],[8,14],[9,15],[10,12],[11,13]]
    paarung12=[[0,7],[1,4],[2,5],[3,6],[8,15],[9,12],[10,13],[11,14]]
    paarung13=[[0,2],[1,3],[4,6],[5,7],[8,10],[9,11],[12,14],[13,15]]
    paarung14=[[0,3],[1,2],[4,7],[5,6],[8,11],[9,10],[12,15],[13,14]]
    paarung15=[[0,1],[2,3],[4,5],[6,7],[8,9],[10,11],[12,13],[14,15]]
    paarungen.append(paarung1)
    paarungen.append(paarung2)
    paarungen.append(paarung3)
    paarungen.append(paarung4)
    paarungen.append(paarung5)
    paarungen.append(paarung6)
    paarungen.append(paarung7)
    paarungen.append(paarung8)
    paarungen.append(paarung9)
    paarungen.append(paarung10)
    paarungen.append(paarung11)
    paarungen.append(paarung12)
    paarungen.append(paarung13)
    paarungen.append(paarung14)
    paarungen.append(paarung15)
    print(bundesliga.spieltag.n_spieltag)

    while bundesliga.spieltag.n_spieltag<=29:
        spiel=0


        ergebnis=[]
        if bundesliga.spieltag.n_spieltag<14:
            paarung=paarungen[bundesliga.spieltag.n_spieltag]
        elif bundesliga.spieltag.n_spieltag>=14:
                paarungHin=paarungen[bundesliga.spieltag.n_spieltag-14]
                paarung=paarungHin
                paarung[0]=paarungHin[1]
                paarung[1]=paarungHin[0]

        while spiel<8:
            ergebnis.append(bundesliga.SpielAusführen(paarung[spiel]))
            spiel+=1



        bundesliga.spieltag.ergebnisse.append(ergebnis)
        bundesliga.spieltag.n_spieltag+=1
        bundesliga.ErgebnisseAnzeigen(paarung,bundesliga.spieltag.ergebnisse[-1],bundesliga.spieltag.n_spieltag)

pygame.quit()



    #++++++++++++++++
    #Kontrolle
    #++++++++++++++++

    #print (bundesliga.mannschaften[0].spieler[0].alter)
    #print (bundesliga.mannschaften[1].spieler[1].alter)
