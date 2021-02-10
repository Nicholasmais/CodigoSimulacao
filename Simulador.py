from tkinter import Button, Entry, Frame, Scale, Tk, mainloop
import pandas as pd
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.ticker as plticker
import os

matplotlib.use("TkAgg")

arquivo = pd.read_excel((str(os.getcwd())) + "\dados.xlsx")


def refletividade(t):
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

    return [data[0], rl]


janela = Tk()
janela.state("zoomed")
janela.title("Simulação")
janela.minsize(500, 500)

frame_grafico = Frame(janela, bd=5, bg='black', relief='ridge')
frame_grafico.pack(expand=True, fill='both')

fi = Figure(figsize=(5, 4), dpi=100)

canvas = FigureCanvasTkAgg(fi, master=frame_grafico)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
canvas._tkcanvas.pack(side='top', fill='both', expand=1)

frame_esquerda = Frame(janela)
frame_esquerda.pack(side='left', fill='both', expand=True)
frame_direita = (Frame(janela))
frame_direita.pack(side='right', fill='both', expand=True)


def update(var):
    global dadosxy
    pos = slider.get()
    entryEsp.delete(0, 'end')
    entryEsp.insert(0, ("%.3f" % pos))
    dadosxy = refletividade(pos / 1000)
    line.set_data(dadosxy[0], dadosxy[1])
    fi.canvas.draw_idle()


frame_slider = Frame(frame_direita, bg='black', bd=5, relief='ridge')
frame_slider.pack(expand=1)

slider = Scale(frame_slider, from_=2, to=8, length=270, orient='horizontal', tickinterval=1,
               resolution=.1, command=update)
slider.set(5)
slider.pack()

frame_esp = Frame(frame_esquerda, bd=5, bg='black', relief='ridge')
frame_esp.pack()

entryEsp = Entry(frame_esp, width=10)
entryEsp.pack(side="left", fill='both')
entryEsp.insert(0, '0.004')


def atualiza_plot():
    pos = float(entryEsp.get())
    slider.set(pos)
    update(slider.get())


btn = Button(frame_esp, text="Espessura", width=20, command=atualiza_plot)
btn.pack(side="right", fill='x')

frame_lim_superior = Frame(frame_esquerda, bd=5, bg='black', relief='ridge')
frame_lim_superior.pack()

frame_lim_inferior = Frame(frame_esquerda, bd=5, bg='black', relief='ridge')
frame_lim_inferior.pack()

NavigationToolbar2Tk(canvas, frame_slider)

ymin = Entry(frame_lim_inferior, width=10)
ymin.pack(side='left', fill='both')

frame_nome = Frame(frame_esquerda, bd=6, bg='black', relief='ridge')
frame_nome.pack()

nome = Entry(frame_nome, width=40)
nome.pack()


def atualiza_axis():
    a.set_ylim(ymin=-np.absolute(float(ymin.get())))
    fi.canvas.draw_idle()


def atualiza_axiss():
    a.set_ylim(ymax=-np.absolute(float(ymax.get())))
    fi.canvas.draw_idle()


btn_lim_inferior = Button(frame_lim_inferior,
                          text="Limite inferior", width=20, command=atualiza_axis)
btn_lim_inferior.pack(side="right", fill='x')

ymax = Entry(frame_lim_superior, width=10)
ymax.pack(side='left', fill='both')

btn_lim_superior = Button(frame_lim_superior, text='Limite Superior', width=20, command=atualiza_axiss)
btn_lim_superior.pack(side='left', fill='both')

a = fi.add_subplot(111)
dadosxy = refletividade(.004)
line, = a.plot(dadosxy[0], dadosxy[1])
a.set_ylim(-30, 0)
a.grid()
a.axes.format_coord = lambda x, y: ""


def nomeup():
    a.set_title(str(nome.get()), fontsize=15)
    fi.canvas.draw_idle()


btn2 = Button(frame_nome, text='Alterar título', command=nomeup)
btn2.pack(fill='x')
tick = plticker.MultipleLocator(base=0.5)
a.xaxis.set_major_locator(tick)
a.set_ylabel('Refletividade (dB)', fontsize=15)
a.set_xlabel('Frequência (GHz)', fontsize=15)

mainloop()
