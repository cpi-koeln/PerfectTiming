x=0
import random

zahl=random.randint(0,100)
while x<7:
    frage=input("Gebe eine Zahl ein:")
    frage=int(frage)
    if frage < zahl:
        print("deine geratene Zahl ist zu klein")
        x=x+1
    elif (frage >zahl):
        print("deine geratene Zahl ist zu groß")
        x=x+1
    else:
        print("Gewonnen")
        x=7

    
