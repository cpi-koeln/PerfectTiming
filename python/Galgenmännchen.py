import random

woerter=["buch", "tisch", "stuhl", "erdbeere", "decke", "kissen", "schrank"]

loesung=random.choice(woerter)
laenge=int(len(loesung))

spielfeld=[]

i=0
while i< laenge:
    spielfeld.extend("_")
    i=i+1

print(spielfeld)
eingabe=[]
fehler=[]
i=0
j=0
while i<9:
    
    eingabe.extend(input("Welcher Buchstabe soll hinzugefügt werden ?"))
    treffer=0
    treffer=loesung.count(eingabe[j])
    if treffer>0:
        x=0
        while x<treffer:
            position=loesung.index(eingabe[j])
        
            spielfeld[position]=eingabe[j]
            x=x+1
        print("Sehr gut! Der Buchstabe ist im Wort enthalten!")
        print(spielfeld)
        j=j+1
    else:
        print("Schade! Der Buchstabe ist nicht im Lösungswort enthalten.")
        i=i+1
        j=j+1
        print("Noch ",9-i, "Züge")
    

        
