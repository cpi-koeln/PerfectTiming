
import tkinter as tk


Fenster=tk.Tk()
Fenster.title("Titel")
text1=tk.Label(Fenster,text="text1")
button_ja=tk.Button(Fenster,text="Ja")
button_nein=tk.Button(Fenster,text="Nein")
text1.pack()
button_ja.pack()
button_nein.pack()
Fenster.mainloop()
