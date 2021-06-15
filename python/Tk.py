import tkinter as tk
root=tk.Tk()
eingabefeld=tk.Entry(root)
eingabefeld_wert=tk.StringVar()
eingabefeld["textvariable"] = eingabefeld_wert
eingabefeld["show"] = "*"
eingabefeld.pack()
