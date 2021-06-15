class Auto():
    def __init__(self,farbe,marke,plaetze,kilometerstand):
        self.farbe=farbe
        self.marke=marke
        self.platze=plaetze
        self.kilometerstand=kilometerstand


    def hupen(self,Anzahl):
        print(Anzahl*"hup")

    def fahren(self,km):
        print("Das Auto ist auf dieser Fahrt so weit gefahren:", km)
        self.kilometerstand+=km
        print("Der Kilometerstand beträgt:",self.kilometerstand)



mein_auto=Auto("weiß","Toyota",4,25000)

print(mein_auto.farbe)

mein_auto.fahren(10)
