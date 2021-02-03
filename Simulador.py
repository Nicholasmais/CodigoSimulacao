from tkinter import *
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

er = []
ur = []
t = 0.004
c = 299792458
k = []
n = []
R = []
rl = []
mod = []
arquivo = pd.read_excel(r"C:\Users\nicoe\PycharmProjects\CodigoSimulacao\e1.xlsx")
print(arquivo)

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

fi = Figure(figsize=(5, 4), dpi=100)

a = fi.add_subplot(111)
a.set_title('Simulation')
a.set_ylabel('Reflection Loss (dB)')
a.set_xlabel('Frequency (GHz)')
a.plot(data[0], rl)

janela = Tk()
janela.title("Simulador")
janela['bg'] = 'skyblue'

nome = Label(janela, text='Simulador', width=20, height=20)
nome.place(relx=0.5, rely=0.1, anchor='center')
nome.configure(font="-family {Euphorigenic} -size 27 -weight bold -slant italic", bg='skyblue')

canvas = FigureCanvasTkAgg(fi, master=janela)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

tk.mainloop()
