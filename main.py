import yfinance as yf
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import QtCore
from tkinter import *
import time



root = Tk()
root.resizable(height = None, width = None)
root.title("Stocks")
# root.geometry("400x150")

STOCK_LIST = []


#PULL DATA FROM YFINANCE API
class Ticker:
    def __init__(self,stock):
        self.stock = stock

    def get_price(self):
        kretanje = 1
        while kretanje:
            data = yf.download(tickers=self.stock, period='1d', interval='1m')
            data2 = yf.download(tickers=self.stock, period='2d', interval='1d')

            a = data["Close"]
            z = data2["Close"]
            a = list(a)
            z = list(z)

            global gme_close_price
            gme_close_price = round((z[-1]), 2)

            GME = ((a[-1] / z[0]) - 1) * 100
            print(GME)

            global gme_iznos
            gme_iznos = round(GME, 2)

            kretanje = False
            return gme_iznos, gme_close_price



# CREATING STOCKS AND LABELS
class Stock_labels:
    def __init__(self,master, stock):
        self.master = master
        self.stock = stock

    def stock10(self):
        global a0
        a0= Ticker(self.stock)

        # dodjeljuje različite .grid columne ovisno o kojoj poziciji u STOCK_LIST se dionica nalazi
        for i in range(len(STOCK_LIST)):
            if self.stock == STOCK_LIST[i]:
                b = i

        self.STOCK_label = Label(self.master, text=self.stock, relief=SUNKEN, bg="lightgrey", padx=5, width=18)
        self.STOCK_label.grid(row=b, column=0, pady=10, padx=10)

        self.STOCK_close_price = Label(self.master, text=f"Price: {a0.get_price()[1]}$",relief=SUNKEN, bg="lightblue",padx=5, width=16)
        self.STOCK_close_price.grid(row=b, column=2, pady=10,padx=10)

        self.STOCK_change_price = Label(self.master, text=f"Price change = {gme_iznos}%", relief=SUNKEN, bg="lightyellow", padx=5, width=16)
        self.STOCK_change_price.grid(row=b, column=1, pady=10,padx=10)

        if gme_iznos > 0:
            self.STOCK_change_price["bg"] = "lightgreen"
        else:
            self.STOCK_change_price["bg"] = "lightcoral"



# REFRESH STOCK PRICE EVERY X SECONDS
def refresher():

    for i in range(len(STOCK_LIST)):
        b = Stock_labels(root, STOCK_LIST[i])
        try:
            b.stock10()
        except IndexError:
            if entry1.get() == STOCK_LIST[i]:
                b = i
                Label(root, text="nima toga jeben ti miša").grid(row=b, column=1,columnspan=2)
    # quit()
    root.after(2000, refresher)

def quit():
    quit1 = Button(root, text="Press 2 quit", command=root.quit)
    quit1.grid(row=4, column=0, padx = 10, columnspan=1)


def appendaj_stock():
    STOCK_LIST.append(entry1.get())


Label(root, text="ADD STOCK:").grid(row=10, column=0, sticky=E)

entry1 = Entry(root)
entry1.grid(row=10, column=1)

# TU CE COMMAND BITI DA DODA NOVo
button1 = Button(root, text="POKRENI", command= appendaj_stock,width=16)
button1.grid(row=10, column=2, sticky="e")

refresher()
root.mainloop()







