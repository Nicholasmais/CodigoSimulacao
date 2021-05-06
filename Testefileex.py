
import tkinter as tk
import tkinter.filedialog as tkf
import pandas as pd

janela = tk.Tk()
janela.minsize(500, 500)

frame1 = tk.Frame(janela, bg='skyblue')
frame1.pack(expand=True, fill='both')

def abre():
    filename = tkf.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
    file = pd.read_excel(f"{filename}")
    print(file)
botao = tk.Button(frame1, text='Teste', command = abre)
botao.pack()

janela.mainloop()