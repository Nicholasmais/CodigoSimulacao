from tkinter import *
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
import matplotlib.ticker as plticker


matplotlib.use("TkAgg")


arquivo = pd.read_excel(r"C:\Users\nicoe\PycharmProjects\CodigoSimulacao\e1.xlsx")
#print(arquivo)


def Refetividade(t):
    er = []
    ur = []
    c = 299792458
    k = []
    n = []
    R = []
    rl = []
    data = []
    for colunas in arquivo.columns:
        data.append(arquivo[colunas].tolist())

    for j in range(0, len(data[0])):
        er.append(np.complex(data[1][j], data[2][j]))
        ur.append(np.complex(data[3][j], data[4][j]))
        k.append(2 * np.pi * data[0][j] / c)
        n.append(((ur[j] / er[j]) ** (1 / 2)) * np.tanh(np.complex(0, -1 * k[j] * t * ((ur[j] * er[j]) ** (1 / 2)))))
        R.append((n[j] - 1) / (n[j] + 1))
        rl.append(20 * np.log(np.absolute(R[j])))

    for i in range(0, len(data[0])):
        data[0][i] = data[0][i] / 1000000000

    return [data[0],rl]


janela = Tk()
janela.state("zoomed")
janela.title("Simulador")





fi = Figure(figsize=(5, 4), dpi=100)
fi.subplots_adjust(bottom=0.35)

canvas = FigureCanvasTkAgg(fi, master=janela)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
NavigationToolbar2Tk(canvas,janela)
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

entryEsp = Entry(janela)
entryEsp.pack(side="left",expand=True,fill='x')
entryEsp.insert(0,'0.004')

def atualiza_plot():
    pos = float(entryEsp.get())
    sld_var.set_val(pos)
    update(sld_var)

btn = Button(janela,text = "OK", command = atualiza_plot)
btn.pack(side="right",expand=True,fill='x')



#plt.axis([8,13,-30,0])
a = fi.add_subplot(111)
dadosxy = Refetividade(.004)
line, = a.plot(dadosxy[0],dadosxy[1])
a.set_ylim(-30,0)
a.grid()

tick = plticker.MultipleLocator(base=0.5)
a.xaxis.set_major_locator(tick)
a.set_title('Simulation')
a.set_ylabel('Reflection Loss (dB)')
a.set_xlabel('Frequency (GHz)')


ax_var = fi.add_axes([0.12,0.1,0.78,0.03])
sld_var = Slider(ax_var,"Espessura",.002,.009,valinit=.004)
def update(val):
    pos = sld_var.val
    entryEsp.delete(0,'end')
    entryEsp.insert(0,("%.3f"%pos))
    dadosxy = Refetividade(pos)
    line.set_data(dadosxy[0],dadosxy[1])
    fi.canvas.draw_idle()

sld_var.on_changed(update)








tk.mainloop()

